# Real-Time Object Tracking

This project provides two Python scripts for real-time object tracking using a webcam feed.
### Example:


[🎥 Watch the demo](./Test.mp4)
## Requirements

*   Python 3
*   OpenCV (`opencv-python`)
*   NumPy

You can install the required libraries using pip:

```bash
pip install opencv-python numpy
```

## How to Run

1.  Navigate to the `Scripts` directory in your terminal.
2.  Run either of the tracking scripts:

    ```bash
    python tracker.py
    ```

    or

    ```bash
    python refinder_tracker.py
    ```
3. - Press `s` to select ROI
   - Press `Enter` to confirm ROI selected
   - Press `r` to refind the selected ROI
   - Press `q` to quit

### `tracker.py`

This script is a basic object tracker.

**How it works:**

1.  It captures video from the webcam.
2.  The user can press the 's' key to pause the feed and select an object to track by drawing a bounding box around it.
3.  The script then uses the CSRT tracker from OpenCV to track the selected object in the video feed, drawing a green box around it.
4.  If the tracker loses the object, a "Lost" message is displayed.
5.  The user can press 'q' to quit the application.

### `refinder_tracker.py`

This script is a more advanced object tracker with a "refind" feature.

**How it works:**

1.  It captures video from the webcam.
2.  The user can press 's' to select an object to track.
3.  The CSRT tracker follows the object.
4.  If the tracker loses the object, the user can press 'r'. This will use template matching to try and find the object again.
5.  If the object is found, the tracker is re-initialized with the new location.
6.  The user can press 'q' to quit.


