import os
import re
import time
import subprocess
import win32com.client
import webbrowser
from datetime import datetime

# --- Constants ---
DESTINATION = r"C:\Users\vikra\Desktop\nishu"
OUTLOOK_PATH = r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"

# --- Ensure destination folder exists ---
if not os.path.exists(DESTINATION):
    os.makedirs(DESTINATION)

# --- Launch Outlook if not running ---
def open_outlook():
    try:
        win32com.client.GetActiveObject("Outlook.Application")
        print("✅ Outlook already running.")
    except:
        print("📨 Outlook not running. Launching...")
        try:
            subprocess.Popen([OUTLOOK_PATH])
            print("⏳ Waiting for Outlook to launch...")
            for i in range(60):
                try:
                    win32com.client.GetActiveObject("Outlook.Application")
                    print(f"✅ Outlook ready after {i+1} seconds.")
                    return True
                except:
                    time.sleep(1)
            print("❌ Outlook did not become available in time.")
            return False
        except Exception as e:
            print(f"❌ Failed to launch Outlook: {e}")
            return False
    return True

# --- Extract all URLs ---
def extract_urls(text):
    return re.findall(r"https?://[^\s<>\"']+", text)

# --- Open file or URL in default browser ---
def open_in_browser(path_or_url):
    try:
        print(f"🌐 Opening in browser: {path_or_url}")
        webbrowser.open(path_or_url)
    except Exception as e:
        print(f"❌ Failed to open in browser: {e}")

# --- Process all unread emails ---
def process_all_unread_emails():
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox
        messages = inbox.Items
        unread_emails = messages.Restrict("[Unread] = true")
        unread_emails.Sort("[ReceivedTime]", True)

        total_processed = 0
        print("📥 Checking unread emails...\n")

        for msg in unread_emails:
            try:
                subject = msg.Subject
                body = msg.Body
                received = msg.ReceivedTime
                attachments = msg.Attachments

                print(f"📨 Email: {subject} ({received})")

                urls = extract_urls(body)
                saved_pdfs = []

                # Save PDF attachments
                for i in range(1, attachments.Count + 1):
                    attachment = attachments.Item(i)
                    if attachment.FileName.lower().endswith(".pdf"):
                        filepath = os.path.join(DESTINATION, attachment.FileName)
                        attachment.SaveAsFile(filepath)
                        saved_pdfs.append(filepath)
                        print(f"📎 Saved PDF: {filepath}")

                # Mark email as read
                msg.Unread = False
                msg.Save()

                # Open all found links
                for url in urls:
                    open_in_browser(url)

                # Open all saved PDFs
                for pdf in saved_pdfs:
                    open_in_browser(f"file:///{pdf}")

                total_processed += 1
                print("✅ Email processed.\n")

            except Exception as e:
                print(f"⚠ Error processing email: {e}\n")

        if total_processed == 0:
            print("❌ No unread emails found with URLs or PDFs.")
        else:
            print(f"🎉 Processed {total_processed} unread email(s).")

    except Exception as e:
        print(f"❌ Outlook MAPI error: {e}")

# --- MAIN ---
if _name_ == "_main_":
    print("🚀 Script started at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if open_outlook():
        process_all_unread_emails()
    else:
        print("🛑 Could not start Outlook.")