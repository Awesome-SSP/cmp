from RPA.Desktop import Desktop
import sys
import time
import pyautogui  # used just for taking screenshot

desktop = Desktop()

def open_calculator():
    print("Opening Calculator...")
    desktop.open_application("calc.exe")
    time.sleep(2)

def perform_calculation(expression):
    print(f"Performing: {expression}")
    desktop.type_text(expression)
    time.sleep(0.5)
    desktop.press_keys("enter")

def capture_screenshot(filename="calculator_result.png"):
    print(f"Capturing screenshot as {filename}")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

def main():
    if len(sys.argv) != 2:
        print("❌ Usage: python rpa_calculator.py \"7+3\"")
        return

    expression = sys.argv[1]
    if not any(op in expression for op in "+-*/"):
        print("❌ Please provide a valid expression like 7+3 or 9*2")
        return

    open_calculator()
    perform_calculation(expression)
    time.sleep(1)
    capture_screenshot()

if __name__ == "__main__":
    main()
