from flask import Flask, request
from crontab import CronTab
from db import index    

import datetime

import schedule
import time

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

@app.route("/retrieve", methods=['GET'])
def getForToday():
    print(index.getMessages())
    return 'done'
