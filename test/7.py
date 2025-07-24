# Extract the URLs of all images from a webpage and print them.


from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def extract_image_urls():
    # 1. Open the webpage
    browser.open_available_browser("https://www.wikipedia.org")

    # 2. Wait for images to load
    browser.wait_until_element_is_visible("tag:img", timeout=10)

    # 3. Find all <img> elements
    image_elements = browser.find_elements("tag:img")

    print(f"Found {len(image_elements)} images.\n")

    # 4. Extract and print their src URLs
    for i, img in enumerate(image_elements, start=1):
        src = img.get_attribute("src")
        if src:
            print(f"{i}. {src}")

    time.sleep(1)
    browser.close_browser()

extract_image_urls()
