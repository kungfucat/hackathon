import datetime
from twilio.rest import TwilioRestClient
from data import *
import sqlite3


account_sid = "" # Your Account SID from www.twilio.com/console
auth_token  = ""  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)


def sendMessage(body , to) :
    message = client.messages.create(body=body,
        to= to, # Replace with your phone number
        from_="+14133845487") # Replace with your Twilio number
    print(message.sid)

def sendBaby(chat_id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute("SELECT * FROM subs WHERE chatid = ?" , [chat_id])
    temp  = c.fetchall()[0]
    babyweek = temp[5]
    mobile_no  = temp[1]
    for i in babydata :
        if i >= babyweek :
            write_baby( i, babyweek , mobile_no)
    sendMessage("You have registered for New Born Baby Vaccination Schedule." , '+91' + str(mobile_no))


def write_baby(week , babyweek , mobile_no):
    d = datetime.date.today()
    diff = week - babyweek
    t =datetime.timedelta(days=7*diff)
    a = t+d
    result_date = str(a.day) + '/' + str(a.month) + '/' + str(a.year)
    file = open('messages.csv' , 'a')
    file.write(result_date + ',' + str(mobile_no) + ',' + babydata[week] + '\n')
    file.close()



def sendPreg(chat_id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute("SELECT * FROM subs WHERE chatid = ?" , [chat_id])
    temp  = c.fetchall()[0]
    pregweek = temp[3]
    mobile_no  = temp[1]
    for i in pregdata :
        if i >= pregweek :
            write_preg( i, pregweek , mobile_no)
    sendMessage("You have registered for Pregnancy Checkup Schedule." , '+91' + str(mobile_no))


def write_preg(week , pregweek , mobile_no):
    d = datetime.date.today()
    diff = week - pregweek
    t =datetime.timedelta(days=7*diff)
    a = t+d
    result_date = str(a.day) + '/' + str(a.month) + '/' + str(a.year)
    file = open('messages.csv' , 'a')
    file.write(result_date + ',' + str(mobile_no) + ',' + pregdata[week] + '\n')
    file.close()

def write_monthly(chat_id) :
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM subs WHERE chatid = ?" , [chat_id])
    temp  = c.fetchall()[0]
    mobile_no  = temp[1]
    d = datetime.date.today()
    for i in range(1,13):
        t = datetime.timedelta(days=30*i)
        a = t+d
        result_date = str(a.day) + '/' + str(a.month) + '/' + str(a.year)
        file = open('messages.csv' , 'a')
        file.write(result_date + ',' + str(mobile_no) + ',' + "Reminder For Due Monthly Checkup By MEDIBOT" + '\n')
        file.close()
    sendMessage("You have registered for Monthly Regular Checkup Schedule." , '+91' + str(mobile_no))
