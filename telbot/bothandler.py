

import database.DataBase as db
from telbot import keyboards, channel
from credentials.creds import Admin, BotToken, ApiId, ApiHash, Home

from telethon import TelegramClient, events

client = TelegramClient(Home+"all_downer", api_id=ApiId, api_hash=ApiHash)
del ApiId, ApiHash, Home


@client.on(events.NewMessage(pattern='/start', func=lambda element: element.is_private))
async def start_handler(event):
    chat_id = event.sender.id

    try:
        if db.add_user(
                chat_id,
                event.sender.first_name,
                event.sender.last_name,
                event.sender.username
        ):
            log_text = f"chat_id: `{chat_id}`\nname: {event.sender.first_name}-{event.sender.last_name}\nusername: @{event.sender.username}"
            await client.send_message(Admin, log_text)

            # try:
            #     if len(event.message.message) != len("/start"):
            #         inviter = event.message.message[len("/start") + 1:]
            #         invited_number = db.handle_invite(inviter, True)
            #         if invited_number % 3 == 0:
            #             db.handle_prem_time(inviter, 1800)
            #             await client.send_message(int(inviter), creds.Text["user_text"]["invited"], buttons=keyboards.BackMainKey)
            # except:
            #     pass

        if await channel.is_member(client, chat_id):
            await event.respond(f"wellcome to our bot")
        else:
            await event.respond("hosde", buttons=keyboards.join_channel_key())

    except Exception as error:
        from traceback import extract_tb
        tb = extract_tb(error.__traceback__)
        await client.send_message(Admin, f"Error occurred in bothandler.start_handler, line:{tb[-1].lineno}\nerror:\n\n{error}")


@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    await event.reply("how to use the bot : \n\n ....")
    if not await channel.is_member(client, event.chat_id):
        await event.reply('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)')
        return

# @client.on(events.NewMessage(func=lambda element: element.is_private and not element.message.out))
# async def my_event_handler(event):
#     try:
#         chat_id = event.chat_id
#         link = event.raw_text
#         if not channel.is_member(chat_id):
#             await event.respond('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', buttons=keyboards.ForceJoinKeyboard)
#             return
#     except Exception as error:
#         await event.respond('ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم')
#         await client.send_message(creds.Admin, f'error in link_manager by:{chat_id}\n==============\nerror:\n{error}\n==============\nlink:\n{link}')
#
#     finally:
#         pass


@client.on(events.CallbackQuery())
async def callback_handler(event):

    chat_id = event.sender.id
    command = event.data.decode("utf-8")

    try:
        if command == 'joined':
            if await channel.is_member(client, chat_id):
                await event.edit('ربات فعال شد الان میتونی استفاده کنی')
            else:
                await event.answer('جوین نشدی که :(')

        elif command.split("-")[0] == "youtube":
            pass

    except Exception as error:
        from traceback import extract_tb
        tb = extract_tb(error.__traceback__)
        await client.send_message(Admin, f"Error occurred in main_bot.callback_handler, line:{tb[-1].lineno}\nerror:\n\n{error}")
        await event.respond("مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


def go_live():
    client.start(bot_token=BotToken)
    print("going live... ,returns error if unsuccesfull")
    client.run_until_disconnected()
