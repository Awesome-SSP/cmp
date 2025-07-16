from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
import os

browser = Selenium()
http = HTTP()

def scrape_images(url, download_folder="images"):
    browser.open_available_browser(url)
    
    # Create folder to store images
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Find all image elements
    img_elements = browser.find_elements("tag:img")
    print(f"Found {len(img_elements)} images.")

    count = 1
    for img in img_elements:
        src = img.get_attribute("src")
        if src and src.startswith("http"):
            try:
                filename = os.path.join(download_folder, f"image_{count}.jpg")
                http.download(url=src, target_file=filename, overwrite=True)
                print(f"Downloaded: {filename}")
                count += 1
            except Exception as e:
                print(f"Failed to download {src}: {e}")

    browser.close_browser()

if __name__ == "__main__":
    url = "https://unsplash.com/s/photos"
