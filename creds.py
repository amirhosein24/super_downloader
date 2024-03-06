def load_json():
    
    from json import load
    
    with open(__file__[:-8] + "creds.json", encoding='utf-8') as file:
        config = load(file)

    Admin = config["Admin"]
    BotToken = config["BotToken"]
    ForceJoin = config["ForceJoin"]
    ForceJoinId = config["ForceJoinId"]
    Sponsor = config["Sponsor"]
    ApiId = config["ApiId"]
    ApiHash = config["ApiHash"]
    Instagram = config["Instagram"]

    return Admin, BotToken, ForceJoin, ForceJoinId, Sponsor, ApiId, ApiHash, Instagram

Admin, BotToken, ForceJoin, ForceJoinId, Sponsor, ApiId, ApiHash, Instagram = load_json()