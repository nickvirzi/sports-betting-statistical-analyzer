import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo.server_api import ServerApi
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

#This script is design to capture the vsin data and send it to a database to be tracked and interpreted

#Notes-------------------------------------------------------------------------------------------------
# - When clicking a different league header u gotta use full XPATH's bc they use active HTML switching


#Sets up driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.vsin.com/betting-resources/daily-betting-insights-for-mlb-nba-nhl/')
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

if tempDate[1][0] == '0': date = date.replace('0', '')
if displayTime[0] == '0': displayTime = displayTime.replace('0', '', 1)

#################################################################################################################################################
### Everything below this line can be sync'd with the other form to work the same apart from web driver behavior ###

#VSIN uses an IFrame which requires a switch to the frame
WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="main-content"]/div[2]/div[1]/div/iframe')))

#Create month dictionary
monthIntStringDict = {
    'January': '1', 'February': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6', 'July': '7', 'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12'
}

#Input month string for month date as a string
def getMonthIntString(month):
    monthIntString = monthIntStringDict[month]
    return monthIntString

def getLeagueVSINDailyData(date, displayTime, league, index): 
    #Connects to mongo and sets up collections and databases
    client = pymongo.MongoClient("mongodb+srv://nickvirzi:sbsa@cluster0.rlqm7dy.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    vsinDailyTrackerDatabase = client["VSINDailyTrackerDB"]
    dayLegueTimeCollection = vsinDailyTrackerDatabase[date + ' - ' + league + ' - ' + timeModifer + ' ' + displayTime] #'12/19 - NFL - PM 9:48'

    listOfMatchupData = []
    
    #Get date formatted to match the VSIN table
    thDate = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div[2]/div/div/div/table/thead[1]/tr/th[1]/span').text 
    thDate = thDate.split(',')[1].split()
    thDate = getMonthIntString(thDate[0]) + "/" + thDate[1]

    if thDate == date:
        #Adds raw matchup data for a sport to an array, also checks to stop the table because it will go on forever
        for tableRow in driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div[2]/div/div/div/table/tbody[1]//tr'):
            matchupDataRow = [item.text for item in tableRow.find_elements(By.XPATH, './/*[self::td]')]
            if matchupDataRow[0] == '' and matchupDataRow[1] == '': break
            listOfMatchupData.append(matchupDataRow)

    #Neatly formats and enters data into the SBSA Database
    for fullMatchupData in listOfMatchupData or []:
        teamNameData = fullMatchupData[0].split('\n')
        teamSpreadData = fullMatchupData[1].split()
        spreadPercentOfMoneyData = fullMatchupData[2].split()
        spreadPercentOfBetsData = fullMatchupData[3].split()
        totalData = fullMatchupData[4].split()
        totalPercentOfMoneyData = fullMatchupData[5].split()
        totalPercentOfBetsData = fullMatchupData[6].split()
        mlData = fullMatchupData[7].split()
        mlPercentOfMoney = fullMatchupData[8].split()
        mlPercentOfBets = fullMatchupData[9].split()

        #Set up dictionary for database insertion
        matchupDictionary = { 
            "awayTeamName" : teamNameData[0],
            "homeTeamName" : teamNameData[1],
            "awaySpread" : teamSpreadData[0],
            "homeSpread" : teamSpreadData[1],
            "awaySpreadPercentOfMoney" : spreadPercentOfMoneyData[0],
            "homeSpreadPercentOfMoney" : spreadPercentOfMoneyData[1],
            "awaySpreadPercentOfBets" : spreadPercentOfBetsData[0],
            "homeSpreadPercentOfBets" : spreadPercentOfBetsData[1],
            "overTotal" : totalData[0],
            "underTotal" : totalData[1],
            "overPercentOfMoney" : totalPercentOfMoneyData[0],
            "underPercentOfMoney" : totalPercentOfMoneyData[1],
            "overPercentOfBets" : totalPercentOfBetsData[0],
            "underPercentOfBets" : totalPercentOfBetsData[1],
            "awayML" : mlData[0],
            "homeML" : mlData[1],
            "awayMLPercentOfMoney" : mlPercentOfMoney[0],
            "homeMLPercentOfMoney" : mlPercentOfMoney[1],
            "awayMLPercentOfBets" : mlPercentOfBets[0],
            "homeMLPercentOfBets" : mlPercentOfBets[1],
            "time" : displayTime,
            "date" : date,
            "league" : league
        }

        #Double check the entry we are about to enter isnt in the table within the last minute
        if dayLegueTimeCollection.find_one({"time":displayTime}) and dayLegueTimeCollection.find_one({"awayTeamName":teamNameData[0]}) and dayLegueTimeCollection.find_one({"homeTeamName":teamNameData[1]}): break
        else: dayLegueTimeCollection.insert_one(matchupDictionary)

# Begin Main

#Gets league headers on VSIN
leagueTH = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[1]')
leagues = leagueTH.find_elements(By.XPATH, './/*[self::a]')

#Index through the different leagues to set up mathcups
for league in leagues:
    #VSINs first sport starts at index 1
    index = leagues.index(league) + 1 
    leagueName = league.text
    
    #Limiting to the first 5 sports on VSIN as of now
    if index < 6: 
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/a[' + str(index) + ']').click()
        getLeagueVSINDailyData(date, displayTime, leagueName, index)
