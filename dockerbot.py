import time
import random
import datetime
import telepot
from subprocess import call
import subprocess
import os
import sys
import docker
from docker import Client
from telepot.loop import MessageLoop

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
bot = telepot.Bot(os.getenv('API_KEY'))
MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')
 
while 1:
    time.sleep(10)
