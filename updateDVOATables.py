import time
import pymongo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo.server_api import ServerApi

#Sets up driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.footballoutsiders.com/')

driver.maximize_window()
driver.find_element(By.XPATH, '//*[@id="block-usernavigation"]/a[2]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="edit-name"]').click() 
driver.find_element(By.XPATH, '//*[@id="edit-name"]').send_keys('virzinho')
driver.find_element(By.XPATH, '//*[@id="edit-pass"]').send_keys('#Supreme2525')
driver.find_element(By.XPATH, '//*[@id="edit-submit"]').click()