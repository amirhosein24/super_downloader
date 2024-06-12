

from credentials.creds import Channel, Sponsor
from telethon import Button


ForceJoinKeyboard = [
    Button.url(item, Channel[item]) for item in Channel
]

ForceJoinKeyboard.append(Button.inline("جوین شدم :)", data="joined"))

SponsorKeyboard = [Button.url(item, Sponsor[item]) for item in Sponsor.keys()]


def CreateKey(link, data):
    keyboard = []

    for res in data.keys():
        if not res in ["title", "length"]:

            size = data[res]["size"]
            tag = data[res]["itag"]

            keyboard.append(
                Button.inline(
                    f"{res} -- {size}MB", data=f"youtube-{tag}-{link}")
            )

    return keyboard


AdminKeyboard = [
    Button.inline("send to all", data='sendall'),
    Button.inline("send data base", data='db')
]

BuyMenu = [
    Button.url("1 ماه : 49,000 تومان", url='https://zarinp.al/544899')
]

AdminPaymentMenu = [
    Button.inline("1 month", data="month-1"),
    Button.inline("none", data="month-0")
]
