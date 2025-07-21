import cv2
import numpy as np

# --- Setup ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

cv2.namedWindow("Live Feed")
cv2.namedWindow("Tracking")

tracker = None
tracking = False
template = None
template_size = None
status_message = "Press 's' to select object, 'r' to refind, 'q' to quit"

# --- Main Loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Frame not read.")
        break

    display_frame = frame.copy()

    # --- Tracking Mode ---
    if tracking and tracker is not None:
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = map(int, box)
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            status_message = "Tracking (press 'r' to refind)"
        else:
            status_message = "Lost (press 'r' to refind)"
            tracking = False

    # --- Draw Status ---
    cv2.putText(display_frame, status_message, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    cv2.imshow("Live Feed", display_frame)
    cv2.imshow("Tracking", display_frame)

    key = cv2.waitKey(1) & 0xFF

    # --- Quit ---
    if key == ord('q'):
        break

    # --- Manual Initial Selection ---
    elif key == ord('s'):
        paused_frame = frame.copy()
        box = cv2.selectROI("Live Feed", paused_frame, fromCenter=False, showCrosshair=True)

        if box[2] > 0 and box[3] > 0:
            x, y, w, h = map(int, box)
            template = frame[y:y+h, x:x+w]
            template_size = (w, h)

            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, box)
            tracking = True
            status_message = "Tracker initialized"
        else:
            status_message = "Invalid ROI"

    # --- Refind Using Template ---
    elif key == ord('r') and template is not None:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(gray_frame, gray_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > 0.6:
            top_left = max_loc
            x, y = top_left
            w, h = template_size

            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, (x, y, w, h))
            tracking = True
            status_message = f"Refound object (score: {max_val:.2f})"
        else:
            status_message = f"Refind failed (score: {max_val:.2f})"

cap.release()
cv2.destroyAllWindows()
