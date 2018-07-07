#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pyrogram import Client, Filters, MessageHandler
import os

app = Client(
    "my_account",
    api_id=os.getenv("MTPROTO_API_ID"),
    api_hash=os.getenv("MTPROTO_API_HASH")
)

def on_document(client, message):
    #print(client)
    print(message)
    message.reply("Hello {}".format(message.from_user.first_name))


app.add_handler(MessageHandler(on_document, Filters.document))
app.run()