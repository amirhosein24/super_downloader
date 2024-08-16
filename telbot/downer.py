

from threading import Thread, RLock

from telbot import keyboards, uploader
from credentials.creds import Admin
from downloaders import youtube_downer, insta_downer, twitter_downer, direct_downer, spotify_downer


var_lock = RLock()
thread_list = {}


def thread_add(update, context):
    if update.callback_query:
        update = update.callback_query
        chat_id = update.from_user.id
    else:
        chat_id = update.message.chat.id

    try:
        acquired = var_lock.acquire(timeout=5)
        if not acquired:
            context.bot.send_message(Admin, f"{chat_id} - failed to acquire lock")
            update.message.reply_text('error happend, pls try again later.')
            return

        if chat_id in thread_list:
            update.message.reply_text('one download at a time')
            return
        else:
            thread_list[chat_id] = ""
            Thread(target=link_handler, args=(update, context, )).start()

    except Exception as error:
        context.bot.send_message(Admin, f"error in try var lock, error: {error}")
        update.message.reply_text('error happend, pls try again later.')
        return

    finally:
        var_lock.release()


def thread_manage(chat_id, pos):
    acquired = var_lock.acquire(timeout=5)
    if not acquired:
        return False
    try:
        thread_list[chat_id] = pos
        return True
    finally:
        var_lock.release()


def thread_remove(chat_id):
    acquired = var_lock.acquire(timeout=5)
    if not acquired:
        return False
    try:
        if chat_id in thread_list:
            del thread_list[chat_id]
        return True
    finally:
        var_lock.release()


def link_handler(update, context):
    try:

        link = update.message.text
        chat_id = update.message.chat_id
        files = None

        if link.startswith("https://www.youtube.com") or link.startswith("https://youtube.com") or link.startswith("https://youtu.be"):
            waitmessage = update.message.reply_text("its you tubeeeeee, wait", reply_to_message_id=update.message.message_id)
            data = youtube_downer.getinfo(link)
            title, length = data["title"], data["length"]
            context.bot.edit_message_text(chat_id=chat_id,
                                          message_id=waitmessage.message_id,
                                          text=f"کیفیت دانلود خود را انتخاب کنید : \n{title}: {length}",
                                          reply_markup=keyboards.youtube_key(link, data))

        elif link.startswith("https://www.instagram.com") or link.startswith("https://instagram.com"):
            waitmessage = update.message.reply_text("insta yooooooooo", reply_to_message_id=update.message.message_id)
            files, caption = insta_downer.instagram(context, chat_id, link)

        elif link.startswith("https://x.com/") or link.startswith("https://twitter.com/"):
            waitmessage = update.message.reply_text(
                "twiterrrr yooooo", reply_to_message_id=update.message.message_id)
            files, caption = twitter_downer.main_download(context, chat_id, link)

        elif link.startswith("https://open.spotify.com/"):
            waitmessage = update.message.reply_text("processing ...", reply_to_message_id=update.message.message_id)
            details, trackid = spotify_downer.get_track_details(link)
            context.bot.edit_message_text(chat_id=chat_id, message_id=waitmessage.message_id, text=details, reply_markup=keyboards.spotify_key(trackid))

        else:
            file_size = direct_downer.get_file_size(link)
            waitmessage = update.message.reply_text(
                f"file size is  {file_size}", reply_to_message_id=update.message.message_id)

        # if files:  # send the files after downloading them
        #     uploader.sender(chat_id, files, caption)
        #     context.bot.delete_message(chat_id, waitmessage.message_id)
        # else:
        #     context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=waitmessage.message_id, text="nothin found to download")

    except Exception as error:
        print(f"error in downer.link_handler, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")
        context.bot.send_message(
            Admin, f"error in downer.link_handler, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")

    finally:
        thread_remove(chat_id)


def download_callback(query, context):

    chat_id = query.from_user.id
    _, platform, tag, link = query.data.split("_")
    files, caption = [], ""

    try:
        if platform == "spotify":
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="download started ...")
            song = spotify_downer.spot_download(link, tag)
            if song:
                files.append(song)

        elif platform == "youtube":
            caption = query.message.text.split("\n")[1]
            # files = youtube_downer.download(chat_id, link, tag)

        if files:  # send the files after downloading them
            uploader.sender(chat_id, files, caption)
            context.bot.delete_message(chat_id, query.message.message_id)
        else:
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="nothin found to download")

    except Exception as error:
        print(f"--------{error}")
        context.bot.send_message(
            Admin, f"error in downer.download_callback, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")

    finally:
        thread_remove(chat_id)
