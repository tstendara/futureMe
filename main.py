from flask import Flask, request
from db import index    

import datetime
import tracking
import schedule
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit


app = Flask(__name__)

@app.route("/")
def main():
    return urllib.request.urlopen("http://www.localhost:5000/remindMe")

    

@app.route('/remindMe', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():

    if request.method == 'POST':
        form = request.form

        x = {'email':form['email'], 'message':form['message'], 'date':form['date']}

        index.saveMessage(x)
        return 'Submitted with email ' + request.form['email']


    return '''<div style="margin: auto; width: 70%; border: 5px solid #FF80AB; padding: 10px;">
                <form method="POST" style="margin: auto; width: 50%;"> 
                    Email: <input type="text" name="email"><br>
                    <p style="margin-bottom:10px">Message:</p> <textarea  rows="3" cols="27" type="text" name="message"></textarea><br>
                    Date(year-month-day): <input type="text" name=date><br>
                    <input type="submit" value="Submit"><br>
                </form>
                </div>'''

def getMessages():
    currentDT = datetime.datetime.now()
    fullDate = str(currentDT)

    year = fullDate[0:4]

    if fullDate[5] == '0':
        month = fullDate[6]
    else:
        month = fullDate[5:7]

    if fullDate[8] == '0':
        day = fullDate[9]
    else:
        day = fullDate[8:10]

    date = {"year": int(year), "month": int(month), "day": int(day)}
    results = index.getMessages(date)
    
    for cur in results:
        formats = list(cur)
        print(formats[1])



scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(
    func=getMessages,
    trigger=IntervalTrigger(seconds=2),
    id='printing_time_job',
    name='Print time every 2 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


