from RPA.Desktop import Desktop
from RPA.FileSystem import FileSystem
import os
import time

desktop = Desktop()
fs = FileSystem()

def open_notepad():
    print("[✓] Opening Notepad")
    time.sleep(2)
    desktop.open_application("notepad.exe")
    time.sleep(2)  # wait for the app to open

def type_message():
    print("[✓] Typing message...")
    message = "Hello Saurabh,\nThis message is typed using RPA.Desktop automation.\n\n- ChatGPT Bot"
    msg = '''Technology has transformed the way we live, work, and communicate.\n
From smartphones and artificial intelligence to cloud computing and robotics, innovation continues to reshape industries and daily life.\n
It has made information more accessible, improved healthcare, enhanced education, and opened up new possibilities for businesses.\n
However, this rapid advancement also brings challenges such as data privacy concerns, job displacement, and the digital divide.\n
As we move forward, it is crucial to balance technological progress with ethical responsibility to ensure a more inclusive and sustainable future for all.
'''
    time.sleep(2)
    desktop.press_keys("ctrl", "a")
    desktop.press_keys("backspace")
    for char in msg:
        desktop.type_text(char)
        time.sleep(0.001)
    # desktop.type_text(msg)   
    time.sleep(20)
    

def save_file():
    print("[✓] Saving file...")
    desktop.press_keys("ctrl", "s")
    time.sleep(1)

    # Save to Desktop
    filename = "RPA_Desktop_Message.txt"
    filepath = os.path.join(r"C:\Users\GAURAV\Desktop\cmp-main\rpaDesktop", filename)

    desktop.type_text(filepath)
    desktop.press_keys("enter")
    time.sleep(1)

    if fs.does_file_exist(filepath):
        print(f"[✓] File saved at: {filepath}")
    else:
        print("[✗] Failed to save file!")

def close_notepad():
    time.sleep(4)
    print("[✓] Closing Notepad...")
    desktop.press_keys("alt", "f4")

def main():
    open_notepad()
    type_message()
    save_file()
    close_notepad()

if __name__ == "__main__":
    main()
