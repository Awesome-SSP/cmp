from RPA.Browser.Selenium import Selenium
import time



browser = Selenium()

# Open browser
browser.open_available_browser("https://www.google.com/search?sca_esv=0f3f3d91d2ee70a0&sxsrf=AE3TifP8aqcOxbUjmsA65K4n5dOk9fz3vw:1752580991881&q=images&udm=2&fbs=AIIjpHxU7SXXniUZfeShr2fp4giZ1Y6MJ25_tmWITc7uy4KIeiAkWG4OlBE2zyCTMjPbGmMU8EWskMk2JSE__efdUJ3xRFvZ0M2vJLB0hUMk5HOE2OjlycQYRp9vQECfaBtuI77VBixuZT8Ikq7knPIraxtLcXUn-925YP4AZPohtCshEMzz_HYh-s2jy_GenEFZtSggFj5UruF1QvDnKbUPJW54S8V0hw&sa=X&ved=2ahUKEwjSgNj76L6OAxVUTWwGHT0UHYgQtKgLKAF6BAgSEAE&biw=1280&bih=632&dpr=1.5")
# a = browser.get_all_links('''https://www.google.com/search?sca_esv=0f3f3d91d2ee70a0&sxsrf=AE3TifP8aqcOxbUjmsA65K4n5dOk9fz3vw:1752580991881&q=images&udm=2&fbs=AIIjpHxU7SXXniUZfeShr2fp4giZ1Y6MJ25_tmWITc7uy4KIeiAkWG4OlBE2zyCTMjPbGmMU8EWskMk2JSE__efdUJ3xRFvZ0M2vJLB0hUMk5HOE2OjlycQYRp9vQECfaBtuI77VBixuZT8Ikq7knPIraxtLcXUn-925YP4AZPohtCshEMzz_HYh-s2jy_GenEFZtSggFj5UruF1QvDnKbUPJW54S8V0hw&sa=X&ved=2ahUKEwjSgNj76L6OAxVUTWwGHT0UHYgQtKgLKAF6BAgSEAE&biw=1280&bih=632&dpr=1.5''')
# print(a)
# Input and click
browser.input_text("name=search", "Robocorp")
browser.click_button("xpath=//button[@type='submit']")

time.sleep(5)

# Take screenshot
browser.capture_page_screenshot()


# Wait for 10 seconds so the user can see the result
time.sleep(10)

# Close the browser
browser.close_browser()
