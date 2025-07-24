# Use a dynamic XPath to click the last item in a product list.


from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()

def click_last_product():
    # 1. Open the product list page
    browser.open_available_browser("https://automationexercise.com/products")

    # 2. Wait for product grid to be visible
    browser.wait_until_element_is_visible("xpath://div[@class='features_items']", timeout=10)

    # 3. Scroll to the bottom (to ensure all products are loaded)
    browser.execute_javascript("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # 4. Click the last product's "View Product" link using dynamic XPath
    last_product_xpath = "(//a[contains(text(),'View Product')])[last()]"
    browser.click_element(last_product_xpath)

    print("✅ Clicked the last product in the list.")

    time.sleep(2)
    browser.close_browser()

click_last_product()
