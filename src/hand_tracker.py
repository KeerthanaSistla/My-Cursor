import cv2
import mediapipe as mp
from . import config



class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_HANDS,
            min_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE
        )

        self.drawer = mp.solutions.drawing_utils

    def process(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        detected_hands = []

        # If no hands are detected, return an empty list for consistency.
        if results.multi_hand_landmarks:

            frame_height, frame_width, _ = frame.shape

            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                if config.SHOW_CONNECTIONS:

                    self.drawer.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

                landmarks = []

                for index, landmark in enumerate(hand_landmarks.landmark):

                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)

                    landmarks.append(
                        {
                            "id": index,
                            "x": x,
                            "y": y
                        }
                    )

                    if config.SHOW_LANDMARKS:

                        cv2.circle(
                            frame,
                            (x, y),
                            4,
                            (0, 0, 255),
                            -1
                        )

                detected_hands.append(
                    {
                        "label": handedness.classification[0].label,
                        "landmarks": landmarks
                    }
                )

        return frame, detected_hands