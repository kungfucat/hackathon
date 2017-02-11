import time
import random
import datetime
import telepot
from telepot.namedtuple import *
from tips import *
import os
from flask import Flask, request

try:
    from Queue import Queue
except ImportError:
    from queue import Queue


from helper import *

packs = ['Pregnancy Checkup Schedule' , 'New Born Vaccination' , 'Monthly Checkup' , 'General Tips']

def keyboardpack():

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=packs[0])],
        [KeyboardButton(text=packs[1])],
        [KeyboardButton(text=packs[2])],
        [KeyboardButton(text=packs[3])],
    ] , one_time_keyboard = True )
    return keyboard

def handle(msg):
    chat_id = msg['chat']['id']
    msg_text = msg['text']



    #print 'Got Message : %s' % msg_text
    print msg

    if msg_text == '/start' :
        new_connection(msg)
        bot.sendMessage( chat_id , "Hi, " + msg['from']['first_name'] +""", I am Medi-Bot. I can help you to stay healthy and to reduce the risk of dangerous diseases! I can give you a health tip whenever you want one, I will also provide SMS reminders for regular health checkups for pregnant women, vaccination schedule for children and monthly health checkup reminders for people of all age groups!! So use /start to get started with this amazing journey!"""  )
        temp = mobile_exists(chat_id)
        if not temp :
            bot.sendMessage(chat_id , "Please Enter Your 10 Digit Mobile Number for receiving updates on SMS Service")
        else :
            keyboard = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text=str(temp))]
            ] , one_time_keyboard = True )

            bot.sendMessage( chat_id , "Your Mobile Number Registered In DataBase is " + str(temp) + " . To Change , Type the New Number Below , Else Click on keyboard button below." , reply_markup = keyboard)



    elif msg_text.isdigit() and len(msg_text) == 10 :
        sendmsg = update_mob(msg)
        bot.sendMessage(chat_id  , sendmsg)
        keyboard = keyboardpack()
        bot.sendMessage( chat_id , "PLease Select the Service to Avail", reply_markup = keyboard )
    elif msg_text in packs :
        sendmsg = setPack(msg)
        bot.sendMessage(chat_id , sendmsg)

    elif msg_text.isdigit()  :
        sendmsg = setweek(msg)
        bot.sendMessage(chat_id , sendmsg)
    elif checkDate(msg_text)   :
        sendmsg = setweek(msg)
        bot.sendMessage(chat_id , sendmsg)

    elif msg_text == '/tip' :
        sendmsg = tips[random.randrange(1,50)]
        bot.sendMessage(chat_id , sendmsg)



# bot = telepot.Bot('362542537:AAF5EYYsRxLFGvIdZHu_po_1Bb7Wwk_IOvw')
# bot.message_loop(handle)
print 'I am listening ...'

try:
    table()
except :
    pass


TOKEN = 'TOKEN'
PORT = int(sys.argv[2])
URL =  ' https://medismsbot.herokuapp.com/' #"https://ded974f2.ngrok.io/verify"

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.message_loop({'chat': handle}, source=update_queue)


@app.route('/verify', methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'


if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT , debug=True)
