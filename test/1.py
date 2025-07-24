# Check if a specific element exists on the page and print appropriate message.

from RPA.Browser.Selenium import Selenium

browser = Selenium()

def check_element():
    browser.open_available_browser("https://www.google.com")

    try:
        if browser.does_page_contain_element("name:q"):
            print("✅ Search box exists on the page.")
        else:
            print("❌ Search box not found.")
    except Exception as e:
        print("⚠️ Error while checking element:", str(e))
    finally:
        browser.close_browser()

check_element()
