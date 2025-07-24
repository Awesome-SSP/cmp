# Switch to a second browser tab and extract a piece of information.

from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def switch_tab_and_extract():
    # 1. Open the first website
    browser.open_available_browser("https://example.com")
    print("✅ Opened first tab:", browser.get_title())

    # 2. Open a second tab with a new website
    browser.execute_javascript("window.open('https://www.wikipedia.org', '_blank');")

    # 3. Get all open window handles (tabs)
    tabs = browser.driver.window_handles

    # 4. Switch to second tab
    browser.driver.switch_to.window(tabs[1])
    print("➡️ Switched to second tab:", browser.get_title())

    # 5. Extract heading text from Wikipedia
    heading = browser.get_text("xpath://h1")
    print("📝 Heading on Wikipedia:", heading)

    time.sleep(1)

    # 6. Close browser
    browser.close_browser()

switch_tab_and_extract()
