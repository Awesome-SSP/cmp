from RPA.Browser.Selenium import Selenium
import time

# Initialize browser instance
browser = Selenium()

from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def login_to_outlook_web(email, password):
    try:
        browser.open_available_browser("https://outlook.office.com/mail/")
        browser.wait_until_element_is_visible("id=i0116", timeout=20)
        browser.input_text("id=i0116", email)
        browser.click_button("id=idSIButton9")  # Next (Email input)
        time.sleep(2)

        browser.wait_until_element_is_visible("id=i0118", timeout=20)
        browser.input_text("id=i0118", password)
        browser.click_button("id=idSIButton9")  # Sign in
        time.sleep(3)

        # Optional MFA or redirect screen (handle if it exists)
        if browser.does_page_contain_element("id=idSubmit_ProofUp_Redirect"):
            browser.click_button("id=idSubmit_ProofUp_Redirect")
            time.sleep(2)

        # Optional "Skip Setup" or "Stay Signed In?" screen
        if browser.does_page_contain_element("id=idSIButton9"):
            browser.click_button("id=idSIButton9")  # Stay signed in? -> Yes
            time.sleep(2)

        # Optional skip setup screen (dynamic class name sometimes used)
        skip_button_locator = "xpath=//button[contains(text(), 'Skip') or contains(text(), 'Skip setup')]"
        if browser.does_page_contain_element(skip_button_locator):
            browser.click_element(skip_button_locator)
            time.sleep(2)

        # Final wait for inbox to load
        browser.wait_until_page_contains("Inbox", timeout=15)
        print("✅ Successfully logged into Outlook Inbox.")

    except Exception as e:
        print(f"❌ Failed to login: {e}")

def fetch_emails_from_web():
    try:
        # Wait for inbox to load
        browser.wait_until_element_is_visible("//div[@role='main']", timeout=20)
        print("📬 Inbox loaded.")

        # Sample: Read top email subject and body preview
        emails = browser.find_elements("//div[@role='option']")
        for index, email in enumerate(emails[:5]):
            try:
                subject = browser.get_text(f"(//div[@role='option'])[{index+1}]//span[contains(@class, 'subject')]")
                preview = browser.get_text(f"(//div[@role='option'])[{index+1}]//span[contains(@class, 'preview')]")
                print(f"📧 Subject: {subject}")
                print(f"   Preview: {preview}")
            except Exception as e:
                print(f"❗ Error reading email {index+1}: {e}")

    except Exception as e:
        print(f"❌ Error fetching emails: {e}")

# Example usage
email = ""
password = ""

login_to_outlook_web(email, password)
fetch_emails_from_web()
browser.close_browser()
