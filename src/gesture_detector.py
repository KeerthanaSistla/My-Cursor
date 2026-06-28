import math
from . import config



class GestureDetector:

    def __init__(self):

        self.left_button_down = False
        self.right_button_down = False

        self.previous_scroll_y = None
        self.previous_zoom_distance = None

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def distance(self, p1, p2):

        return math.hypot(
            p1["x"] - p2["x"],
            p1["y"] - p2["y"]
        )

    # --------------------------------------------------
    # Cursor
    # --------------------------------------------------

    def cursor_position(self, hand):

        index_tip = hand["landmarks"][8]

        return (
            index_tip["x"],
            index_tip["y"]
        )

    # --------------------------------------------------
    # Finger States
    # --------------------------------------------------

    def finger_states(self, hand):

        lm = hand["landmarks"]

        return {

            "thumb":
                lm[4]["x"] < lm[3]["x"],

            "index":
                lm[8]["y"] < lm[6]["y"],

            "middle":
                lm[12]["y"] < lm[10]["y"],

            "ring":
                lm[16]["y"] < lm[14]["y"],

            "little":
                lm[20]["y"] < lm[18]["y"]

        }

    # --------------------------------------------------
    # Left Click
    # --------------------------------------------------

    def left_state(self, hand):

        lm = hand["landmarks"]

        touching = (
            self.distance(lm[4], lm[8])
            < config.PINCH_DISTANCE
        )

        if touching:

            if not self.left_button_down:

                self.left_button_down = True
                return "DOWN"

            return "HOLD"

        else:

            if self.left_button_down:

                self.left_button_down = False
                return "UP"

        return "NONE"

    # --------------------------------------------------
    # Right Click
    # --------------------------------------------------

    def right_click(self, hand):

        lm = hand["landmarks"]

        touching = (
            self.distance(lm[4], lm[12])
            < config.RIGHT_CLICK_DISTANCE
        )

        if touching:

            if not self.right_button_down:

                self.right_button_down = True
                return True

        else:

            self.right_button_down = False

        return False

    # --------------------------------------------------
    # Scroll Mode
    # --------------------------------------------------

    def scroll_mode(self, hand):

        fingers = self.finger_states(hand)

        return (

            fingers["index"]

            and

            fingers["middle"]

            and

            not fingers["ring"]

            and

            not fingers["little"]

        )

    def scroll_amount(self, hand):

        if not self.scroll_mode(hand):

            self.previous_scroll_y = None
            return 0

        y = hand["landmarks"][8]["y"]

        if self.previous_scroll_y is None:

            self.previous_scroll_y = y
            return 0

        delta = self.previous_scroll_y - y

        self.previous_scroll_y = y

        if abs(delta) < config.SCROLL_DEADZONE:
            return 0

        return delta

    # --------------------------------------------------
    # Zoom Mode
    # --------------------------------------------------

    def zoom_mode(self, hands):

        return len(hands) == 2

    def zoom_amount(self, hands):

        if len(hands) != 2:

            self.previous_zoom_distance = None
            return 0

        hand1 = hands[0]["landmarks"][0]
        hand2 = hands[1]["landmarks"][0]

        current_distance = self.distance(hand1, hand2)

        if self.previous_zoom_distance is None:

            self.previous_zoom_distance = current_distance
            return 0

        delta = current_distance - self.previous_zoom_distance

        self.previous_zoom_distance = current_distance

        if abs(delta) < config.ZOOM_DEADZONE:
            return 0

        return delta