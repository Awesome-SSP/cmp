from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
import time

browser = Selenium()
fs = FileSystem()

# Task 1: Open Google and search for 'Robocorp'. Print the title of the first result.
browser.open_available_browser("https://www.google.com")
# browser.input_text("name:q", "Robocorp")
# browser.press_keys("name:q", "ENTER")
# browser.wait_until_element_is_visible("css:h3", timeout=10)
# first_result_title = browser.get_text("css:h3")
# print("First result title:", first_result_title)

# Task 2: Login to a dummy website
browser.go_to("https://the-internet.herokuapp.com/login")
browser.input_text("id:username", "tomsmith")
browser.input_text("id:password", "SuperSecretPassword!")
browser.click_button("css:button[type='submit']")
browser.wait_until_element_is_visible("id:flash", timeout=10)
print("Login Status:", browser.get_text("id:flash"))

# # Task 3: Open a news website and extract all headlines
# browser.go_to("https://www.bbc.com/news")
# browser.wait_until_element_is_visible("css:h3", timeout=10)
# headlines = browser.find_elements("css:h3")
# print("\nBBC Headlines:")
# for h in headlines[:10]:
#     print("-", h.text)

# # Task 4: Open a website, fill form with name/email/password, and submit
# browser.go_to("https://www.w3schools.com/howto/howto_css_signup_form.asp")
# browser.wait_until_element_is_visible("id:main", timeout=10)
# browser.execute_javascript("window.scrollBy(0, 600);")
# browser.input_text("xpath://input[@placeholder='Enter Email']", "test@example.com")
# browser.input_text("xpath://input[@placeholder='Enter Password']", "password123")
# browser.click_button("xpath://button[text()='Sign Up']")

# # Task 5: From dropdown, select value by visible text
# browser.go_to("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select")
# browser.wait_until_element_is_visible("id:iframeResult", timeout=10)
# browser.select_frame("id:iframeResult")
# browser.select_from_list_by_label("name:cars", "Saab")

# # Task 6: Take a screenshot after a page has fully loaded and save locally
# browser.unselect_frame()
# browser.go_to("https://www.python.org")
# browser.wait_until_element_is_visible("id:content", timeout=10)
# screenshot_path = "python_homepage.png"
# browser.capture_page_screenshot(screenshot_path)
# print("\nScreenshot saved at:", screenshot_path)

# # Task 7: Use wait_until_element_is_visible before interacting
# browser.go_to("https://the-internet.herokuapp.com/dynamic_loading/1")
# browser.click_button("css:#start button")
# browser.wait_until_element_is_visible("css:#finish h4", timeout=15)
# message = browser.get_text("css:#finish h4")
# print("Loaded Message:", message)

# # Close browser at end
browser.close_browser()
