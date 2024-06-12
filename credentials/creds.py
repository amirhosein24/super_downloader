
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
    botToken = config["BotToken"]

    api_id = config["ApiId"]
    api_hash = config["ApiHash"]

    forcejoin_name = config["ForceJoin"]
    forcejoin_id = config["ForceJoinId"]
    sponsor = config["Sponsor"]
    apps = config["apps"]

    from telegram import Bot
    bot = Bot(token=botToken)

    del config, load, path, _exit, Bot

    return admin, home, botToken, api_id, api_hash, forcejoin_id, forcejoin_name, sponsor, bot, apps


Admin, Home, BotToken, ApiId, ApiHash, ForceJoindId, ForceJoindName, Sponser, Bot, Apps = load_json()
