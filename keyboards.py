
from creds import ForceJoin, Sponsor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 

ForceJoinKeyboard = [[InlineKeyboardButton(item, url=ForceJoin[item])] for item in ForceJoin.keys()]
ForceJoinKeyboard.append([InlineKeyboardButton("جوین شدم :)", callback_data="joined")])
ForceJoinKeyboard = InlineKeyboardMarkup(ForceJoinKeyboard)


SponsorKeyboard = [[InlineKeyboardButton(item, url=Sponsor[item]) for item in Sponsor.keys()]]
SponsorKeyboard = InlineKeyboardMarkup(SponsorKeyboard)




def CreateKey(data):
    pass





