import pyautogui


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        pyautogui.FAILSAFE = True

    def move(self, x, y, camera_width, camera_height):

        screen_x = int(
            (x / camera_width) * self.screen_width
        )

        screen_y = int(
            (y / camera_height) * self.screen_height
        )

        pyautogui.moveTo(screen_x, screen_y)

    def left_down(self):

        pyautogui.mouseDown()

    def left_up(self):

        pyautogui.mouseUp()