
from credentials.creds import Channel, Sponsor

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def join_channel_key():
    keyboard = []
    for channel_name in Channel:
        keyboard.append([InlineKeyboardButton(
            channel_name, url=Channel[channel_name]["link"])])
    keyboard.append([InlineKeyboardButton("جوین شدم :)))",
                    callback_data='joined')])
    return InlineKeyboardMarkup(keyboard)

# SponsorKeyboard = [[InlineKeyboardButton(item, url=Sponsor[item])] for item in Sponsor.keys()]


def spotify_key(link):
    keyboard = [
        [
            InlineKeyboardButton(
                "128K", callback_data=f"dcb_spotify_128k_{link}"),
            InlineKeyboardButton(
                "320K", callback_data=f"dcb_spotify_320k_{link}")
        ]
    ]
    return keyboard


def youtube_key(link, data):
    keyboard = []
    keys = list(data.keys())

    for i in range(0, len(keys), 2):
        res1 = keys[i]
        res2 = keys[i+1] if i+1 < len(keys) else None

        if res1 not in ["title", "length"]:
            size = data[res1]["size"]
            tag = data[res1]["itag"]
            if res1.endswith("bps"):
                button1 = InlineKeyboardButton(
                    f"فایل صوتی -- {res1} -- {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")
            else:
                button1 = InlineKeyboardButton(
                    f"{res1} -- {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")

        if res2 and res2 not in ["title", "length"]:
            size = data[res2]["size"]
            tag = data[res2]["itag"]
            if res2.endswith("bps"):
                button2 = InlineKeyboardButton(
                    f"فایل صوتی -- {res2} -- {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")
            else:
                button2 = InlineKeyboardButton(
                    f"{res2} -- {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")

        try:
            if res2:
                keyboard.append([button1, button2])
            else:
                keyboard.append([button1])
        except:
            pass

    return InlineKeyboardMarkup(keyboard)


BackKey = [[
    InlineKeyboardButton("back", callback_data="back_to_main")
]]
BackKey = InlineKeyboardMarkup(BackKey)


MainKey = [
    [
        InlineKeyboardButton("helppp", callback_data="help")
    ],
    [
        InlineKeyboardButton("yupppp", callback_data="account")
    ]
]
MainKey = InlineKeyboardMarkup(MainKey)


AdminKeyboard = [
    [
        InlineKeyboardButton("send to all", callback_data='admin_sendtoall')
    ],
    [
        InlineKeyboardButton("send data base", callback_data='admin_getdb')
    ]
]
AdminKeyboard = InlineKeyboardMarkup(AdminKeyboard)


AccountMenu = [
    [
        InlineKeyboardButton("خرید اشتراک ویژه", callback_data="get_prem")
    ],
    [
        InlineKeyboardButton("back", callback_data="back_to_main")
    ]
]
AccountMenu = InlineKeyboardMarkup(AccountMenu)


BuyMenu = [
    [
        InlineKeyboardButton("1 ماه : 49,000 تومان",
                             url='https://zarinp.al/544899')
    ],
    [
        InlineKeyboardButton("back", callback_data="back_to_account")
    ]
]
BuyMenu = InlineKeyboardMarkup(BuyMenu)


AdminPaymentMenu = [
    [
        InlineKeyboardButton("1 month", callback_data="month-1")
    ],
    [
        InlineKeyboardButton("none", callback_data="month-0")
    ]
]
AdminPaymentMenu = InlineKeyboardMarkup(AdminPaymentMenu)
