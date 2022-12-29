import pymongo
from Matchup import Matchup
from pymongo.server_api import ServerApi
from datetime import datetime

# This was needed to make the mongo work, idk why
import certifi
ca = certifi.where()

#This script imports the mongo vsin data to anaylze for specific trends to then send to the database

#Notes-------------------------------------------------------------------------------------------------
# - A trend page in the db will have all leagues for the day.
# - TrendsDatabase
#   |
#    --> (month)/(day) - (trend) - (timeModifer)(time)

#Functions
def spreadMoneyGreaterThanBetsTrend(matchupsByLeague, vsinTrendTrackerDatabase, dateTimeData):
    percentsGreaterThan = [1, 15, 25, 40]
    
    for percent in percentsGreaterThan:
        trendDataCollection = vsinTrendTrackerDatabase[dateTimeData['date'] + ' - ' + 'Money_' + str(percent) + '_Greater_Than_Bets' + ' - ' + dateTimeData['timeModifier'] + ' ' + dateTimeData['time']]
        
        for leagueMatchupData in matchupsByLeague:
            for matchup in leagueMatchupData['matchupDataArray']:
                if int((matchup.homeSpreadPercentOfMoney[:-1])) > int((matchup.homeSpreadPercentOfBets[:-1])) + (percent - 1):
                    percentDifference = int((matchup.homeSpreadPercentOfMoney[:-1])) - int((matchup.homeSpreadPercentOfBets[:-1]))
                    
                    trendData = {
                        "league": leagueMatchupData['league'],
                        "team": matchup.homeTeamName,
                        "line": matchup.homeSpread,
                        "percentDifference": percentDifference,
                        "percentMoney": matchup.homeSpreadPercentOfMoney,
                        "percentBets": matchup.homeSpreadPercentOfBets,
                        "time": matchup.time,
                        "trend": 'Money > ' + str(percent) + ' Bets'
                    }
                    
                    if trendDataCollection.find_one({"time":dateTimeData['time']}) and trendDataCollection.find_one({"team":matchup.homeTeamName})and trendDataCollection.find_one({"trend":'Money > Bets'}): break
                    else: trendDataCollection.insert_one(trendData)
                elif int((matchup.awaySpreadPercentOfMoney[:-1])) > int((matchup.awaySpreadPercentOfBets[:-1])) + (percent - 1):
                    percentDifference = int((matchup.awaySpreadPercentOfMoney[:-1])) - int((matchup.awaySpreadPercentOfBets[:-1]))
                    
                    trendData = {
                        "league": leagueMatchupData['league'],
                        "team": matchup.awayTeamName,
                        "line": matchup.awaySpread,
                        "percentDifference": percentDifference,
                        "percentMoney": matchup.awaySpreadPercentOfMoney,
                        "percentBets": matchup.awaySpreadPercentOfBets,
                        "time": matchup.time,
                        "trend": 'Money > ' + str(percent) + ' Bets'
                    }
                    
                    if trendDataCollection.find_one({"time":dateTimeData['time']}) and trendDataCollection.find_one({"team":matchup.awayTeamName}) and trendDataCollection.find_one({"trend": 'Money > ' + str(percent) + ' Bets'}): break
                    else: trendDataCollection.insert_one(trendData)

#Sets up current time and date formatting
now = datetime.now()
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
vsinDailyTrackerDatabase = client["VSINDailyTrackerDB"]
vsinTrendTrackerDatabase = client["VSINTrendTrackerDB"]

leagues = ['CBB', 'CFB', 'NBA', 'NFL', 'NHL']
matchupsByLeague = []
mostRecentTimeInDB = -1

for collectionName in vsinDailyTrackerDatabase.list_collection_names():
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

        if (firstDigit + (secondDigit / 60)) > mostRecentTimeInDB: 
            if 'PM' in time: firstDigit -= 12
            mostRecentTimeInDBString = str(firstDigit) + ':' + str(secondDigit)
            if 'PM' in time: firstDigit += 12
            mostRecentTimeInDB = firstDigit + (secondDigit / 60)

for league in leagues:
    dayLegueTimeCollection = vsinDailyTrackerDatabase[date + ' - ' + league + ' - ' + timeModifer + ' ' + mostRecentTimeInDBString] #'12/19 - NFL - PM 9:48'
    matchupsArray = []
    dateTimeData = {
        "date": date,
        'time': mostRecentTimeInDBString,
        "timeModifier": timeModifer
    }
    
    for matchupData in dayLegueTimeCollection.find():
        matchup = Matchup(matchupData['homeTeamName'][1:], matchupData['awayTeamName'][1:])
        matchup.homeSpread = matchupData['homeSpread']
        matchup.awaySpread = matchupData['awaySpread']
        matchup.homeSpreadPercentOfMoney = matchupData['homeSpreadPercentOfMoney']
        matchup.awaySpreadPercentOfMoney = matchupData['awaySpreadPercentOfMoney']
        matchup.homeSpreadPercentOfBets = matchupData['homeSpreadPercentOfBets']
        matchup.awaySpreadPercentOfBets = matchupData['awaySpreadPercentOfBets']
        matchup.overTotal = matchupData['overTotal']
        matchup.underTotal = matchupData['underTotal']
        matchup.overPercentOfMoney = matchupData['overPercentOfMoney']
        matchup.underPercentOfMoney = matchupData['underPercentOfMoney']
        matchup.overPercentOfBets = matchupData['overPercentOfBets']
        matchup.underPercentOfBets = matchupData['underPercentOfBets']
        matchup.homeML = matchupData['homeML']
        matchup.awayML = matchupData['awayML']
        matchup.homeMLPercentOfMoney = matchupData['homeMLPercentOfMoney']
        matchup.awayMLPercentOfMoney = matchupData['awayMLPercentOfMoney']
        matchup.homeMLPercentOfBets = matchupData['homeMLPercentOfBets']
        matchup.awayMLPercentOfBets = matchupData['awayMLPercentOfBets']
        matchup.date = matchupData['date']
        matchup.time = matchupData['time']
        matchup.league = matchupData['league']
        
        matchupsArray.append(matchup)

    if len(matchupsArray) != 0:
        leagueMatchupData = {
            "league": league,
            "matchupDataArray": matchupsArray
        }
    
        matchupsByLeague.append(leagueMatchupData)
        
spreadMoneyGreaterThanBetsTrend(matchupsByLeague, vsinTrendTrackerDatabase, dateTimeData)