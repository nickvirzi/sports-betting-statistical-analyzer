import os
#import vsinDailyTracker
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    #Wont work with local, comment out this line and change below to app.run()
    port = int(os.environ.get('PORT')) 
    app.run(host='0.0.0.0', port=port, debug=True)