from robocorp import browser

def search_youtube(query):
    # Configure browser (optional slow motion to see actions)
    browser.configure(slowmo=100)

    # Open browser and go to YouTube
    page = browser.goto("https://www.youtube.com")

    # Wait for the search input to be ready
    page.wait_for_selector("input.ytSearchboxComponentInput.yt-searchbox-input.title")

    # Type the search query
    page.fill("input.ytSearchboxComponentInput.yt-searchbox-input.title", query)

    # Press Enter to search
    page.press("input.ytSearchboxComponentInput.yt-searchbox-input.title", "Enter")

    # Optionally: wait for results to load
    page.wait_for_selector("ytd-video-renderer", timeout=10000)

    # Screenshot or save something if needed
    page.screenshot(path="youtube_search_results.png")

if __name__ == "__main__":
    search_youtube("Python RPA Tutorial")
