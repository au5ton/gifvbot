# gifvbot
Automatically converts large-ish .gif files sent in Telegram to a silent .mp4

## Context
In 2016, Telegram [implemented a feature](https://telegram.org/blog/gif-revolution) into their platform and clients that converts gif files into mp4 videos before sending them. However, very large gifs and user error will still let giant gif files slip through. To counteract this, this userbot will automatically recognize gifs that are sent as documents, encode them as mp4, and reply with an mp4-optimized gif.

## Requirements
- Python 3.5+
- FFmpeg installed and in PATH
- Linux/macOS environment

## Running an instance
- do some things to be written later