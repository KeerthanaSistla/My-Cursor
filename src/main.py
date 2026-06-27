import cv2
from hand_tracker import HandTracker

camera = cv2.VideoCapture(0)

tracker = HandTracker()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.process(frame)

    if landmarks:

        index_tip = landmarks[8]

        _, x, y = index_tip

        cv2.circle(frame, (x, y), 15, (0, 0, 255), -1)

        cv2.putText(
            frame,
            f"X:{x}  Y:{y}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

    cv2.imshow("MyCursor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()