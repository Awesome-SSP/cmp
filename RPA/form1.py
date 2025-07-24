from RPA.Browser.Selenium import Selenium
import time
browser = Selenium()

def search_google():
    try:
        browser.open_chrome_browser("https://docs.google.com/forms/d/e/1FAIpQLSdMaOnrfoUk8M_5eOM-NCSvBTcZxgeQ2HjNhr2ZEhMblwIY5g/viewform")
        time.sleep(5)
        browser.input_text('(//input[@type="text"])[1]', "saurabh")
     
        browser.input_text('(//input[@type="text"])[2]', "19")

        browser.input_text('(//input[@type="text"])[3]', "MALE")
        time.sleep(2)
        
        browser.click_element('//span[text()="Submit"]')
        time.sleep(5)
        browser.capture_page_screenshot("screen.png")
    except Exception as e:
        print("error")
        
def search():
    try:
        browser.open_chrome_browser("https://google.com/")
        time.sleep(1)
        browser.input_text('(//input[@type="text"]),"saurabh"')
        browser.capture_page_screenshot("screen.png")
    except Exception as e:
        print(e)
        
search()