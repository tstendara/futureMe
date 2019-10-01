import pymysql
import datetime
import config

mydb = pymysql.connect(
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

    mydb.close()


def getMessages(date):
  results = []
  
  sql = "SELECT email, message FROM users where date=%s"
  x = datetime.date(date["year"], date["month"], date["day"])
  vals = (x,)
  mycursor.execute(sql, vals)

  myresult = mycursor.fetchall ( )

  for x in myresult :
    results.append(x)
  
  print(results)
  return results

  mydb.close()


def deleteMessages(date):
  sql="DELETE FROM users where date=%s"
  val= datetime.date(date["year"], date["month"], date["day"])
  vals=(val,)
  mycursor.execute(sql, vals)
  mydb.commit()

  mydb.close()

