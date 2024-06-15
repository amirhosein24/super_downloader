
from downloaders import youtube_downer, insta_downer, twitter_downer, direct_downer, spotify_downer
from telbot import keyboards

from threading import Lock, Thread
import asyncio

var_lock = Lock()
thread_list = []


def thread_handler(update, context):
    chat_id = update.effective_chat.id

    with var_lock:
        if chat_id in thread_list:
            update.message.reply_text("waint dudeeeeeeee", reply_to_message_id=update.message.message_id)
            return
        else:
            thread_list.append(chat_id)
            Thread(target=link_handler, args=(update, context, )).start()


def link_handler(update, context):
    try:

        link = update.message.text
        chat_id = update.message.chat_id

        if link.startswith("https://www.youtube.com"):
            waitmessage = update.message.reply_text("its you tubeeeeee, wait", reply_to_message_id=update.message.message_id)
            data = youtube_downer.getinfo(link)
            title, length = data["title"], data["length"]
            context.bot.edit_message_text(chat_id=chat_id, message_id=waitmessage.message_id, text=f"کیفیت دانلود خود را انتخاب کنید : \n{title}: {length}", reply_markup=keyboards.youtube_key(link, data))

        elif link.startswith("https://www.instagram.com"):

            waitmessage = update.message.reply_text("insta yooooooooo", reply_to_message_id=update.message.message_id)

            fileoo = insta_downer.instagram(chat_id, link)

        elif link.startswith("https://x.com/") or link.startswith("https://twitter.com/"):

            waitmessage = update.message.reply_text("twiterrrr yooooo", reply_to_message_id=update.message.message_id)
            filess = twitter_downer.create_url(context, chat_id, link)

            print(filess)

        elif link.startswith("https://open.spotify.com/"):

            track_id = link.split('/')[-1]
            if '?' in track_id:
                track_id = track_id.split('?')[0]

            details = spotify_downer.get_track_details(track_id)

            waitmessage = update.message.reply_text(details, reply_to_message_id=update.message.message_id)

            filepath = spotify_downer.spot_download(track_id)

            print(filepath)

        else:
            file_size = direct_downer.get_file_size(link)





    except Exception as e:
        print(e)

    finally:
        with var_lock:
            if chat_id in thread_list:
                thread_list.remove(chat_id)


def youtube_callback(update, context):

    query = update.callback_query
    chat_id = query.from_user.id

    try:
        query = update.callback_query
        chat_id = query.from_user.id
        _, tag, link = query.data.split("-")

        with var_lock:
            if chat_id in thread_list:
                query.answer("waittoooooo")
                return

            thread_list.append(chat_id)

        fil0 = youtube_downer.download(link, tag)
        print(fil0)

    except Exception as e:
        print(e)

    finally:
        with var_lock:
            if chat_id in thread_list:
                thread_list.remove(chat_id)


async def send_to(client, chat_id, file_path, caption, duration):

    with open(file_path, 'rb') as file:
        uploaded_file = await client.upload_file(file, part_size_kb=20_480, timeout=15, max_retries=4)

    await client.send_file(chat_id, uploaded_file, caption=caption, attributes=[('duration', duration)], force_document=False)
