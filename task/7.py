# 7. Use wait_until_element_is_visible() to wait for an element before interacting


from RPA.Browser.Selenium import Selenium

browser = Selenium()

def wait_and_interact():
    # 1. Open the dynamic loading page
    browser.open_available_browser("https://the-internet.herokuapp.com/dynamic_loading/1")

    # 2. Click the "Start" button to begin loading
    browser.click_button("css:#start button")

    # 3. Wait until the hidden text appears
    browser.wait_until_element_is_visible("id:finish", timeout=10)

    # 4. Get and print the text
    text = browser.get_text("id:finish")
    print("Loaded text:", text)

    # 5. Close the browser
    browser.close_browser()

wait_and_interact()

