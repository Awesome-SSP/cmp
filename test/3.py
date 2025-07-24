# Handle an alert pop-up using Selenium.

from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import NoAlertPresentException
import time

browser = Selenium()

def handle_alert():
    # 1. Open the alert demo page
    browser.open_available_browser("https://the-internet.herokuapp.com/javascript_alerts")

    # 2. Click the button to trigger alert
    browser.click_button("xpath://button[text()='Click for JS Alert']")
    
    # 3. Wait and switch to alert
    try:
        alert = browser.driver.switch_to.alert
        print("⚠️ Alert text:", alert.text)

        # 4. Accept the alert
        alert.accept()
        print("✅ Alert accepted.")
    except NoAlertPresentException:
        print("❌ No alert present.")

    # 5. Get result message
    result = browser.get_text("id:result")
    print("📝 Result message:", result)

    time.sleep(1)
    browser.close_browser()

handle_alert()
