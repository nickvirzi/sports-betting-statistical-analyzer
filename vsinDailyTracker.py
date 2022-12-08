import pymongo
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from pymongo.server_api import ServerApi
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = GOOGLE_CHROME_BIN
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

# #This script is design to capture the vsin data and send it to a database to be tracked and interpreted

# #Notes-------------------------------------------------------------------------------------------------
# # - All games upload with current date, needs to be its date, index through table looking for headers maybe?
# # - When clicking a different league header u gotta use full XPATH's bc they use active HTML switching
# # - Automate gathering all leagues

# #Sets up driver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.vsin.com/betting-resources/daily-betting-insights-for-mlb-nba-nhl/')
# driver.maximize_window()

# #Sets up current time and date formatting
# now = datetime.now()
# currentTimeMilitary = now.strftime("%H:%M")
# currentTimeStandard = datetime.strptime(currentTimeMilitary, "%H:%M")
# displayTime = currentTimeStandard.strftime("%r")
# date = now.strftime("%m/%d/%Y")

# #VSIN uses an IFrame which requires a switch to the frame
WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="main-content"]/div[2]/div[1]/div/iframe')))

# league = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/a[1]/span').text

# #Connects to mongo and sets up collections and databases
# client = pymongo.MongoClient("mongodb+srv://nickvirzi:sbsa@cluster0.rlqm7dy.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# vsinDailyTrackerDatabase = client["VSINDailyTrackerDatabase"]
# dayLegueTimeCollection = vsinDailyTrackerDatabase[date + ' - ' + league + ' - ' + displayTime]

# listOfMatchupData = []

# #Adds raw matchup data for a sport to an array, also checks to stop the table because it will go on forever
# for tableRow in driver.find_elements(By.XPATH, '//*[@id="dksplits"]/tbody//tr'):
#     matchupDataRow = [item.text for item in tableRow.find_elements(By.XPATH, './/*[self::td]')]
#     if matchupDataRow[0] == '' and matchupDataRow[1] == '': break
#     listOfMatchupData.append(matchupDataRow)

# #Neatly formats and enters data into the SBSA Database
# for fullMatchupData in listOfMatchupData:
#     teamNameData = fullMatchupData[0].split()
#     teamSpreadData = fullMatchupData[1].split()
#     spreadPercentOfMoneyData = fullMatchupData[2].split()
#     spreadPercentOfBetsData = fullMatchupData[3].split()
#     totalData = fullMatchupData[4].split()
#     totalPercentOfMoneyData = fullMatchupData[5].split()
#     totalPercentOfBetsData = fullMatchupData[6].split()
#     mlData = fullMatchupData[7].split()
#     mlPercentOfMoney = fullMatchupData[8].split()
#     mlPercentOfBets = fullMatchupData[9].split()

#     matchupDictionary = { 
#         "awayTeamName" : teamNameData[1],
#         "awayTeamAbbr" : teamNameData[0],
#         "homeTeamName" : teamNameData[3],
#         "homeTeamAbbr" : teamNameData[2],
#         "awayTeamSpread" : teamSpreadData[0],
#         "homeTeamSpread" : teamSpreadData[1],
#         "awayTeamSpreadPercentOfMoney" : spreadPercentOfMoneyData[0],
#         "homeTeamSpreadPercentOfMoney" : spreadPercentOfMoneyData[1],
#         "awayTeamSpreadPercentOfBets" : spreadPercentOfBetsData[0],
#         "homeTeamSpreadPercentOfBets" : spreadPercentOfBetsData[1],
#         "overTotal" : totalData[0],
#         "underTotal" : totalData[1],
#         "overPercentOfMoney" : totalPercentOfMoneyData[0],
#         "underPercentOfMoney" : totalPercentOfMoneyData[1],
#         "overPercentOfBets" : totalPercentOfBetsData[0],
#         "underPercentOfBets" : totalPercentOfBetsData[1],
#         "awayML" : mlData[0],
#         "homeML" : mlData[1],
#         "awayMLPercentOfMoney" : mlPercentOfMoney[0],
#         "homeMLPercentOfMoney" : mlPercentOfMoney[1],
#         "awayMLPercentOfBets" : mlPercentOfBets[0],
#         "homeMLPercentOfBets" : mlPercentOfBets[1],
#         "time" : displayTime,
#         "date" : date,
#         "league" : league
#     }

#     dayLegueTimeCollection.insert_one(matchupDictionary)