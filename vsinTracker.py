import time
import pymongo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo.server_api import ServerApi

#Sets up driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('')

client = pymongo.MongoClient("mongodb+srv://nickvirzi:%23Supreme2525@cluster0.rlqm7dy.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test


mydb = client["mydatabase"]
mycol = mydb["customers"]
mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)
mydict = { "name": "Peter", "address": "Lowstreet 27" }

x = mycol.insert_one(mydict)

print(x.inserted_id)

#time.sleep(15)