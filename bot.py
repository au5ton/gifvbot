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
FILE_SIZE_MAXIMUM = 5 * (10**8) # 500 megabytes
#FILE_SIZE_MAXIMUM = 2 * (10**7) # 20 megabytes

app = Client(
    "my_account",
    api_id=os.getenv("MTPROTO_API_ID"),
    api_hash=os.getenv("MTPROTO_API_HASH")
)

# When a document is sent
def on_document(client, message):
    # if the document is a gif and is within an acceptable size
    if message.document.mime_type == "image/gif" and message.document.file_size in range(FILE_SIZE_MINIMUM,FILE_SIZE_MAXIMUM):
        print("eligbile document")
        # download the document
        download_path = client.download_media(message, message.document.file_id)
        print("\tdownloaded")
         # pyrogram doesnt add extension, so we must
        os.rename(download_path, download_path+".gif")
        # create the path to the conversion script
        convert_script = os.path.join(PROJECT_DIRECTORY, "gif2mp4.sh")
        # run the conversion script
        print("\tconversion running")
        status = subprocess.run([convert_script, download_path+".gif", download_path+".mp4"])
        # if the conversion failed or not
        if status.returncode is 0:
            # send the newly created mp4
            print("\tuploading")
            client.send_video(message.chat.id, download_path+".mp4", reply_to_message_id=message.message_id)
            print("\tvideo sent")
            # delete downloaded/generated files after
            os.remove(download_path+".gif")
            os.remove(download_path+".mp4")
        else:
            #print("error when converting")
            os.remove(download_path+".gif")

    # if the document is a webm and is within an acceptable size
    if (message.document.file_name.lower().endswith(".webm") or message.document.file_name.lower().endswith(".mkv")) and message.document.file_size in range(1,FILE_SIZE_MAXIMUM):
        print("eligbile document")
        extension = ""
        if(message.document.file_name.lower().endswith(".webm")):
            extension = ".webm"
        if(message.document.file_name.lower().endswith(".mkv")):
            extension = ".mkv"
        # download the document
        download_path = client.download_media(message, message.document.file_id)
        print("\tdownloaded")
         # pyrogram doesnt add extension, so we must
        os.rename(download_path, download_path+extension)
        # create the path to the conversion script
        print("\tconversion running")
        convert_script = os.path.join(PROJECT_DIRECTORY, "webm2mp4.sh")
        # run the conversion script
        status = subprocess.run([convert_script, download_path+extension, download_path+".mp4"])
        # if the conversion failed or not
        if status.returncode is 0:
            # send the newly created mp4
            print("\tuploading")
            client.send_video(message.chat.id, download_path+".mp4", reply_to_message_id=message.message_id)
            print("\tvideo sent")
            # delete downloaded/generated files after
            os.remove(download_path+extension)
            os.remove(download_path+".mp4")
        else:
            #print("error when converting")
            os.remove(download_path+extension)

# When a message is sent in a private message
def on_message(client, message):
    # bot commands
    if message.text.startswith("/start"):
        message.reply("Hello! I automatically convert large gif files to a silent mp4. Simply send your gif file as an attached document and I will reply with a watchable mp4. I work in group chats too.")
        message.reply("I\'m also open source! https://github.com/au5ton/gifvbot")


# Startup checks
print(Fore.YELLOW + "Performing startup checks" + Style.RESET_ALL)
# check
print("\tChecking for ffmpeg in PATH...")
if shutil.which("ffmpeg") is not None:
    print("\tFFmpeg found")
else:
    print("\tFFmpeg not found!")
    raise Exception(Fore.RED + "FFmpeg could not be located in your path" + Style.RESET_ALL)
# check
print("\tChecking for execute permissions for gif2mp4.sh")
if os.access(os.path.join(PROJECT_DIRECTORY, "gif2mp4.sh"), os.X_OK):
    print("\tFile permissions ok")
else:
    print("Won\'t be able to execute gif2mp4.sh. Try: chmod u+x gif2mp4.sh")
    raise Exception(Fore.RED + "gif2mp4.sh cannot be executed, change the file permissions" + Style.RESET_ALL)
# check
print("\tChecking for execute permissions for webm2mp4.sh")
if os.access(os.path.join(PROJECT_DIRECTORY, "webm2mp4.sh"), os.X_OK):
    print("\tFile permissions ok")
else:
    print("Won\'t be able to execute webm2mp4.sh. Try: chmod u+x webm2mp4.sh")
    raise Exception(Fore.RED + "webm2mp4.sh cannot be executed, change the file permissions" + Style.RESET_ALL)
# check
print("\tDeleting contents of `downloads` directory")
if os.path.isdir(os.path.join(PROJECT_DIRECTORY, "downloads")) is True:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, "downloads"))
elif os.path.exists(os.path.join(PROJECT_DIRECTORY, "downloads")):
    os.remove(os.path.join(PROJECT_DIRECTORY, "downloads"))
os.makedirs(os.path.join(PROJECT_DIRECTORY, "downloads"))
print("\tCleaned `downloads` directory")

# if the code has made it here, startup checks have gone ok
print(Fore.GREEN + "Startup checks complete!" + Style.RESET_ALL)
app.add_handler(MessageHandler(on_document, Filters.document))
app.add_handler(MessageHandler(on_message, Filters.private))
app.run()
