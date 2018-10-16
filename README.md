[![codebeat badge](https://codebeat.co/badges/679d47b4-a076-41d4-8c25-e67d9e9775cd)](https://codebeat.co/projects/github-com-au5ton-gifvbot-master)

# gifvbot
Automatically converts large-ish .gif files sent in Telegram to a silent .mp4. Also converts webm and mkv files (not playable natively) to mp4.

## Context
In 2016, Telegram [implemented a feature](https://telegram.org/blog/gif-revolution) into their platform and clients that converts gif files into mp4 videos before sending them. However, very large gifs and user error will still let giant gif files slip through. To counteract this, this userbot will automatically recognize gifs that are sent as documents, encode them as mp4, and reply with an mp4-optimized gif. The "gifv" part refers to how [Imgur](https://github.com/au5ton/gifvbot) refers to [video alernatives to GIF](https://en.wikipedia.org/wiki/Video_alternative_to_GIF).


Check out the live bot here: **https://t.me/gifvbot**

## Demonstration

See [demo video](https://www.youtube.com/watch?v=x7euHeqo64s).

## Requirements
- Python 3.5+
- FFmpeg installed and in PATH
- Linux/macOS environment
- A Telegram user account (can be separate from your primary account)

## Running an instance
- `git clone https://github.com/au5ton/gifvbot.git`
- `pip3 install -r requirements.txt`
- Make gif2mp4.sh executable: `chmod u+x gif2mp4.sh`
- [Register a new Telegram application](https://my.telegram.org/apps)
- `cp .env.example .env`
- Supply API ID and API Hash that was provided when registering your Telegram application by editing the `.env` file
- Run the python script: `python3 bot.py`
- Follow instructions to sign into a Telegram user account
- The bot is now running

## What is a userbot?
Although rare, a Telegram userbot is a type of Telegram bot that does not run from a Telegram bot account, but from a full user account. Telegram userbots are fully-fledged Telegram accounts. The only reason a Telegram bot would be made to be a userbot instead of a normal bot created by the BotFather is because of API limitations. 

## Why is gifvbot a userbot instead of a normal bot?
gifvbot is a userbot because the Telegram bot API [limits attached documents to be downloaded at 20MB](https://core.telegram.org/bots/api#file), which would defeat the purpose of downloading large gifs and converting them for convenience. The only solution was to make gifvbot a userbot.
