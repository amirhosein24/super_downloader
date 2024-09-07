
from creds import Channel, Sponsor

from telethon.tl.custom import Button
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


#  ########################################## telegram keyboards ##########################################
def join_channel_key():
    keyboard = []

    for channel_name in Channel:
        keyboard.append(
            [
                InlineKeyboardButton(
                    channel_name, url=Channel[channel_name]["url"])
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton("جوین شدم :)", callback_data='joined')
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def spotify_key(trackid: str):
    keyboard = [
        [
            InlineKeyboardButton(
                "320K", callback_data=f"dcb_spotify_320k_{trackid}"),
            InlineKeyboardButton(
                "128K", callback_data=f"dcb_spotify_128k_{trackid}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def youtube_key(link, data):
    keyboard = []
    keys = list(data.keys())

    for i in range(0, len(keys), 2):
        res1 = keys[i]
        res2 = keys[i+1] if i+1 < len(keys) else None

        size = data[res2]["size"]
        tag = data[res2]["itag"]

        if res1 not in ["title", "length"]:
            if res1.endswith("bps"):
                button1 = InlineKeyboardButton(
                    f"فایل صوتی - {res1} - {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")
            else:
                button1 = InlineKeyboardButton(
                    f"{res1} -- {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")

        if res2 and res2 not in ["title", "length"]:
            if res2.endswith("bps"):
                button2 = InlineKeyboardButton(
                    f"فایل صوتی - {res2} - {size}MB", callback_data=f"dcb_youtube_{tag}_{link}")
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


SponsorKeyboard = [
    [
        InlineKeyboardButton(item, url=Sponsor[item])
    ] for item in Sponsor.keys()
]
SponsorKeyboard = InlineKeyboardMarkup(SponsorKeyboard)


BackKey = [[
    InlineKeyboardButton("برگشت به منو اصلی 🏡", callback_data="back_to_main")
]]
BackKey = InlineKeyboardMarkup(BackKey)


MainKey = [
    [
        InlineKeyboardButton("راهنمای استفاده از ربات 👨‍🏫",
                             callback_data="help")
    ],
    [
        InlineKeyboardButton("مشاهده حساب 🏦", callback_data="account")
    ]
]
MainKey = InlineKeyboardMarkup(MainKey)


AccountMenu = [
    [
        InlineKeyboardButton("خرید اشتراک ویژه", callback_data="get_prem")
    ],
    [
        InlineKeyboardButton("برگشت به منو اصلی 🏡",
                             callback_data="back_to_main")
    ]
]
AccountMenu = InlineKeyboardMarkup(AccountMenu)


BuyMenu = [
    [
        InlineKeyboardButton("3 ماه : 49,000 تومان",
                             url='https://zarinp.al/544899')
    ],
    [
        InlineKeyboardButton("برگشت به منو اصلی 🏡", callback_data="account")
    ]
]
BuyMenu = InlineKeyboardMarkup(BuyMenu)


#  ########################################## Admin keyboards ##########################################
def admin_payment_menu(chat_id):
    keyboard = [
        [
            InlineKeyboardButton(
                "3 month", callback_data=f"month_3_{chat_id}"),
            InlineKeyboardButton(
                "1 month", callback_data=f"month_1_{chat_id}"),
            InlineKeyboardButton("none", callback_data=f"month_0_{chat_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


AdminMainKey = [
    [
        InlineKeyboardButton("send to all", callback_data='sendtoall')
    ],
    [
        InlineKeyboardButton("send data base", callback_data='getdb')
    ],
    [
        InlineKeyboardButton('view thread list',
                             callback_data='view_threadlist')
    ]
]
AdminMainKey = InlineKeyboardMarkup(AdminMainKey)

#  ########################################## MTPROTO keyboards ##########################################
SponsorKeyboard_mtproto = [
    [
        Button.url(item, Sponsor[item]) for item in Sponsor.keys()
    ]
]
