from pyrogram import Client, Filters

app = Client("my_account")


@app.on_message(Filters.private)
def hello(client, message):
    message.reply("Hello {}".format(message.from_user.first_name))


app.run()
helloworld() 