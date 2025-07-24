from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

try:
    # Open Google search page with a query for "chatgpt"
    url = "https://www.google.com/search?q=chatgpt"
    browser.open_available_browser(url)

    # Try clicking the "Accept all cookies" button if it appears
    cookie_accept_xpath = (
        "xpath://*[contains(concat(' ', @class, ' '), ' DKV0Md ')] "
        "| //*[contains(concat(' ', @class, ' '), ' gb_Za ')]"
    )
    browser.wait_until_element_is_visible(cookie_accept_xpath, timeout=5)
    browser.click_element(cookie_accept_xpath)
    # browser.capture_page_screenshot("screenshot")

except Exception as e:
    print("Cookie banner not found or another error:", e)

# Add a wait to observe the result (optional)
time.sleep(3)

# Close the browser (optional for cleanup)
browser.close_browser()
