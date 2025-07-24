# 2. Login to a dummy website (https://the-internet.herokuapp.com/login).
from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def login_dummy_site():
    # 1. Open the dummy login page
    browser.open_available_browser("https://the-internet.herokuapp.com/login")

    # 2. Input username and password
    browser.input_text("id:username", "tomsmith")
    browser.input_text("id:password", "SuperSecretPassword!")

    # 3. Click Login button
    browser.click_button("xpath://button[@type='submit']")

    time.sleep(2)  # wait for the page to load

    # 4. Validate login success
    message = browser.get_text("id:flash")
    print("Login message:", message.strip())

    # 5. Optional: Logout
    browser.click_link("Logout")

    browser.close_browser()

login_dummy_site()
