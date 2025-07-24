from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Optional: Set path to chromedriver if it's not in PATH
chrome_driver_path = "path/to/chromedriver"  # e.g., "C:/chromedriver.exe"

# Set up Chrome options (optional)
options = Options()
options.add_argument("--start-maximized")  # Opens Chrome in maximized mode
# options.add_argument("--headless")  # Uncomment to run without GUI

# Start the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open a website
driver.get("https://www.google.com")

# Wait a few seconds before closing
time.sleep(5)
driver.quit()
