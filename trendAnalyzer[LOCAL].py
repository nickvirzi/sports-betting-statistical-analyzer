import pymongo
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta
from TrendPick import TrendPick
import certifi

ca = certifi.where()

#This script is design to capture the vsin data and send it to a database to be tracked and interpreted

#Notes-------------------------------------------------------------------------------------------------
# Do I wana analyze dynamically by the web, or import all stats from games from major leagues to my DB??
# New script to scrape scores every morning, checks for duplicates of the day, decide how in depth to go on stats kept. 
# Then this script can pull that data and not have to scrape. 

#Functions
#Take in league and return the ESPN league string needed to find scoreboard
def getESPNLeagueAbbreviation(league):
    espnLeagueDictionary = { 'NFL': 'nfl', 'NBA': 'nba', 'CBB': 'mens-college-basketball', 'CFB': 'college-football', 'NHL': 'nhl' }
    espnLeague = espnLeagueDictionary[league]
    return espnLeague

#Sets up current time and date formatting
now = datetime.now()
now -= timedelta(days=1)
currentTimeMilitary = now.strftime("%H:%M")
currentTimeStandard = datetime.strptime(currentTimeMilitary, "%H:%M")
displayTime = currentTimeStandard.strftime("%r")
timeModifer = displayTime[-2:]
displayTime = displayTime[:-6]
date = now.strftime("%m/%d")
tempDate = date.split('/')

if tempDate[1][0] == '0': date = date.replace('0', '')
if displayTime[0] == '0': displayTime = displayTime.replace('0', '', 1)

#Connects to mongo and sets up collections and databases
#Alternative second argument is: "server_api=ServerApi('1')" hand in hand with the certify
client = pymongo.MongoClient("mongodb+srv://nickvirzi:sbsa@cluster0.rlqm7dy.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
vsinTrendTrackerDatabase = client["VSINTrendTrackerDB"]

trends = ['Money_1_Greater_Than_Bets', 'Money_15_Greater_Than_Bets', 'Money_25_Greater_Than_Bets', 'Money_40_Greater_Than_Bets',]
trendPicks = []
mostRecentTimeInDB = -1

for collectionName in vsinTrendTrackerDatabase.list_collection_names():
    #Get current date in correct form
    if collectionName[0] == '1' and collectionName[1] != '/': collectionDate = collectionName[:5]
    else: collectionDate = collectionName[:4]
    
    #Checks for matching dates then finds the most recent DB entry for that date
    if collectionDate == date: 
        if collectionName[-5] == ' ': 
            time = collectionName[-7:]
            firstDigit = int(time[3])
        else: 
            time = collectionName[-8:]
            firstDigit = int(time[3] + time[4])

        secondDigit = int(time[-2:])
        if 'PM' in time and firstDigit != 12: firstDigit += 12
        timeModifer = time[:2]
        
        if (firstDigit + (secondDigit / 60)) > mostRecentTimeInDB: 
            if 'PM' in time: firstDigit -= 12
            mostRecentTimeInDBString = str(firstDigit) + ':' + str(secondDigit)
            if 'PM' in time: firstDigit += 12
            mostRecentTimeInDB = firstDigit + (secondDigit / 60)

for trend in trends:
    trendDataCollection = vsinTrendTrackerDatabase[date + ' - ' + trend + ' - ' + timeModifer + ' ' + mostRecentTimeInDBString] #'12/19 - NFL - PM 9:48'

    for trendData in trendDataCollection.find():
        trendPick = TrendPick(trendData['team'][1:])
        trendPick.league = trendData['league']
        trendPick.line = trendData['line']
        trendPick.percentDifference = trendData['percentDifference']
        trendPick.percentMoney = trendData['percentMoney']
        trendPick.percentBets = trendData['percentBets']
        trendPick.time = trendData['time']
        trendPick.trend = trendData['trend']

        trendPicks.append(trendPick)