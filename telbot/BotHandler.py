


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

        if not channel.channel_checker(client, chat_id):
            await event.reply('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)')
            return

        await event.reply(f"سلام {firstname}, به ربات دانلودر خوش آومدین\n لینک فایل یا پست شبکه اجتماعی مد نظرت رو بفرست تا برات دانلودش کنم ╰(*°▽°*)╯")
    except Exception as error:
        await client.send_message(admin_chat_id, f"Error in thread_start by {chat_id}\nerror : \n{error}")


@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.reply("how to use the bot : \n\n ....")
    if not methods.channel_checker(client, event.chat_id):
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

        if not methods.channel_checker(chat_id):
            await event.respond('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', buttons=keyboards.ForceJoinKeyboard)
            return

        # twitter section
        elif (link.startswith("https://x.com") or link.startswith("https://twitter.com")):
            wait_message = await event.respond('در حال پردازش ...')
            url, caption = methods.create_url(link)
            if not url:
                await wait_message.edit('داخل این لینک هیچ فیلمی پیدا نکردم')
                return
            await wait_message.edit('داره دانلود میشه صبر کن یکم ...')
            file_names = [
                f"{home}cache/twitter/{chat_id}_{item}.mp4" for item in range(len(url))]
            i = 0
            for item in url:
                methods.download_video(item, file_names[i])
                i += 1
            await wait_message.edit('دانلود شد, الان میفرستمش برات')
            if len(file_names) == 1:  # if its one video in the tweet
                await client.send_file(chat_id, file_names[0], caption=caption)
            else:  # if its a group video
                await client.send_file(chat_id, file_names, caption=caption)
            await wait_message.delete()
            await event.respond('''（づ￣3￣）づ╭❤️～''', buttons=keyboards.SponsorKeyboard)
            db.AddUsageNum(chat_id)

        # youtube section
        elif link.startswith("https://www.youtube.com") or link.startswith("https://youtu.be") or link.startswith("https://youtube.com"):
            wait_message = await event.respond('در حال پردازش ...')
            data, working = methods.youtube_getinfo(link)
            if data and working:
                await wait_message.edit(f'{data["title"]}\nlength : {data["length"]}', buttons=keyboards.CreateKey(data))
            elif not working:
                await wait_message.edit('this video cant be downloaded')
                await client.send_message(creds.Admin, data)

        # instagram section
        elif link.startswith("https://www.instagram.com") or link.startswith("https://instagram.com"):
            wait_message = await event.respond('در حال حاضر دانلود اینستاگرام غیر فعال میباشد.')
            file_list, caption = methods.download_insta(chat_id, link)
            await client.send_file(chat_id, file_list, caption=caption)
            await event.respond('''（づ￣3￣）づ╭❤️～''', buttons=keyboards.SponsorKeyboard)
            await wait_message.delete()

        # direct download from internet
        else:
            try:
                file_size = methods.get_file_size(link)
            except:
                await event.respond('لینک درست شناسایی نشد, از صحت لینک دانلود فایل مطمن شوید')
                return

            if file_size > 1024:
                await event.respond('در حال حاضر دانلود فایل های بیشتر از یک گیگابایت ممکن نمی باشد.')
                return

            wait_message = await event.respond('در حال دانلود ...')
            file = methods.downloader(link)
            await wait_message.edit('فایل دانلود شد,  در حال آپلود ...')
            await client.send_file(chat_id, home + "cache/other/" + file)
            await event.respond('''（づ￣3￣）づ╭❤️～''', buttons=keyboards.SponsorKeyboard)
            await wait_message.delete()

    except Exception as error:
        await event.respond('ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم')
        await client.send_message(creds.Admin, f'error in link_manager by:{chat_id}\n==============\nerror:\n{error}\n==============\nlink:\n{link}')

    finally:
        pass


async def file_sender(chat_id, file_path, caption=None):

    if caption:
        caption = f"{caption}\n\n<a href='https://t.me/x_downloadbot'>Downloader Bot | ربات دانلودر </a>"
    else:
        caption = "<a href='https://t.me/x_downloadbot'>Downloader Bot | ربات دانلودر </a>"

    attributes = [DocumentAttributeVideo(
        duration=3, w=1280, h=720, supports_streaming=True)]

    try:
        await client.send_message(chat_id, message=caption, parse_mode='html', link_preview=False, file=file_path, attributes=attributes)
    except Exception as error:
        await client.send_message(chat_id, "ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
        await client.send_message(creds.Admin, f"error in file_sender by {chat_id}\nerror:\n{error}")
        print(error)

    finally:
        if isinstance(file_path, list):
            for file in file_path:
                if path.exists(file):
                    remove(file)
        else:
            if path.exists(file_path):
                remove(file_path)


@client.on(events.CallbackQuery())
async def callback_handler(event):
    query = event.data
    chat_id = event.chat_id

    try:
        if query.data == 'joined':
            if methods.channel_checker(chat_id):
                await event.edit('ربات فعال شد الان میتونی استفاده کنی')

                if not (event.message.reply_to_message.text).startswith("/start"):
                    await thread_link_manager(event)
            else:
                if chat_id == creds.Admin:
                    await event.answer('اوففف ادمینن')
                    await client.send_message(chat_id, 'choose command:', buttons=keyboards.AdminKeyboard)
                else:
                    await event.answer('جوین نشدی که :(')

        elif query.data.split("-")[0] == "youtube":
            generator = methods.youtube_getvideo(
                event.message.reply_to_message.text, query.data.split("-")[1])
            if next(generator) > 1024:
                await client.send_message(chat_id, 'در حال حاضر دانلود فایل های بیشتر از یک گیگابایت ممکن نمی باشد.')
                return

            await event.edit('دانلود شروع شد ...')
            file_path, title = next(generator)
            await event.edit('دانلود تمام شد , در حال آپلود...')
            await run_filesender(file_sender(chat_id, file_path, title))
            await client.send_message(chat_id, '（づ￣3￣）づ╭❤️～', buttons=keyboards.SponsorKeyboard)
            await client.delete_messages(chat_id, [event.message.id])
            if path.isfile(file_path):
                remove(file_path)

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

    except Exception as error:
        print(error)
        await client.send_message(chat_id, "ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
        await client.send_message(creds.Admin, f"error in call back manager by {chat_id}\nerror:\n{error}")


@client.on(events.NewMessage)
async def thread_forward(event):
    chat_id = event.chat_id

    try:




        if event.photo:
            photo_id = event.photo.id
            pic = await client.send_file(creds.Admin, event.photo, caption=chat_id, reply_markup=keyboards.admin_addmenu)
            if event.message.message:
                await client.send_message(creds.Admin, event.message.message, reply_to=pic)
            await event.respond("در حال برسی, چند دقیقه صبر کنید ...", reply_to=event.message, buttons=keyboards.RemoveKeys)
        else:
            await event.respond("مشکلی در سیستم پیش آمد, لطفا دوباره تلاش کنید.")
    except Exception as error:
        await event.respond("مشکلی در سیستم پیش آمد, لطفا دوباره تلاش کنید.")
        await client.send_message(creds.Admin, f"error in thread forward by {event.message.message}\nerror : {error}")


def go_live():
    client.start(bot_token=creds.BotToken)
    print("going live... ,returns error if unsuccesfull")
    client.run_until_disconnected()
