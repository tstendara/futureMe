import schedule
import time
import main
from db import index
import datetime


def job():
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
    print(index.getMessages(date))


schedule.every(0.1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
