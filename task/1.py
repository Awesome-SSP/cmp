# 1. Open Google and search for 'Robocorp'. Print the title of the first result.
from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def search_google():
    browser.open_available_browser("https://www.google.com")

    # Accept cookies if shown (for EU/UK)
    try:
        browser.click_element("xpath://button[.='I agree' or .='Accept all']")
    except:
        pass  # Continue if not shown

    # Type 'Robocorp' into search box
    browser.input_text("name:q", "Robocorp")
    browser.press_keys("name:q", "ENTER")

    time.sleep(2)  # wait for results to load

    # Get title of the first search result
    title = browser.get_text("xpath=(//h3)[1]")
    print("Title of the first result:", title)

    browser.close_browser()

search_google()
