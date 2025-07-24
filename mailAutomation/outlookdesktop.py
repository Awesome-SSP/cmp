from RPA.Desktop import Desktop
from RPA.FileSystem import FileSystem
import os
import time
import pyperclip
# from RPA.Outlook.Application import Outlook
from RPA.Excel.Files import Files



# outlook = Outlook()
excel = Files()

desktop = Desktop()
fs = FileSystem()

def open_notepad():
    print("[✓] Opening OUTLOOK")
    time.sleep(2)
    desktop.open_application("olk.exe")
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
    print("[✓] Closing Outlook...")
    desktop.press_keys("alt", "f4")

# def main():
#     open_notepad()
#     # type_message()
#     # save_file()
#     close_notepad()



# def read_recent_emails():
#     print("[✓] Reading latest Outlook emails...")
#     outlook.open_application()
#     messages = outlook.get_messages(folder="Inbox", count=5)  # You can change count
#     for i, msg in enumerate(messages, 1):
#         print(f"\nEmail #{i}")
#         print(f"Subject: {msg['Subject']}")
#         print(f"From: {msg['Sender']}")
#         print(f"Body:\n{msg['Body'][:300]}...\n")  # First 300 characters only


def focus_outlook_window():
    print("[✓] Focusing Outlook window...")
    desktop.switch_window("Inbox")  # Works if the title includes "Inbox"
    time.sleep(1)
    


def get_clipboard_text(timeout=3):
    """Try reading from clipboard with retry logic."""
    for _ in range(timeout * 2):
        text = pyperclip.paste()
        if text.strip():
            return text
        time.sleep(0.5)
    return "[!] Clipboard empty or unreadable."


def read_email_using_ui():
    print("[✓] Reading top email using keyboard + clipboard...")

    # Step 1: Switch to Mail view
    desktop.press_keys("ctrl", "1")
    time.sleep(1)

    # Step 2: Select and open top email in new window
    desktop.press_keys("up")  # highlight
    desktop.press_keys("alt", "enter")  # open in new window
    time.sleep(2)

    # Step 3: Focus email body area (adjust coordinates if needed)
    desktop.click((772, 440))  # ✅ FIXED: use tuple
    time.sleep(0.5)

    # Step 4: Copy content
    desktop.press_keys("ctrl", "a")
    time.sleep(0.5)
    desktop.press_keys("ctrl", "c")
    time.sleep(1)

    # Step 5: Get clipboard data
    body = get_clipboard_text()
    print("📨 Email Content Preview:\n")
    print(body[:500])  # Print preview

    # Step 6: Close email window
    desktop.press_keys("esc")
    print("[✓] Finished reading email.\n")


def read_recipients_from_excel():
    print("[✓] Reading recipients from Excel...")
    filepath = os.path.join(os.path.expanduser("~"), "Desktop", "broadcast_list.xlsx")  # File must be placed here
    excel.open_workbook(filepath)
    excel.read_worksheet(name="Sheet1", header=True)
    data = excel.read_worksheet_as_table()
    recipients = [row["Email"] for row in data if "Email" in row and row["Email"]]
    excel.close_workbook()
    print(f"[✓] Found {len(recipients)} recipient(s).")
    return recipients

# def send_broadcast_email(recipients):
#     print("[✓] Sending broadcast email to all...")
#     subject = "🚀 Technology and the Future"
#     body = (
#         "Dear Subscriber,\n\n"
#         "Technology continues to reshape how we live, work, and communicate.\n"
#         "Stay updated with the latest insights and innovation.\n\n"
#         "Regards,\nRPA Bot"
#     )
#     for recipient in recipients:
#         print(f" → Sending to: {recipient}")
#         outlook.send_message(to=recipient, subject=subject, body=body)
#         time.sleep(1)

def main():
    open_notepad()
    # read_recent_emails()
    read_email_using_ui()
    # recipients = read_recipients_from_excel()
    # send_broadcast_email(recipients)
    close_notepad()


if __name__ == "__main__":
    main()





