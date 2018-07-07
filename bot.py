#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
from pyrogram import Client, Filters, MessageHandler
import os
import shutil
import subprocess
import colorama
from colorama import Fore, Back, Style
load_dotenv(find_dotenv())
colorama.init()

PROJECT_DIRECTORY = os.path.split(os.path.realpath(__file__))[0]
FILE_SIZE_MINIMUM = 1 * (10**7) # 1 megabytes
FILE_SIZE_MAXIMUM = 2 * (10**8) # 200 megabytes
#FILE_SIZE_MAXIMUM = 2 * (10**7) # 20 megabytes

app = Client(
    "my_account",
    api_id=os.getenv("MTPROTO_API_ID"),
    api_hash=os.getenv("MTPROTO_API_HASH")
)

def on_document(client, message):
    #print(client)
    #print(message)
    if message.document.mime_type == "image/gif" and message.document.file_size in range(FILE_SIZE_MINIMUM,FILE_SIZE_MAXIMUM):
        print("Downloading gif...")
        download_path = client.download_media(message, message.document.file_id)
        print("download done: " + download_path)
        os.rename(download_path, download_path+".gif") # pyrogram doesnt add extension, so we must
        convert_script = os.path.join(PROJECT_DIRECTORY, "gif2mp4.sh")
        print("converting gif")
        subprocess.run([convert_script, download_path+".gif", download_path+".mp4"])
        print("done converting")
        print("sending video")
        client.send_video(message.chat.id, download_path+".mp4", reply_to_message_id=message.message_id)
        print("video sent!")
        print("cleaning up")
        os.remove(download_path+".gif")
        os.remove(download_path+".mp4")
        print("all cleaned up")


def on_message(client, message):
    # bot commands
    if message.text.startswith("/start"):
        message.reply("Hello! I automatically convert large gif files to a silent mp4. Simply send your gif file as an attached document and I will reply with a watchable mp4. I work in group chats too.")

print(Fore.YELLOW + "Performing startup checks" + Style.RESET_ALL)
print("\tChecking for ffmpeg in PATH...")
if shutil.which("ffmpeg") is not None:
    print("\tFFmpeg found")
else:
    print("\tFFmpeg not found!")
    raise Exception(Fore.RED + "FFmpeg could not be located in your path" + Style.RESET_ALL)
print("\tChecking for execute permissions for gif2mp4.sh")
if os.access(os.path.join(PROJECT_DIRECTORY, "gif2mp4.sh"), os.X_OK):
    print("\tFile permissions ok")
else:
    print("Won\'t be able to execute gif2mp4.sh. Try: chmod u+x gif2mp4.sh")
    raise Exception(Fore.RED + "gif2mp4.sh cannot be executed, change the file permissions" + Style.RESET_ALL)
print("\tDeleting contents of `downloads` directory")
shutil.rmtree(os.path.join(PROJECT_DIRECTORY, "downloads"))
os.makedirs(os.path.join(PROJECT_DIRECTORY, "downloads"))
print("\tCleaned `downloads` directory")

# if the code has made it here, everything has gone ok
print(Fore.GREEN + "Startup checks complete!" + Style.RESET_ALL)
app.add_handler(MessageHandler(on_document, Filters.document))
app.add_handler(MessageHandler(on_message, Filters.private))
app.run()