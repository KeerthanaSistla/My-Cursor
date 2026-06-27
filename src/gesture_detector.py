import math
import config


class GestureDetector:

    def __init__(self):

        self.left_button_down = False

    def distance(self, p1, p2):

        return math.hypot(
            p1[1] - p2[1],
            p1[2] - p2[2]
        )

    def get_cursor(self, landmarks):

        _, x, y = landmarks[8]

        return x, y

    def detect_left_button(self, landmarks):

        thumb = landmarks[4]
        index = landmarks[8]

        dist = self.distance(thumb, index)

        if dist < config.PINCH_DISTANCE:

            if not self.left_button_down:

                self.left_button_down = True

                return "DOWN"

            return "HOLD"

        else:

            if self.left_button_down:

                self.left_button_down = False

                return "UP"

        return "NONE"