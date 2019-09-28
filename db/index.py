import mysql.connector
import datetime
import config

mydb = mysql.connector.connect(
  host=config.host,
  user=config.user,
  passwd=config.passwd,
  database=config.database
)

mycursor = mydb.cursor()

def saveMessage(body):
    sql = "insert into users (email, message, date) values (%s, %s, %s)"
    vals = (body['email'], body['message'], body['date'])
    mycursor.execute(sql, vals)

    mydb.commit()
    print(mycursor.rowcount, "record saved")


    #crontab maybe?

def getMessages(date):
  results = []
  print(date)
  sql = "SELECT * FROM users where date=%s"
  x = datetime.date(date["year"], date["month"], date["day"])
  vals = (x,)
  mycursor.execute(sql, vals)

  myresult = mycursor.fetchall ( )

  for x in myresult :

    results.append(x)
  
  return results

