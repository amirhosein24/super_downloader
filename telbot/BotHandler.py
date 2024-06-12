

import credentials.creds as creds
import database.DataBase as db

import asyncio
from os import remove, path, listdir, rename

from telbot import keyboards, sender, channel

from telethon import TelegramClient, events


home = path.dirname(path.realpath(__file__)) + "/"

client = TelegramClient(
    home+"all_downer", api_id=creds.ApiId, api_hash=creds.ApiHash)


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    try:
        chat_id = event.chat_id
        user = await event.get_sender()
        username = user.username
        firstname = user.first_name
        lastname = user.last_name

        if db.add_user(int(chat_id), username, firstname, lastname):
            await client.send_message(creds.Admin, f"bot started by: `{chat_id}`\nname: {firstname}-{lastname}\nusername: @{username}")

        if not channel.is_member(client, chat_id):
            await event.repond('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', buttons=keyboards.ForceJoinKeyboard)
            return

        await event.reply(f"سلام {firstname}, به ربات دانلودر خوش آومدین\n لینک فایل یا پست شبکه اجتماعی مد نظرت رو بفرست تا برات دانلودش کنم ╰(*°▽°*)╯")
    except Exception as error:
        await client.send_message(creds.Admin, f"Error in thread_start by {chat_id}\nerror : \n{error}")


@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.reply("how to use the bot : \n\n ....")
    if not channel.is_member(client, event.chat_id):
        await event.reply('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)')
        return


@client.on(events.NewMessage(pattern='/premium'))
async def premium(event):
    await event.reply("با خرید اشتراک شما میتوانید هر فایلی با هر حجمی رو دانلود کنید")
    await event.reply("لطفا بعد از خرید از صفحه انجام تراکنش یا پیام برداشت از حساب عکس گرفته و برای ربات بفرستید تا حساب شما شارژ شود.")


@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        chat_id = event.chat_id
        link = event.raw_text

        if not channel.is_member(chat_id):
            await event.respond('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', buttons=keyboards.ForceJoinKeyboard)
            return

    except Exception as error:
        await event.respond('ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم')
        await client.send_message(creds.Admin, f'error in link_manager by:{chat_id}\n==============\nerror:\n{error}\n==============\nlink:\n{link}')

    finally:
        pass


@client.on(events.CallbackQuery())
async def callback_handler(event):

    query = event.data
    chat_id = event.chat_id

    try:
        if query.data == 'joined':
            if channel.is_member(chat_id):
                await event.edit('ربات فعال شد الان میتونی استفاده کنی')

            else:
                await event.answer('جوین نشدی که :(')

        elif query.data.split("-")[0] == "youtube":
            pass

        elif chat_id == creds.Admin:
            if query.data == 'sendall':
                await client.send_message(chat_id, 'sent your text to sent to all users')

            elif query.data == "db":
                await client.send_file(chat_id, home+'db.sqlite')

            elif query.data.startswith("month"):
                month = int(query.data.split("-")[1])
                user = event.message.caption

                try:
                    db.add_prem(user, month)
                    if month == 0:
                        await client.send_message(user, f"اعتبار حساب شما افزایش پیدا نکرد، از صحت عکس ارسالی مطمئن شوید.")
                    else:
                        await client.send_message(user, f"حساب شما {month} ماه شارژ شد")
                    await event.edit(f"{query.data} added to {user}")

                except Exception as error:
                    await client.send_message(chat_id, f"error in add month\n error : {error}")

        elif command == "send_receipt":
            call_message_id = event.original_update.msg_id
            call_message = await client.get_messages(chat_id, ids=call_message_id)
            file_message_id = call_message.reply_to.reply_to_msg_id
            file_message = await client.get_messages(chat_id, ids=file_message_id)

            caption = f"chat_id:`{chat_id}`, username:@{event.sender.username}"
            await client.send_file(creds.Admin, file_message, buttons=keyboards.admin_get_pay(chat_id), caption=caption)
            await event.edit(creds.Text["user_text"]["wait_for_admin"], buttons=keyboards.MainKey)

    except Exception as error:
        print(error)
        await client.send_message(chat_id, "ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
        await client.send_message(creds.Admin, f"error in call back manager by {chat_id}\nerror:\n{error}")


def go_live():
    client.start(bot_token=creds.BotToken)
    print("going live... ,returns error if unsuccesfull")
    client.run_until_disconnected()
