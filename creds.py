from json import load

def load_json():
    with open(__file__[:-8] + "creds.json", encoding='utf-8') as file:
        config = load(file)

    Admin = config["Admin"]
    BotToken = config["BotToken"]
    ForceJoin = config["ForceJoin"]
    ForceJoinId = config["ForceJoinId"]
    Sponsor = config["Sponsor"]

    return Admin, BotToken, ForceJoin, ForceJoinId, Sponsor

Admin, BotToken, ForceJoin, ForceJoinId, Sponsor = load_json()