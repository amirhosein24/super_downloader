
def load_json():

    from json import load
    from os import path, _exit

    home = path.dirname(path.dirname(__file__)) + "/"

    try:
        with open(__file__[:-8] + "creds.json", encoding='utf-8') as file:
            config = load(file)
    except FileNotFoundError:
        print("creds.json file wasnt found, exiting the bot ...")
        _exit(0)

    admin = config["Admin"]
    bottoken = config["BotToken"]

    api_id = config["ApiId"]
    api_hash = config["ApiHash"]

    channel = config["Channel"]

    sponsor = config["Sponsor"]
    apps = config["apps"]

    from telegram import Bot
    bot = Bot(token=bottoken)

    del config, load, path, _exit, Bot

    return admin, home, bottoken, api_id, api_hash, channel, sponsor, bot, apps


Admin, Home, BotToken, ApiId, ApiHash, Channel, Sponsor, Bot, Apps = load_json()
