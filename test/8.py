# Automate downloading a file from a page and verify it was saved


from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
import os
import time

browser = Selenium()
fs = FileSystem()

def download_and_verify_file():
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # Configure browser profile for auto-download
    options = {
        "prefs": {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
    }

    browser.open_chrome_browser("https://file-examples.com/index.php/sample-documents-download/sample-pdf-download/", options=options)

    # Wait until link is clickable and click first download link
    browser.wait_until_element_is_visible("xpath://a[contains(text(),'Download sample pdf file')]", timeout=15)
    browser.click_element("xpath:(//a[contains(text(),'Download sample pdf file')])[1]")

    print("Download started...")

    # Wait for download to complete
    time.sleep(5)  # You can implement a loop to wait for *.crdownload to disappear

    # Check if PDF file exists
    files = fs.find_files(download_dir, "*.pdf")
    if files:
        print(f"Download successful! File saved at: {files[0]}")
    else:
        print("Download failed or file not found.")

    browser.close_browser()

download_and_verify_file()
