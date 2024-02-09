
from creds import ForceJoin
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 








ForceJoinKeyboard = [[InlineKeyboardButton(item, url=ForceJoin[item])] for item in ForceJoin.keys()]

ForceJoinKeyboard.append(
    [InlineKeyboardButton("i joined :)", callback_data="joined")]
)

ForceJoinKeyboard = InlineKeyboardMarkup(ForceJoinKeyboard)

