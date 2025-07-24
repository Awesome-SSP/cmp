import tkinter as tk
from tkinter import scrolledtext
from RPA.Browser.Selenium import Selenium

browser = Selenium()

# ---------- Automation Functions ----------
def log(msg):
    output_box.insert(tk.END, f"{msg}\n")
    output_box.see(tk.END)

def search_google():
    try:
        browser.open_chrome_browser("https://www.google.com")
        browser.input_text("name=q", "Robocorp")
        browser.press_keys("name=q", "ENTER")
        browser.wait_until_element_is_visible("css=h3", timeout=10)
        title = browser.get_text("css=h3")
        log(f"✅ Google Result Title: {title}")
    except Exception as e:
        log(f"❌ Error: {e}")

def login_website():
    
    try:
        browser.go_to("https://the-internet.herokuapp.com/login")
        browser.input_text("id=username", "tomsmith")
        browser.input_text("id=password", "SuperSecretPassword!")
        browser.click_element("css=button.radius")
        browser.wait_until_element_is_visible("css=div.flash.success", timeout=10)
        log("✅ Login successful!")
    except Exception as e:
        log(f"❌ Error: {e}")

def extract_headlines():
    try:
        browser.go_to("https://www.bbc.com/news")
        browser.wait_until_element_is_visible("css=h3", timeout=10)
        headlines = browser.find_elements("css=h3")
        log("✅ Top Headlines:")
        for h in headlines[:5]:
            log(f" • {h.text}")
    except Exception as e:
        log(f"❌ Error: {e}")

def fill_form():
    try:
        browser.go_to("https://www.w3schools.com/html/html_forms.asp")
        browser.input_text('xpath=//input[@name="firstname"]', "John")
        browser.input_text('xpath=//input[@name="lastname"]', "Doe")
        log("✅ Form filled with dummy data.")
    except Exception as e:
        log(f"❌ Error: {e}")

def dropdown_select():
    try:
        browser.go_to("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select")
        browser.wait_until_element_is_visible("id=iframeResult", timeout=10)
        browser.switch_frame("id=iframeResult")
        browser.select_from_list_by_label("tag=select", "Volvo")
        log("✅ 'Volvo' selected from dropdown.")
    except Exception as e:
        log(f"❌ Error: {e}")

def take_screenshot():
    try:
        browser.go_to("https://hello.com")
        browser.wait_until_element_is_visible("tag=h1", timeout=10)
        browser.capture_page_screenshot("example_screenshot.png")
        log("✅ Screenshot saved: example_screenshot.png")
    except Exception as e:
        log(f"❌ Error: {e}")

def wait_and_click():
    try:
        browser.go_to("https://the-internet.herokuapp.com/dynamic_loading/1")
        browser.click_element("css=#start button")
        browser.wait_until_element_is_visible("css=#finish h4", timeout=10)
        result = browser.get_text("css=#finish h4")
        log(f"✅ Loaded content: {result}")
    except Exception as e:
        log(f"❌ Error: {e}")

def close_browser():
    browser.close_all_browsers()
    log("🛑 Browser closed.")
# ---------- GUI Function ----------
def handle_search():
    query = entry.get()
    if not query:
        messagebox.showwarning("Input Required", "Please enter a keyword to search.")
        return
    result = search_google(query)
    output_label.config(text=result)

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("RPA Desktop GUI")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=10)

buttons = [
    ("Search Google", search_google),
    ("Login to Site", login_website),
    ("Get Headlines", extract_headlines),
    ("Fill Form", fill_form),
    ("Select Dropdown", dropdown_select),
    ("Take Screenshot", take_screenshot),
    ("Wait & Click", wait_and_click),
    ("Close Browser", close_browser),
]

for (text, command) in buttons:
    tk.Button(frame, text=text, width=20, command=command).pack(pady=3)
    
    
tk.Label(root, text="Enter search keyword:").pack(pady=10)
entry = tk.Entry(root, width=40, font=('Arial', 12))
entry.pack()
# Submit Button
tk.Button(root, text="Search Google", command=handle_search, bg="blue", fg="white", padx=10, pady=5).pack(pady=15)


output_box = scrolledtext.ScrolledText(root, height=15, width=70)
output_box.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", close_browser)
root.mainloop()
