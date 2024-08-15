
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

    apps = config["apps"]

    api_id = config["ApiId"]
    api_hash = config["ApiHash"]
    bottoken = config["BotToken"]

    admin = config["Admin"]
    logger = config["logger"]
    channel = config["Channel"]
    sponsor = config["Sponsor"]

    from telegram import Bot
    bot = Bot(token=bottoken)

    del config, load, path, _exit, Bot

    return admin, logger, home, bottoken, api_id, api_hash, channel, sponsor, bot, apps


Admin, Logger, Home, BotToken, ApiId, ApiHash, Channel, Sponsor, Bot, Apps = load_json()


from os import mkdir
try:
    mkdir(Home + "downloaders/cache/")
except:
    pass
del mkdir
