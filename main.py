import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

drawer = mp.solutions.drawing_utils

while True:
    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            drawer.draw_landmarks(
                frame,
                hand,
                mpHands.HAND_CONNECTIONS
            )

    cv2.imshow("Hand Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()