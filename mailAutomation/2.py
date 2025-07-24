import os

import win32com.client

 

# === CONFIGURATION ===

DOWNLOAD_FOLDER = r"C:\Users\GAURAV\Desktop\cmp-main\mailAutomation" 

 

def ensure_download_folder():

    if not os.path.exists(DOWNLOAD_FOLDER):

        os.makedirs(DOWNLOAD_FOLDER)

 

def mark_and_download():

    try:

        ensure_download_folder()

 

        print("Connecting to Outlook...")

        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        inbox = outlook.GetDefaultFolder(6)

 

        # Filter unread messages

        messages = inbox.Items

        unread_messages = messages.Restrict("[Unread]=True")

        count = unread_messages.Count

 

        if count == 0:

            print("No unread emails found.")

            return

 

        print(f"Found {count} unread email(s).")

 

        for message in unread_messages:

            try:

                subject = message.Subject

                sender = message.SenderName

                print(f"\n Processing: '{subject}' from {sender}")

 

                # === Download Attachments ===

                attachments = message.Attachments

                if attachments.Count == 0:

                    print("No attachments found in this email.")

                else:

                    for i in range(1, attachments.Count + 1):

                        attachment = attachments.Item(i)

                        filename = attachment.FileName

 

                        # Ensure unique filename

                        save_path = os.path.join(DOWNLOAD_FOLDER, filename)

                        base, ext = os.path.splitext(save_path)

                        counter = 1

                        while os.path.exists(save_path):

                            save_path = f"{base}_{counter}{ext}"

                            counter += 1

 

                        attachment.SaveAsFile(save_path)

                        print(f"Attachment saved: {save_path}")

 

                # === Mark as read ===

                message.Unread = False

                message.Save()

 

            except Exception as msg_error:

                print(f"Error processing this message: {msg_error}")

 

        print("\n Finished: All unread emails processed.")

 

    except Exception as e:

        print("General Error:", str(e))

 

# Run the function

mark_and_download()