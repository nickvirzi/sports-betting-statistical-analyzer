import os
import vsinDailyTracker
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

#@app.route('/runVSIN')
#def runVSIN():
    os.system('python vsinDailyTracker.py')
    return 'Hello World'

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)