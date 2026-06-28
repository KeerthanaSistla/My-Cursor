import math
import time
from . import config


class GestureDetector:

    def __init__(self):
        # Left click state
        self.left_button_down = False
        self._left_pinch_counter = 0
        self._left_release_counter = 0
        self._pinch_start_time = 0
        
        # Right click state
        self.right_button_down = False
        
        # Scroll state
        self.previous_scroll_y = None
        
        # Zoom state
        self.previous_zoom_distance = None

    def distance(self, p1, p2):
        return math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])

    # --------------------------------------------------
    # Cursor Position (Index Finger Tip)
    # --------------------------------------------------
    def cursor_position(self, hand):
        index_tip = hand["landmarks"][8]
        return (index_tip["x"], index_tip["y"])

    # --------------------------------------------------
    # Finger States (are fingers extended?)
    # --------------------------------------------------
    def finger_states(self, hand):
        lm = hand["landmarks"]
        return {
            "thumb": lm[4]["x"] < lm[3]["x"],
            "index": lm[8]["y"] < lm[6]["y"],
            "middle": lm[12]["y"] < lm[10]["y"],
            "ring": lm[16]["y"] < lm[14]["y"],
            "little": lm[20]["y"] < lm[18]["y"]
        }

    # --------------------------------------------------
    # Left Click / Drag (Thumb + Index Pinch)
    # Returns: "NONE" | "DOWN" | "HOLD" | "UP"
    # --------------------------------------------------
    def left_state(self, hand):
        """
        Pinch = Mouse Down
        Release = Mouse Up (fires click if was down)
        
        The mouse controller will handle:
        - If DOWN followed quickly by UP = click
        - If DOWN held = drag
        """
        lm = hand["landmarks"]
        d = self.distance(lm[4], lm[8])  # Distance between thumb tip and index tip
        
        # Debug print to see what distances we're getting
        # print(f"Pinch distance: {d:.1f}, Down threshold: {config.PINCH_DOWN_DISTANCE}, Hold threshold: {config.PINCH_HOLD_DISTANCE}")

        if self.left_button_down:
            # Currently holding - check if we should release
            if d > config.PINCH_HOLD_DISTANCE:
                self._left_release_counter += 1
                if self._left_release_counter >= config.PINCH_DEBOUNCE_FRAMES:
                    self.left_button_down = False
                    self._left_pinch_counter = 0
                    self._left_release_counter = 0
                    return "UP"  # Release
                return "HOLD"  # Still holding during debounce
            else:
                self._left_release_counter = 0
                return "HOLD"  # Still pinching
        else:
            # Not holding - check if we should press
            if d < config.PINCH_DOWN_DISTANCE:
                self._left_pinch_counter += 1
                if self._left_pinch_counter >= config.PINCH_DEBOUNCE_FRAMES:
                    self.left_button_down = True
                    self._pinch_start_time = time.time()
                    self._left_release_counter = 0
                    return "DOWN"  # Start pressing
                return "NONE"  # Still debouncing
            else:
                self._left_pinch_counter = 0
                return "NONE"

    # --------------------------------------------------
    # Right Click (Thumb + Middle Pinch)
    # --------------------------------------------------
    def right_click(self, hand):
        lm = hand["landmarks"]
        d = self.distance(lm[4], lm[12])  # Thumb tip to middle tip
        
        if d < config.RIGHT_CLICK_DISTANCE:
            if not self.right_button_down:
                self.right_button_down = True
                return True
            return False
        else:
            self.right_button_down = False
            return False

    # --------------------------------------------------
    # Scroll Mode Detection (Index + Middle Extended)
    # --------------------------------------------------
    def scroll_mode(self, hand):
        fingers = self.finger_states(hand)
        return (fingers["index"] and fingers["middle"] and 
                not fingers["ring"] and not fingers["little"])

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

        return delta * config.SCROLL_SPEED

    # --------------------------------------------------
    # Zoom Mode (Two Hands)
    # --------------------------------------------------
    def zoom_mode(self, hands):
        return len(hands) == 2

    def zoom_amount(self, hands):
        if len(hands) != 2:
            self.previous_zoom_distance = None
            return 0

        hand1_wrist = hands[0]["landmarks"][0]
        hand2_wrist = hands[1]["landmarks"][0]

        current_distance = self.distance(hand1_wrist, hand2_wrist)

        if self.previous_zoom_distance is None:
            self.previous_zoom_distance = current_distance
            return 0

        delta = current_distance - self.previous_zoom_distance
        self.previous_zoom_distance = current_distance

        if abs(delta) < config.ZOOM_DEADZONE:
            return 0

        return delta * config.ZOOM_SPEED