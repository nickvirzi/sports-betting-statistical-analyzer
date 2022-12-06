import os
import vsinDailyTracker
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/runVSIN')
def runVSIN():
    os.system('python vsinDailyTracker.py')
    return 'Hello World'

if __name__ == '__main__':
    app.run('0.0.0.0', '5000')