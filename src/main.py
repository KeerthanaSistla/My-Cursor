import cv2

import config

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController


camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

tracker = HandTracker()

gesture = GestureDetector()

mouse = MouseController()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.process(frame)

    if landmarks:

        x, y = gesture.get_cursor(landmarks)

        h, w, _ = frame.shape

        mouse.move(x, y, w, h)

        state = gesture.detect_left_button(landmarks)

        if state == "DOWN":
            mouse.left_down()

        elif state == "UP":
            mouse.left_up()

        cv2.circle(frame, (x, y), 12, (0, 0, 255), -1)

        cv2.putText(
            frame,
            state,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

    cv2.imshow("MyCursor", frame)

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()