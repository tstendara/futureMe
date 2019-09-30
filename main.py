from flask import Flask, request
from db import index    
import tesing


import datetime
import tracking
import schedule
import time
import asyncio
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import atexit

done = False
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




allMessages = []

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
        formatting = list(cur)
        body = {"reciever": formatting[0], "message": formatting[1]}
        allMessages.append(body)
    
    sendMsg()


def sendMsg():
    if len(allMessages) > 0:
        tesing.loop(allMessages)
    else:
        return

    

scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})
scheduler.start()

def testing():
    print('waow')

scheduler.add_job(testing, CronTrigger.from_crontab('0 0 * * *'))

scheduler.add_job(getMessages, CronTrigger.from_crontab('0 0 * * *'))

# scheduler.add_job(
#     func=getMessages,
#     trigger=IntervalTrigger(seconds=20),
#     id='getting_messages',
#     name='Getting messages every ',
#     start_date='2019-10-01 07:30')

# scheduler.add_job(
# func=sendMsg,
# trigger=IntervalTrigger(hours=2),
# id='sending_messages',
# name='send messages every 24 hours',
# start_date='2019-10-01 08:30')

    
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


