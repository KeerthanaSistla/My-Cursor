import cv2
import mediapipe as mp
import config


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            max_num_hands=config.MAX_HANDS,
            min_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE
        )

        self.drawer = mp.solutions.drawing_utils

    def process(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        landmarks = []

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            self.drawer.draw_landmarks(
                frame,
                hand,
                self.mpHands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            for id, lm in enumerate(hand.landmark):

                x = int(lm.x * w)
                y = int(lm.y * h)

                landmarks.append((id, x, y))

        return frame, landmarks