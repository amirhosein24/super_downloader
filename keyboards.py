
from creds import ForceJoin, Sponsor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 

ForceJoinKeyboard = [[InlineKeyboardButton(item, url=ForceJoin[item])] for item in ForceJoin.keys()]
ForceJoinKeyboard.append([InlineKeyboardButton("جوین شدم :)", callback_data="joined")])
ForceJoinKeyboard = InlineKeyboardMarkup(ForceJoinKeyboard)


SponsorKeyboard = [[InlineKeyboardButton(item, url=Sponsor[item]) for item in Sponsor.keys()]]
SponsorKeyboard = InlineKeyboardMarkup(SponsorKeyboard)



def CreateKey(data):
    keyboard = []
    for res in data.keys():
        if not res in ["title", "length", "None"]:
            keyboard.append([InlineKeyboardButton(f"{res} -- {data[res]}MB", callback_data=res)])
    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard






AdminKeyboard = [
    InlineKeyboardButton("send to all"      , callback_data='sendall')     ],[
    InlineKeyboardButton("send data base"   , callback_data='db')          ]
AdminKeyboard = InlineKeyboardMarkup(AdminKeyboard)

