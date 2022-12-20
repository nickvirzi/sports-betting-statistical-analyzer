import pymongo
from pymongo.server_api import ServerApi
from datetime import datetime

#This script imports the mongo vsin data to anaylze for specific trends to then send to the database

#Notes-------------------------------------------------------------------------------------------------
# - A trend page in the db will have all leagues for the day.
# - TrendsDatabase
#   |
#    --> (month)/(day) - (time) - (trend)

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
client = pymongo.MongoClient("mongodb+srv://nickvirzi:sbsa@cluster0.rlqm7dy.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
vsinDailyTrackerDatabase = client["VSINDailyTrackerDB"]

leagues = ['CBB', 'CFB', 'NBA', 'NFL', 'NHL']
mostRecentTimeInDB = -1

for collectionName in vsinDailyTrackerDatabase.list_collection_names():
    if collectionName[-5] == ' ': 
        time = collectionName[-7:]
        firstDigit = int(time[3])
    else: 
        time = collectionName[-8:]
        firstDigit = int(time[3] + time[4])

    secondDigit = int(time[-2:])
    if 'PM' in time: firstDigit += 12

    if (firstDigit + (secondDigit / 60)) > mostRecentTimeInDB: 
        if 'PM' in time: firstDigit -= 12
        mostRecentTimeInDBString = str(firstDigit) + ':' + str(secondDigit)
        if 'PM' in time: firstDigit += 12
        mostRecentTimeInDB = firstDigit + (secondDigit / 60)

    

for league in leagues:
    dayLegueTimeCollection = vsinDailyTrackerDatabase[date + ' - ' + league + ' - ' + timeModifer + ' ' + mostRecentTimeInDBString] #'12/19 - NFL - PM 9:48'
    #print(dayLegueTimeCollection.find_one({"awayTeamName": " UTA Jazz"}))
    print(dayLegueTimeCollection.find_one())
