from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=100,
    )
    open_the_intranet_website()
    log_in()
    download_excel_file()
    fill_and_submit_sales_form()
    

def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/")

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    page = browser.page()
    page.fill("#username", "maria")
    print("-----")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")
    page.screenshot(path="screenshot1.png")
    
def download_excel_file():
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)
    
def fill_and_submit_sales_form():
    """Fills in the sales data and click the 'Submit' button"""
    page = browser.page()

    page.fill("#firstname", "John")
    page.fill("#lastname", "Smith")
    page.fill("#salesresult", "123")
    page.select_option("#salestarget", "10000")
    page.click("text=Submit")
    
def fill_form_with_excel_data():
    """Read data from excel and fill in the sales form"""
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet = excel.read_worksheet_as_table("data", header=True)
    for i in worksheet:
        print(i)
    print(worksheet[::1][::])
    excel.close_workbook()
    
if __name__ == "__main__":
    robot_spare_bin_python()
    # fill_form_with_excel_data()
    # open_the_intranet_website()