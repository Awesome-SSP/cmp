# Example usage in Python
from RPA.Browser.Selenium import Selenium

bot = Selenium()
bot.open_available_browser("https://google.com")
bot.input_text("name=q", "Robocorp Python RPA")
bot.press_keys("name=q", "ENTER")
bot.capture_page_screenshot("screenshot.png")

bot.close_browser()