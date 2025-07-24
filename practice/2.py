from RPA.Browser.Selenium import Selenium
browser = Selenium()

try:
    browser.open_available_browser()
    browser.input_text("input=q","hello")
except Exception as e:
    print("hello There is an error ", e)
    