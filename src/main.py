import cv2
import pyautogui
from hand_tracker import HandTracker

camera = cv2.VideoCapture(0)

tracker = HandTracker()

screen_width, screen_height = pyautogui.size()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.process(frame)

    if landmarks:

        _, x, y = landmarks[8]

        camera_height, camera_width, _ = frame.shape

        screen_x = int((x / camera_width) * screen_width)
        screen_y = int((y / camera_height) * screen_height)

        cv2.circle(frame, (x, y), 15, (0, 0, 255), -1)

        pyautogui.moveTo(screen_x, screen_y)

    cv2.imshow("MyCursor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()