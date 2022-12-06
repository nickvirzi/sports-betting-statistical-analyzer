import os
import vsinDailyTracker
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/runVSIN')
def runVSIN():
    os.system('python vsinDailyTracker.py')
    return 'Hello World'