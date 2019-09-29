import smtplib 
import config

username = config.G_username
password = config.G_password

def sendMessages(data):
    print(data)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.ehlo()
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(username,password) 
    
    # message to be sent 
    message = "oi oi"
    
    # sending the mail 
    s.sendmail(username, "tstendara@gmail.com", message) 
    
    # terminating the session 
    s.quit() 

