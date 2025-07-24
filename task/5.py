# 5. From a dropdown, select a value by visible text.

from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def select_from_dropdown():
    # 1. Open the dropdown demo site
    browser.open_available_browser("https://www.seleniumeasy.com/test/basic-select-dropdown-demo.html")

    # 2. Select "Wednesday" from the dropdown by visible text
    browser.select_from_list_by_label("id:select-demo", "Wednesday")

    time.sleep(2)

    # 3. (Optional) Print selected message
    result = browser.get_text("class:selected-value")
    print("Selected result message:", result)

    # 4. Close browser
    browser.close_browser()

select_from_dropdown()
