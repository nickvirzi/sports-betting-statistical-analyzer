from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#Sets up driver
DRIVER_PATH = r'C:\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.espn.com/')
