# 3. Open a news website and extract all headlines.
from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def extract_headlines():
    browser.open_available_browser("https://www.bbc.com")

    time.sleep(2)  # wait for page to load

    # Get all headline elements
    headline_elements = browser.find_elements("xpath://h3")

    print("Top Headlines:\n")
    for i, headline in enumerate(headline_elements, start=1):
        text = headline.text.strip()
        if text:  # filter out empty headlines
            print(f"{i}. {text}")

    browser.close_browser()

extract_headlines()
