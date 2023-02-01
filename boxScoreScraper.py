import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo.server_api import ServerApi
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# This was needed to make the mongo work LOCAL OR DEPLOYED, idk why
import certifi
ca = certifi.where()
#

#Notes-------------------------------------------------------------------------------------------------
# - Use bball ref to load player stats, sort all player this year on min per game in stats on season page could store this and update daily approx 400 players maybe too much
# - Maybe as I add box score data I can add a matchup tab and track their recent matchups to get avgs over last x games
# - https://www.basketball-reference.com/leagues/NBA_2023_per_game.html


#Sets up driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.espn.com/')
driver.maximize_window()

#Sets up current time and date formatting
now = datetime.now()
#now += timedelta(hours=-12) #Not needed on local
currentTimeMilitary = now.strftime("%H:%M")
currentTimeStandard = datetime.strptime(currentTimeMilitary, "%H:%M")
displayTime = currentTimeStandard.strftime("%r")
timeModifer = displayTime[-2:]
displayTime = displayTime[:-6]
date = now.strftime("%m/%d")
tempDate = date.split('/')

if tempDate[0][0] == '0': date = date.replace('0', '', 1)
if tempDate[1][0] == '0': date = date.replace('0', '')
if displayTime[0] == '0': displayTime = displayTime.replace('0', '', 1)

#################################################################################################################################################
### Everything below this line can be sync'd with the other form to work the same apart from web driver behavior ###

#Connects to mongo and sets up collections and databases
#Alternative second argument is: "server_api=ServerApi('1')" hand in hand with the certify
client = pymongo.MongoClient("mongodb+srv://nickvirzi:sbsa@cluster0.rlqm7dy.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
vsinDailyTrackerDatabase = client["VSINDailyTrackerDB"]
vsinTrendTrackerDatabase = client["VSINTrendTrackerDB"]

#Create month dictionary
monthIntStringDict = {
    'January': '1', 'February': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6', 'July': '7', 'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12'
}

dbLeagueToESPNLeague = {
    'CBB': 'mens-college-basketball', 'CFB': 'college-football', 'NBA': 'nba', 'NFL': 'nfl', 'NHL': 'nhl'
}

#Input month string for month date as a string
def getMonthIntString(month):
    monthIntString = monthIntStringDict[month]
    return monthIntString

#Input month string for month date as a string
def getESPNMonthFromDB(dbLeague):
    espnLeague = dbLeagueToESPNLeague[dbLeague]
    return espnLeague

# def get lerague box
    # load league url


# Begin Main

# league arr = [ leagues to load]
# Get box score for league (league)