from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Sets up driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('')