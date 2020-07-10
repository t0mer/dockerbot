import time
import random
import datetime
import telepot
from subprocess import call
import subprocess
import os
import sys
import docker
from telepot.loop import MessageLoop

#Auto Commmand List
def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    list_of_results = []
    new_line = "\n"
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                if ("/?" not in line):
                    command = line
                    number = command.rfind("/")
                    command = command[number:]
                    number = command.rfind("'")
                    command = command[:number]
                    command = command + new_line
                    # If yes, then add the line number & line as a tuple in the list
                    list_of_results.append(command)
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Got command: %s')%command
    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/speed':
        x = subprocess.check_output(['speedtest-cli','--share'])
        bot.sendMessage(chat_id,x)
    elif command == '/ip':
        x = subprocess.check_output(['curl','ipinfo.io/ip'])
        bot.sendMessage(chat_id,x)
    elif command == '/disk':
        x = subprocess.check_output(['df', '-h'])
        bot.sendMessage(chat_id,x)
    elif command == '/mem':
        x = subprocess.check_output(['cat','/proc/meminfo'])
        bot.sendMessage(chat_id,x)
    elif command == '/stat':
        bot.sendMessage(chat_id,'Number five is alive!')
    elif command == '/services':
        x = subprocess.check_output('service --status-all|grep "+"', shell = True)
        bot.sendMessage(chat_id,x)
    elif command == '/plexstat':
        try:
            client = client = docker.from_env()
            container = client.containers.list(all=True, filters={'name':'plex'})
            x = container[0].status
            bot.sendMessage(chat_id,x)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif command == '/plexrestart':
        try:
            client = client = docker.from_env()
            container = client.containers.list(all=True, filters={'name':'plex'})
            id = container[0].id
            container = client.containers.get(id)
            container.restart()
            x = container.status
            bot.sendMessage(chat_id,x)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif command == '/listcon':
        try:
            client = client = docker.from_env()
            containers = client.containers.list(all=True)
            bot.sendMessage(chat_id,containers)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif command == '/?':
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
