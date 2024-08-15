

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
            print(data)
            title, length = data["title"], data["length"]

            context.bot.edit_message_text(chat_id=chat_id,
                                          message_id=waitmessage.message_id,
                                          text=f"کیفیت دانلود خود را انتخاب کنید : \n{title}: {length}",
                                          reply_markup=keyboards.youtube_key(link, data))

        elif link.startswith("https://www.instagram.com") or link.startswith("https://instagram.com"):
            waitmessage = update.message.reply_text("insta yooooooooo", reply_to_message_id=update.message.message_id)
            files = insta_downer.instagram(chat_id, link)

        elif link.startswith("https://x.com/") or link.startswith("https://twitter.com/"):

            waitmessage = update.message.reply_text(
                "twiterrrr yooooo", reply_to_message_id=update.message.message_id)
            files, caption = twitter_downer.create_url(context, chat_id, link)

        elif link.startswith("https://open.spotify.com/"):
            track_id = link.split('/')[-1]
            if '?' in track_id:
                track_id = track_id.split('?')[0]
            details = spotify_downer.get_track_details(track_id)
            waitmessage = update.message.reply_text(
                details, reply_to_message_id=update.message.message_id, reply_markup=keyboards.spotify_key(link))

        else:
            file_size = direct_downer.get_file_size(link)
            waitmessage = update.message.reply_text(
                f"file size is  {file_size}", reply_to_message_id=update.message.message_id)

        if files:
            uploader.sender(chat_id, files, "caption")

    except Exception as e:
        print(f"error in link handler e:{e}")

    finally:
        thread_remove(chat_id)


def download_callback(update, context):

    query = update.callback_query

    chat_id = query.from_user.id
    command = query.data

    _, platform, tag, link = command.split("_")

    try:
        if platform == "spotify":
            pass

        elif platform == "youtube":
            caption = query.message.text.split("\n")[1]
            # files = youtube_downer.download(chat_id, link, tag)
            print(caption)
            uploader.sender(chat_id, r"C:\Users\amhei\Documenti\GitHub\telegram\super-downloader\downloaders\cache\lol Apple Intelligence is dumb....mp4", caption)

            context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)

    except Exception as e:
        print(f"--------{e}")

    finally:
        thread_remove(chat_id)
