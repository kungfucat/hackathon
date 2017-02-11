import sqlite3
import datetime
from sms import *
from tips import *
packs = ['Pregnancy Checkup Schedule' , 'New Born Vaccination' , 'Monthly Checkup' , 'General Tips']
import random


def checkDate(date):
    ans = True
    if date[:2].isdigit() and date[3:5].isdigit() and date[6:].isdigit() and date[2] == '/' and date[5] == '/' :
        return True

    return False
def findweek(msg_text):
    a = datetime.date.today()
    dyear = int(msg_text[-4:])
    dday = int(msg_text[:2])
    dmonth = int(msg_text[3:5])
    weeks = ((a.year - dyear)*365 + (a.month - dmonth)*30 + (a.day - dday))//7
    return weeks

def setPack(msg):
    chat_id = msg['chat']['id']
    msg_text = msg['text']
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    if msg_text == packs[0] :
        sendmsg = "Please Enter The Week Of Pregnancy"
        c.execute("UPDATE subs SET pregweekpending = 1 where chatid = ? " , [chat_id])
        conn.commit()
    elif msg_text == packs[1] :
        sendmsg = "Please Enter The Date of Birth Of Child in DD/MM/YYYY"
        c.execute("UPDATE subs SET babyweekpending = 1 where chatid = ? " , [chat_id])
        conn.commit()
    elif msg_text == packs[2] :
        sendmsg = "You Have Registered For Monthly Checkup Remainder"
        write_monthly(chat_id)
    elif msg_text == packs[3] :
        sendmsg = tips[random.randrange(1,50)]
    return sendmsg

def setweek(msg):
    chat_id = msg['chat']['id']
    msg_text = msg['text']
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute("SELECT * FROM subs where chatid = ? " , [chat_id])
    temp = c.fetchall()[0]
    print temp
    if temp[4] == 1 or temp[6] == 1 :
        if temp[4] == 1 :
            c.execute("UPDATE subs SET pregweek = ? where chatid = ? " , [int(msg_text) , chat_id])
            sendmsg = "Updated Pregnancy Week Succesfully"
            sendPreg(chat_id)
            c.execute("UPDATE subs SET pregweekpending = 0 where chatid = ? " , [chat_id])
            conn.commit()
        elif temp[6] == 1 :
            print "Select"
            weeks = findweek(msg_text)
            c.execute("UPDATE subs SET babyweek = ? where chatid = ? " , [int(weeks) , chat_id])
            sendmsg = "Updated Vaccination Week Schedule Succesfully"
            sendBaby(chat_id)
            c.execute("UPDATE subs SET babyweekpending = 1 where chatid = ? " , [chat_id])
            conn.commit()
            print weeks

    conn.commit()

    return sendmsg

def update_mob(msg):
    chat_id = msg['chat']['id']
    msg_text = msg['text']
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("UPDATE subs SET mobile = ? where chatid = ? " , [int(msg_text) , chat_id])
    conn.commit()
    sendmsg = "Mobile Added Successfully"
    return sendmsg



def table() :
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE subs (
             chatid integer PRIMARY KEY,
             mobile integer NOT NULL ,
             sub_pack integer NOT NULL,
             pregweek integer DEFAULT 0,
             pregweekpending boolean DEFAULT 0 ,
             babyweek integer DEFAULT 0 ,
             babyweekpending boolean DEFAULT 0
            );''')

def new_connection(msg) :
    chat_id = msg['chat']['id']
    msg_text = msg['text']

    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(" SELECT * FROM subs WHERE chatid = ? " , [chat_id]  )
    temp =  c.fetchall()
    if temp == [] :
        c.execute("INSERT INTO subs VALUES (?,? , ?,?,?,?,?)" ,[ chat_id ,0000000000 , 0 , 0 , 0 , 0, 0])
        conn.commit()

    c.execute(" SELECT * FROM subs WHERE chatid = ? " , [chat_id]  )
    print c.fetchall()


def setAge(msg) :
    chat_id = msg['chat']['id']
    msg_text = msg['text']
    age = ''.join([i for i in msg_text if i.isdigit()])


def mobile_exists(chat_id) :
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM subs WHERE chatid = ?" , [chat_id])
    temp  = c.fetchall()[0]
    mobile_no  = temp[1]
    return mobile_no
