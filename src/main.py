import cv2
import time

from . import config
from .hand_tracker import HandTracker
from .gesture_detector import GestureDetector
from .mouse_controller import MouseController


def main():
    camera = cv2.VideoCapture(config.CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

    tracker = HandTracker()
    gesture = GestureDetector()
    mouse = MouseController()

    previous_time = time.time()

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame, hands = tracker.process(frame)

        gesture_name = "No Hand"

        # =====================================================
        # TWO HANDS -> ZOOM MODE
        # =====================================================
        if gesture.zoom_mode(hands):
            amount = gesture.zoom_amount(hands)
            if amount != 0:
                mouse.zoom(amount)
                gesture_name = "ZOOM"

        # =====================================================
        # ONE HAND -> GESTURE MODE
        # =====================================================
        elif len(hands) == 1:
            hand = hands[0]
            x, y = gesture.cursor_position(hand)
            frame_height, frame_width, _ = frame.shape

            # Check scroll mode first (index + middle extended)
            if gesture.scroll_mode(hand):
                amount = gesture.scroll_amount(hand)
                if amount != 0:
                    mouse.scroll(amount)
                gesture_name = "SCROLL"
            else:
                # Move cursor
                mouse.move(x, y, frame_width, frame_height)

                # Check right click (thumb + middle pinch)
                if gesture.right_click(hand):
                    mouse.right_click()
                    gesture_name = "RIGHT CLICK"
                else:
                    # Check left click/drag (thumb + index pinch)
                    left_state = gesture.left_state(hand)
                    
                    if left_state == "DOWN":
                        mouse.left_down()
                        gesture_name = "MOUSE DOWN"
                    elif left_state == "HOLD":
                        # Mouse is down, can move to drag
                        gesture_name = "DRAGGING"
                    elif left_state == "UP":
                        mouse.left_up()
                        gesture_name = "MOUSE UP (CLICK)"
                    else:
                        gesture_name = "MOVE"

            # Draw cursor position
            color = (0, 0, 255)  # Red by default
            if gesture.left_button_down:
                color = (0, 255, 0)  # Green when mouse is down
            cv2.circle(frame, (x, y), 10, color, -1)

            # Draw pinch distance indicator for debugging
            lm = hand["landmarks"]
            pinch_dist = gesture.distance(lm[4], lm[8])
            cv2.putText(frame, f"Pinch: {pinch_dist:.0f}", (x + 20, y - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # =====================================================
        # Display Info
        # =====================================================
        if config.SHOW_GESTURE:
            cv2.putText(frame, gesture_name, (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if config.SHOW_FPS:
            current_time = time.time()
            fps = 1 / (current_time - previous_time)
            previous_time = current_time
            cv2.putText(frame, f"FPS : {int(fps)}", (20, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("MyCursor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()