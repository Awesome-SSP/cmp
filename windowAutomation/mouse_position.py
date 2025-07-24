# get_mouse_position.py

import pyautogui
import time

print("Move your mouse to the desired location...")

for _ in range(50):
    x, y = pyautogui.position()
    print(f"Position: {x}, {y}")
    time.sleep(1)
