import pyautogui
from . import config


class MouseController:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.current_x = self.screen_width // 2
        self.current_y = self.screen_height // 2
        pyautogui.FAILSAFE = False
        
        # Track mouse state
        self.mouse_down = False

    def move(self, x, y, frame_width, frame_height):
        target_x = int((x / frame_width) * self.screen_width * config.MOVE_SPEED)
        target_y = int((y / frame_height) * self.screen_height * config.MOVE_SPEED)

        self.current_x += (target_x - self.current_x) * config.CURSOR_SMOOTHING
        self.current_y += (target_y - self.current_y) * config.CURSOR_SMOOTHING

        self.current_x = max(0, min(self.current_x, self.screen_width - 1))
        self.current_y = max(0, min(self.current_y, self.screen_height - 1))

        pyautogui.moveTo(int(self.current_x), int(self.current_y), _pause=False)

    # --------------------------------------------------
    # Left Mouse Button (simple down/up like real mouse)
    # --------------------------------------------------
    def left_down(self):
        """Press left mouse button"""
        if not self.mouse_down:
            pyautogui.mouseDown(button="left", _pause=False)
            self.mouse_down = True
            print("MOUSE DOWN")  # Debug

    def left_up(self):
        """Release left mouse button"""
        if self.mouse_down:
            pyautogui.mouseUp(button="left", _pause=False)
            self.mouse_down = False
            print("MOUSE UP - CLICK REGISTERED")  # Debug

    # --------------------------------------------------
    # Right Mouse
    # --------------------------------------------------
    def right_click(self):
        pyautogui.click(button="right", _pause=False)

    # --------------------------------------------------
    # Scroll
    # --------------------------------------------------
    def scroll(self, amount):
        pyautogui.scroll(int(amount), _pause=False)

    # --------------------------------------------------
    # Zoom
    # --------------------------------------------------
    def zoom(self, amount):
        pyautogui.keyDown("ctrl")
        pyautogui.scroll(int(amount), _pause=False)
        pyautogui.keyUp("ctrl")