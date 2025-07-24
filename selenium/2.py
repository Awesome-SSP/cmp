from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# chrome_driver_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # e.g., "C:/chromedriver.exe"

options = Options()
options.add_argument("--start-maximized")  # Opens Chrome in maximized mode
options.add_argument("--headless")  # Uncomment to run without GUI


# service = Service(chrome_driver_path)
driver = webdriver.Chrome(options=options)

# Open a website
driver.get("https://www.google.com/search?q=image&oq=image&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIOCAEQRRgnGDsYgAQYigUyDAgCECMYJxiABBiKBTIKCAMQABixAxiABDIKCAQQABixAxiABDIKCAUQABixAxiABDIHCAYQABiABDIKCAcQABixAxiABDIKCAgQABixAxiABDINCAkQABiDARixAxiABNIBCTQxMDlqMGoxNagCCLACAfEFDan5l9RvtUfxBQ2p-ZfUb7VH&sourceid=chrome&ie=UTF-8")

results = driver.find_elements(By.CSS_SELECTOR, 'h3')

print("🔍 Top Search Results:")

for index, result in enumerate(results[:5]):
    print(f"{index + 1}. {result.text}")

time.sleep(5)
driver.quit()
