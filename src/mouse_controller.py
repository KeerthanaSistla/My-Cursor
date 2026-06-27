import pyautogui
import config


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        self.current_x = self.screen_width // 2
        self.current_y = self.screen_height // 2

        pyautogui.FAILSAFE = False

    # --------------------------------------------------
    # Cursor Movement
    # --------------------------------------------------

    def move(self, x, y, frame_width, frame_height):

        target_x = int(
            (x / frame_width) *
            self.screen_width *
            config.MOVE_SPEED
        )

        target_y = int(
            (y / frame_height) *
            self.screen_height *
            config.MOVE_SPEED
        )

        self.current_x += (
            target_x - self.current_x
        ) * config.CURSOR_SMOOTHING

        self.current_y += (
            target_y - self.current_y
        ) * config.CURSOR_SMOOTHING

        self.current_x = max(
            0,
            min(self.current_x, self.screen_width)
        )

        self.current_y = max(
            0,
            min(self.current_y, self.screen_height)
        )

        pyautogui.moveTo(
            int(self.current_x),
            int(self.current_y)
        )

    # --------------------------------------------------
    # Left Mouse
    # --------------------------------------------------

    def left_down(self):

        pyautogui.mouseDown(button="left")

    def left_up(self):

        pyautogui.mouseUp(button="left")

    # --------------------------------------------------
    # Right Mouse
    # --------------------------------------------------

    def right_click(self):

        pyautogui.click(button="right")

    # --------------------------------------------------
    # Scroll
    # --------------------------------------------------

    def scroll(self, amount):

        pyautogui.scroll(
            int(amount * config.SCROLL_SPEED)
        )

    # --------------------------------------------------
    # Zoom
    # --------------------------------------------------

    def zoom(self, amount):

        pyautogui.keyDown("ctrl")

        pyautogui.scroll(
            int(amount * config.ZOOM_SPEED)
        )

        pyautogui.keyUp("ctrl")