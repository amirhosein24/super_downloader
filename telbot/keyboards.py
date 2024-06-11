


from downloader_bot.credentials.creds import ForceJoin, Sponsor
from telethon import Button

ForceJoinKeyboard = [Button.url(item, ForceJoin[item]) for item in ForceJoin.keys()]
ForceJoinKeyboard.append(Button.inline("جوین شدم :)", data="joined"))

SponsorKeyboard = [Button.url(item, Sponsor[item]) for item in Sponsor.keys()]

def CreateKey(data):
    keyboard = []
    for res in data.keys():
        if not res in ["title", "length", "None"]:
            keyboard.append(Button.inline(f"{res} -- {data[res]}MB", data=f"youtube-{res}"))
    return keyboard

AdminKeyboard = [
    Button.inline("send to all", data='sendall'),
    Button.inline("send data base", data='db')
]

buymenu = [
    Button.url("1 ماه : 49,000 تومان", url='https://zarinp.al/544899 '),
    Button.url("3 ماه : 119,000 تومان", url="https://zarinp.al/576440"),
    Button.url("6 ماه : 290,000 تومان", url="https://zarinp.al/576441")
]

admin_addmenu = [
    Button.inline("1 month", data="month-1"), Button.inline("6 month", data="month-6"),
    Button.inline("3 month", data="month-3"), Button.inline("none", data="month-0")
]

cancelbuy = [Button.text("❌ لغو خرید ❌")]
