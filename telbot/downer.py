
from downloaders import youtube_downer
from telbot import keyboards

from threading import Lock, Thread
import asyncio

var_lock = Lock()
thread_list = []


def thread_handler(update, context):
    chat_id = update.effective_chat.id

    with var_lock:
        if chat_id in thread_list:
            update.message.reply_text("waint dudeeeeeeee")
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
