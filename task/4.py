# 4. Open a website, fill a form with name/email/password, and click submit.

from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def fill_form_and_submit():
    # 1. Open form demo site
    browser.open_available_browser("https://www.seleniumeasy.com/test/input-form-demo.html")

    # Wait to ensure form loads
    time.sleep(2)

    # 2. Fill in name, email, and password-like fields
    browser.input_text("name:first_name", "John")
    browser.input_text("name:last_name", "Doe")
    browser.input_text("name:email", "john.doe@example.com")
    browser.input_text("name:phone", "1234567890")
    browser.input_text("name:address", "123 Main St")
    browser.input_text("name:city", "New York")
    browser.select_from_list_by_value("name:state", "New York")
    browser.input_text("name:zip", "10001")
    browser.input_text("name:website", "www.johndoe.com")

    # Select "Yes" for hosting
    browser.click_element("xpath://input[@value='yes']")

    # Input a project description
    browser.input_text("name:comment", "This is a test project.")

    # 3. Click Submit button
    browser.click_button("xpath://button[@type='submit']")

    # 4. Wait and close
    time.sleep(3)
    browser.close_browser()

fill_form_and_submit()
