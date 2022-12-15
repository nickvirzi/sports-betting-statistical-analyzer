import os
import vsinTrendTracker
from vsinTrendTracker import vsinDailyTracker
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Evan is gay'

@app.route('/runVSIN')
def runVSIN():
    os.system('python vsinDailyTracker.py')
    return 'Hello World'

if __name__ == '__main__':
    #Wont work with local, comment out this line and change below to app.run()
    #port = int(os.environ.get('PORT')) 
    app.run()