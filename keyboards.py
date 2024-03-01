
from creds import ForceJoin, Sponsor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

ForceJoinKeyboard = [[InlineKeyboardButton(item, url=ForceJoin[item])] for item in ForceJoin.keys()]
ForceJoinKeyboard.append([InlineKeyboardButton("جوین شدم :)", callback_data="joined")])
ForceJoinKeyboard = InlineKeyboardMarkup(ForceJoinKeyboard)


SponsorKeyboard = [[InlineKeyboardButton(item, url=Sponsor[item]) for item in Sponsor.keys()]]
SponsorKeyboard = InlineKeyboardMarkup(SponsorKeyboard)



def CreateKey(data):
    keyboard = []
    for res in data.keys():
        if not res in ["title", "length", "None"]:
            keyboard.append([InlineKeyboardButton(f"{res} -- {data[res]}MB", callback_data=f"youtube-{res}")])
    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard


AdminKeyboard = [
    InlineKeyboardButton("send to all"      , callback_data='sendall')     ],[
    InlineKeyboardButton("send data base"   , callback_data='db')          ]
AdminKeyboard = InlineKeyboardMarkup(AdminKeyboard)



buymenu = [
    [InlineKeyboardButton("1 ساعت تایپ : 9,000 تومان", url='https://zarinp.al/544882')],
    [InlineKeyboardButton("3 ساعت تایپ : 25,000 تومان", url="https://zarinp.al/544884")],
    [InlineKeyboardButton("10 ساعت تایپ : 80,000 تومان", url="https://zarinp.al/544885")]]
buymenu = InlineKeyboardMarkup(buymenu)


admin_addmenu = [
        InlineKeyboardButton("1 month", callback_data="month-1"), InlineKeyboardButton("6 month", callback_data="month-6")],[
        InlineKeyboardButton("3 month", callback_data="month-3"), InlineKeyboardButton("none", callback_data="month-0")]
admin_addmenu = InlineKeyboardMarkup(admin_addmenu)



cancelbuy = ReplyKeyboardMarkup([["❌ لغو خرید ❌"]], resize_keyboard=True)



RemoveKeys = ReplyKeyboardRemove()
