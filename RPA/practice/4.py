from robocorp.tasks import task
from robocorp import browser


@task
def minimal_task():
    message = "Hello"
    message = message + " World!"
    print(message)
def open_browser(url):
    page = browser.goto(url)
    page.screenshot(path="screenshot.png")
    
if __name__ == '__main__':
    minimal_task()
    url = "https://robotsparebinindustries.com/"
    open_browser(url)