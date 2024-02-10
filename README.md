# X_dwonloader

## Twitter Video Downloader Telegram Bot

# This is a Telegram bot built in Python that can download and send Twitter videos to users.

 - Features

    1- Takes a Twitter video URL as input and downloads the video
    2- Sends the downloaded Twitter video to the user
    3- Handles videos with multiple variants and sends the highest quality
    4- Saves downloaded videos locally before sending
    5- Stores user data like usage counts in a SQLite database
    6- Requires users to join a channel before using the bot

 - Usage

    1- /start - Starts the bot and explains usage
    2- Send a Twitter video URL to the bot
    3- Bot downloads the video and sends it to the user

 - Code Overview

    BotHandler.py - Main bot file with command handlers
    DataBase.py - SQLite database code for storing user data
    keyboards.py - Reply keyboards like the force join button
    methods.py - Helper methods like downloading and processing videos
    creds.json - Bot token and admin Telegram ID


 - Running the Bot

    1- Install requirements (pip install -r requirements.txt)
    2- Add your Telegram bot token to creds.json
    3- Run python BotHandler.py
    4- Send /start to your bot in Telegram

# also create a creds.json format in this syntax

```
{
    "Admin": INT,
    "BotToken": "yourtelegrambottoken",
    "ForceJoin": {
        "name" : "link"
    },
    "ForceJoinId": {
        "name" : "@username"
    }
}
```