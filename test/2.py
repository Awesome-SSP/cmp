# Login to a test portal and navigate to a second page.


from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def login_and_navigate():
    # 1. Open the login page
    browser.open_available_browser("https://the-internet.herokuapp.com/login")

    # 2. Enter credentials
    browser.input_text("id:username", "tomsmith")
    browser.input_text("id:password", "SuperSecretPassword!")

    # 3. Click the login button
    browser.click_button("xpath://button[@type='submit']")

    # 4. Wait for navigation and confirm login
    browser.wait_until_element_is_visible("id:flash", timeout=5)
    flash_msg = browser.get_text("id:flash")
    print("Login message:", flash_msg.strip())

    # 5. Navigate to a second page (e.g., Secure File Download page)
    browser.go_to("https://the-internet.herokuapp.com/download")
    print("Navigated to file download page.")

    # Optional: Print a heading from the new page
    heading = browser.get_text("xpath://h3")
    print("Second page heading:", heading)

    # 6. Close browser
    time.sleep(2)
    browser.close_browser()

login_and_navigate()
