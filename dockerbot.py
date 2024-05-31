import time
import re
import random
import datetime
import telepot
from subprocess import call
import subprocess
import os
import sys
import docker
from telepot.loop import MessageLoop



def getCommandHelp(line):
    if "#[" in line:
        start = line.find("#[") + len("]#")
        end = line.find("]#")
        return line[start:end]
    return ""


#Auto Commmand List
def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                if ("/?" not in line and not "o/" in line and not "," in line):
                    command = line
                    number = command.rfind("/")
                    command = command[number:]
                    number = command.rfind("'")
                    command = command[:number]
                    command = command + " " + getCommandHelp(line)  +"\n"
                    # If yes, then add the line number & line as a tuple in the list
                    list_of_results.append(command)
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if str(chat_id) not in os.getenv('ALLOWED_IDS'):
        bot.sendPhoto(chat_id,"https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        return ""



    print ('Got command: %s')%command
    if command == '/time': #[ Get Local Time ]#
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/speed': #[ Run Speedtest ]#
        x = subprocess.check_output(['speedtest-cli','--share'])
        photo = re.search("(?P<url>https?://[^\s]+)", x).group("url")
        bot.sendPhoto(chat_id,photo)
    elif command == '/ip': #[ Get Real IP ]#
        x = subprocess.check_output(['curl','ipinfo.io/ip'])
        bot.sendMessage(chat_id,x)
    elif command == '/disk': #[ Get Disk Space ]#
        x = subprocess.check_output(['df', '-h'])
        bot.sendMessage(chat_id,x)
    elif command == '/mem': #[ Get Memory ]#
        x = subprocess.check_output(['cat','/proc/meminfo'])
        bot.sendMessage(chat_id,x)
    elif command == '/stat': #[ Get bot Status ]#
        bot.sendMessage(chat_id,'Number five is alive!')
    elif command == '/list_containers':
        try:
            client = client = docker.from_env()
            containers = client.containers.list(all=True)
            for f in containers:
                bot.sendMessage(chat_id,str(f.name) + " : " + str(f.status) + "\n( /" +f.name +"_restart \n /" +f.name +"_stop \n /" +f.name +"_start )")
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif '_restart' in command:
        try:
            commands = command.split('_')
            commands[0] = commands[0].replace('/','')
            client = client = docker.from_env()
            containers = client.containers.list(all=True, filters={'name':commands[0]})
            bot.sendMessage(chat_id,'Restarting ' + commands[0])
            containers[0].restart()
            time.sleep(2)
            bot.sendMessage(chat_id, commands[0] + ' is: ' + containers[0].status)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif '_stop' in command:
        try:
            commands = command.split('_')
            commands[0] = commands[0].replace('/','')
            client = client = docker.from_env()
            containers = client.containers.list(all=True, filters={'name':commands[0]})
            bot.sendMessage(chat_id,'Stopping ' + commands[0])
            containers[0].stop()
            time.sleep(2)
            bot.sendMessage(chat_id, commands[0] + ' is: ' + containers[0].status)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif '_start' in command:
        try:
            commands = command.split('_')
            commands[0] = commands[0].replace('/','')
            client = client = docker.from_env()
            containers = client.containers.list(all=True, filters={'name':commands[0]})
            bot.sendMessage(chat_id,'Starting  ' + commands[0])
            containers[0].start()
            time.sleep(2)
            bot.sendMessage(chat_id, commands[0] + ' is: ' + containers[0].status)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif command == '/?' or command=="/start":
        array = search_string_in_file('/opt/dockerbot/dockerbot.py', "/")
        s = "Command List:\n"
        for val in array:
            if ")" not in val:
                s+=str(val)
        x = s
        bot.sendMessage(chat_id,x)

bot = telepot.Bot(os.getenv('API_KEY'))
MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')
 
while 1:
    time.sleep(10)
