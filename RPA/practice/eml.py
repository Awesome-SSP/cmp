from RPA.Robocorp.Vault import Vault
from RPA.Email.ImapSmtp import ImapSmtp

email = ImapSmtp()

def read_emails():
    email.authorize(
        account="your_email@example.com",
        password="your_password",
        smtp_server="smtp.example.com",
        smtp_port=587,
        imap_server="imap.example.com",
        imap_port=993,
    )

    email.list_messages()
    messages = email.get_messages()
    for msg in messages:
        print(f"From: {msg["From"]}")
        print(f"Subject: {msg["Subject"]}")
        print(f"Body:\n{msg["Body"]}")
    email.close_connection()


secrets = Vault.get_secret("email-credentials")


email.authorize(
    account=secrets["email"],
    password=secrets["password"],
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    imap_server="imap.gmail.com",
    imap_port=993,
)


def send_email():
    email.authorize(
        account="your_email@example.com",
        password="your_password",
        smtp_server="smtp.example.com",
        smtp_port=587,
        imap_server="imap.example.com",
        imap_port=993,
    )

    email.send_message(
        sender="your_email@example.com",
        recipients=["recipient@example.com"],
        subject="Test Email from RPA",
        body="Hello from Robocorp RPA Email Automation!",
    )
    email.close_connection()
