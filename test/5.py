# Scroll down the page until a specific element becomes visible.



from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def scroll_until_element_visible():
    # 1. Open the infinite scroll demo page
    browser.open_available_browser("https://the-internet.herokuapp.com/infinite_scroll")

    # 2. Try to scroll until the 3rd new content block is visible
    for i in range(10):  # max attempts
        try:
            # Try to find and scroll to the 3rd scroll-loaded block
            element = browser.find_element("xpath:(//div[@class='jscroll-added'])[3]")
            browser.scroll_element_into_view(element)
            print("✅ Element is now visible.")
            break
        except:
            # Scroll down a bit
            browser.execute_javascript("window.scrollBy(0, 1000);")
            time.sleep(1)

    browser.close_browser()

scroll_until_element_visible()
