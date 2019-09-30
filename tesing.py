import asyncio
import time
import smtplib 
import config


username = config.G_username
password = config.G_password

async def myTask(dat):
    time.sleep(2)
    print("Processing message")

    print(dat['reciever'])
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.ehlo()
    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(username,password) 
    
    # sending the mail 
    s.sendmail(username, dat["reciever"], dat["message"]) 
    
    # terminating the session 
    s.quit() 


async def myTaskGenerator(data):
    for i in data:
        asyncio.ensure_future(myTask(i))

def loop(messages):

    data = messages
    loop = asyncio.new_event_loop()
    loop.run_until_complete(myTaskGenerator(data))
    print("Completed All Tasks")
    loop.close()

