# automate_gui.py

import pyautogui
import time
import subprocess
import pygetwindow as gw

# Start the GUI app
subprocess.Popen(["python", r"C:\Users\GAURAV\Desktop\cmp-main\windowAutomation\app_gui.py"])

# Wait for GUI to load
time.sleep(3)

# Focus the GUI window (adjust title if needed)
window = None
for win in gw.getWindowsWithTitle("Input & Dropdown Example"):
    if win.isActive == False:
        win.activate()
        window = win
        break

time.sleep(1)

# Coordinates will vary by screen size & OS!
# You may need to adjust them slightly using pyautogui.position()
pyautogui.click(374, 425)  # Click on Entry box
pyautogui.write("John Doe", interval=0.05)

pyautogui.click(484, 513)  # Click on dropdown
time.sleep(0.5)
pyautogui.press("down")   # Navigate to Option 2
pyautogui.press("enter")
time.sleep(2)
pyautogui.click(390, 579) 
pyautogui.press("submit")
time.sleep(2)
pyautogui.click(1039, 668) 
pyautogui.press("okay")
time.sleep(2)


pyautogui.screenshot("filled_form.png")
print("Screenshot saved as filled_form.png")

pyautogui.click(582, 330) 
pyautogui.press("cancle")

# Wait a bit and take screenshot
time.sleep(1)


