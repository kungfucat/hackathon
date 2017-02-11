from sms import *
import datetime

today = datetime.date.today()
today = str(today.day) + '/' + str(today.month) + '/' + str(today.year)
print today

file = open("messages.csv" , "r")
lines = file.readlines()
write_lines = []
#print lines
for line in lines :
    temp = line.split(',' ,2)
    if temp[0] == today :
        sendMessage(temp[2] , '+91' + temp[1]  )
    else :
        write_lines.append(line)
file.close()

file = open("messages.csv" , "w")
file.writelines(write_lines)
file.close()
