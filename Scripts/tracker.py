import cv2

# Define tracker
tracker = cv2.TrackerCSRT_create()

initBB = None  # Bounding box
tracking = False

# Start webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    key = cv2.waitKey(1) & 0xFF

    # If tracking is active, update the tracker
    if tracking:
        success, box = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Show instructions
    cv2.putText(frame, "Press 's' to select object, 'q' to quit", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show frame
    cv2.imshow("Live Object Tracker", frame)

    # Press 's' to select ROI
    if key == ord("s"):
        tracking = False  # Pause tracking during selection
        initBB = cv2.selectROI("Select Object", frame, False, False)
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, initBB)
        tracking = True

    # Press 'q' to quit
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
