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

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port, debug=True)