import time
import re
import random
import datetime
import logging
from subprocess import call
import subprocess
import os
import sys
import docker
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get allowed IDs from environment variable
ALLOWED_IDS = [uid.strip() for uid in os.getenv('ALLOWED_IDS', '').split(',') if uid.strip()] if os.getenv('ALLOWED_IDS') else []

def getCommandHelp(line):
    if "#[" in line:
        start = line.find("#[") + 2
        end = line.find("]#")
        return line[start:end]
    return ""

# Auto Command List
def search_string_in_file(file_name, string_to_search):
    list_of_results = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                if ("/?" not in line and not "o/" in line and not "," in line):
                    command = line
                    number = command.rfind("def ")
                    if number != -1:
                        command = command[number+4:]
                        space_pos = command.find("(")
                        if space_pos != -1:
                            command_name = command[:space_pos]
                            help_text = getCommandHelp(line)
                            command = f"/{command_name} {help_text}\n"
                            list_of_results.append(command)
    return list_of_results

# Check if user is authorized
def is_authorized(update, context):
    user_id = str(update.message.from_user.id)
    if user_id not in ALLOWED_IDS:
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo="https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif"
        )
        logger.warning(f"Unauthorized access attempt from user ID: {user_id}")
        return False
    return True

# Command handlers
def start(update, context):
    if not is_authorized(update, context):
        return
    command_list = search_string_in_file('/opt/dockerbot/dockerbot.py', "def ")
    message = "Command List:\n"
    for cmd in command_list:
        message += cmd
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def help_command(update, context):
    start(update, context)

def time_command(update, context): #[ Get Local Time ]#
    if not is_authorized(update, context):
        return
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=str(datetime.datetime.now())
    )

def speed_command(update, context): #[ Run Speedtest ]#
    if not is_authorized(update, context):
        return
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Running speed test... Please wait."
    )
    try:
        result = subprocess.check_output(['speedtest-cli', '--share'])
        result_str = result.decode('utf-8')
        photo_match = re.search(r"(?P<url>https?://[^\s]+)", result_str)
        if photo_match:
            photo_url = photo_match.group("url")
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=photo_url
            )
        else:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=result_str
            )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error running speed test: {str(e)}"
        )

def ip_command(update, context): #[ Get Real IP ]#
    if not is_authorized(update, context):
        return
    try:
        result = subprocess.check_output(['curl', 'ipinfo.io/ip'])
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=result.decode('utf-8')
        )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error getting IP: {str(e)}"
        )

def disk_command(update, context): #[ Get Disk Space ]#
    if not is_authorized(update, context):
        return
    try:
        result = subprocess.check_output(['df', '-h'])
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=result.decode('utf-8')
        )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error getting disk space: {str(e)}"
        )

def mem_command(update, context): #[ Get Memory ]#
    if not is_authorized(update, context):
        return
    try:
        result = subprocess.check_output(['cat', '/proc/meminfo'])
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=result.decode('utf-8')
        )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error getting memory info: {str(e)}"
        )

def stat_command(update, context): #[ Get bot Status ]#
    if not is_authorized(update, context):
        return
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Number five is alive!'
    )

def list_containers_command(update, context): #[ List all Docker containers ]#
    if not is_authorized(update, context):
        return
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        if not containers:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="No containers found."
            )
            return
        for container in containers:
            message = (f"{container.name}: {container.status}\n"
                       f"( /{container.name}_restart \n"
                       f" /{container.name}_stop \n"
                       f" /{container.name}_start )")
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=message
            )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error listing containers: {str(e)}"
        )

def container_command(update, context):
    if not is_authorized(update, context):
        return
    command = update.message.text
    operation = None
    if command.endswith("_restart"):
        operation = "restart"
    elif command.endswith("_stop"):
        operation = "stop"
    elif command.endswith("_start"):
        operation = "start"
    else:
        return
    container_name = command.lstrip('/').rsplit(f'_{operation}', 1)[0]
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True, filters={'name': container_name})
        if not containers:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Container '{container_name}' not found."
            )
            return
        container = containers[0]
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{operation.capitalize()}ing {container_name}..."
        )
        if operation == "restart":
            container.restart()
        elif operation == "stop":
            container.stop()
        elif operation == "start":
            container.start()
        time.sleep(2)
        container.reload()
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{container_name} is: {container.status}"
        )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error {operation}ing container: {str(e)}"
        )

# Error handler
def error_handler(update, context):
    logger.error(f"Update {update} caused error {context.error}")
    if update:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="An error occurred while processing your request."
        )

def main():
    api_key = os.getenv('API_KEY')
    if not api_key:
        sys.exit("API_KEY environment variable is not set")
    updater = Updater(api_key)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("time", time_command))
    dp.add_handler(CommandHandler("speed", speed_command))
    dp.add_handler(CommandHandler("ip", ip_command))
    dp.add_handler(CommandHandler("disk", disk_command))
    dp.add_handler(CommandHandler("mem", mem_command))
    dp.add_handler(CommandHandler("stat", stat_command))
    dp.add_handler(CommandHandler("list_containers", list_containers_command))

    dp.add_handler(MessageHandler(Filters.regex(r"^/[a-zA-Z0-9_-]+_(restart|stop|start)$"), container_command))

    dp.add_error_handler(error_handler)

    logger.info("Starting bot...")
    updater.start_polling()
    logger.info("Bot started successfully!")
    updater.idle()

if __name__ == "__main__":
    main()
