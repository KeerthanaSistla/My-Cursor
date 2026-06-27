import cv2
import time

import config
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController


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
        # ONE HAND -> NORMAL MODE
        # =====================================================

        elif len(hands) == 1:

            hand = hands[0]

            x, y = gesture.cursor_position(hand)

            frame_height, frame_width, _ = frame.shape

            left_state = gesture.left_state(hand)

            right_click = gesture.right_click(hand)

            scroll_mode = gesture.scroll_mode(hand)

            if scroll_mode:

                amount = gesture.scroll_amount(hand)

                if amount != 0:

                    mouse.scroll(amount)

                gesture_name = "SCROLL"

            else:

                mouse.move(
                    x,
                    y,
                    frame_width,
                    frame_height
                )

                if left_state == "DOWN":

                    mouse.left_down()

                    gesture_name = "LEFT DOWN"

                elif left_state == "HOLD":

                    gesture_name = "LEFT HOLD"

                elif left_state == "UP":

                    mouse.left_up()

                    gesture_name = "LEFT UP"

                elif right_click:

                    mouse.right_click()

                    gesture_name = "RIGHT CLICK"

                else:

                    gesture_name = "MOVE"

            if config.SHOW_FINGER_STATES:

                states = gesture.finger_states(hand)

                cv2.putText(
                    frame,
                    str(states),
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

            if config.SHOW_GESTURE:

                cv2.putText(
                    frame,
                    gesture_name,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            cv2.circle(
                frame,
                (x, y),
                10,
                (0, 0, 255),
                -1
            )

        # =====================================================
        # FPS
        # =====================================================

        if config.SHOW_FPS:

            current_time = time.time()

            fps = 1 / (current_time - previous_time)

            previous_time = current_time

            cv2.putText(
                frame,
                f"FPS : {int(fps)}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

        cv2.imshow("MyCursor", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()