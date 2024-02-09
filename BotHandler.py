
import methods
import keyboards
import DataBase as db
import creds

from os import remove

from time        import sleep
from threading              import Thread, enumerate
from telegram.ext           import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telegram import InputMediaVideo


""" TODO
complete threading , one at time to upload for a preson
better detail
ad
caption

"""



def active_thread(name):
    for thread in enumerate():
        if thread.name == name and thread.is_alive():
            return True
    return False

def thread_start(update, context): 
        try:

            chat_id   = update.message.chat_id
            username  = update.message.chat.username
            firstname = update.message.chat.first_name
            lastname  = update.message.chat.last_name

            update.message.reply_text(f"hi {firstname}, go on")

            if db.add_user(int(chat_id), username, firstname, lastname):
                context.bot.send_message(chat_id=creds.Admin, text=f"bot started by:\nchat_id: {chat_id}\nname: {firstname}-{lastname}\nusername: @{username}")               
            if not methods.channel_checker(context, chat_id):
                update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard)

        except Exception as error:
            context.bot.send_message(chat_id=creds.Admin, text=f"Error in thread_start by {chat_id}\nerror : \n{error}")









def thread_help(update, context):
        update.message.reply_text("how to use the bot : \n\n ....")
        # if not check.check_membership(context, join_channel_id, update.message.chat_id):
        #     update.message.reply_text('لطفا برای استفاده از ربات در کانال اسپانسر ما جوین شوید. :)', reply_markup=InlineKeyboardMarkup(channel_keyboard))




def thread_link_manager(update, context):

    try:
        chat_id = update.message.chat_id
        link    = update.message.text

        if not methods.channel_checker(context, chat_id):
            update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard)
            return
        if not (link.startswith("https://x.com") or link.startswith("https://twitter.com")):        
            update.message.reply_text("use tweeter link bitch ")
            return

        url, caption = methods.create_url(context, link)

        if not url:
            update.message.reply_text("use correct link and only tweeter link") 
            return

        wait = context.bot.send_message(chat_id=chat_id, text="downloading ....")
        nameist = [f"cache/{chat_id}_{item}.mp4" for item in range(len(url))]

        i = 0
        for item in url:
            methods.download_video(item, nameist[i])
            i += 1
        context.bot.edit_message_text(chat_id=chat_id, message_id=wait.message_id, text="downloaded, uploading... ")

        media_files = [InputMediaVideo(open(file, 'rb')) for file in nameist]

        medgroup = context.bot.send_media_group(chat_id=chat_id, media=media_files)
        # context.bot.send_media_group(chat_id=chat_id, media=media_files, caption=caption, parse_mode=ParseMode.HTML)

        if caption:
            context.bot.send_message(chat_id=chat_id, text=caption, reply_to_message_id=medgroup[0].message_id)

        for file in nameist:
            remove(file)
        db.AddUsageNum(chat_id)

    except Exception as error:
        context.bot.send_message(chat_id=creds.Admin, text=f"error in link_manager by {chat_id}\nerror:\n{error}")
        context.bot.send_message(chat_id=chat_id, text="error happend")








def thread_callback(update, context):

        query = update.callback_query

        if query.data == 'joined':
            if methods.channel_checker(context, query.message.chat_id):
                query.edit_message_text("go onnnnnn use the bot bitch")
            else:
                query.answer("جوین نشدی که :(")        




#########################################################################################
#########################################################################################


def start(update, context):
    Thread(target=thread_start, args=(update, context, )).start()

def link_manager(update, context):
    if not active_thread(update.message.chat_id):
        Thread(target=thread_link_manager, args=(update, context, ), name=update.message.chat_id).start()

def help(update, context):
    Thread(target=thread_help, args=(update, context, )).start()

def callback(update, context):
    Thread(target=thread_callback, args=(update, context, )).start()

def go_live():
    print("going live...")
    while True:
        try:
            updater = Updater(token=creds.BotToken, use_context=True)#, request_kwargs={'proxy_url': 'socks5://localhost:2080'}
            updater.dispatcher.add_handler(CommandHandler('start', start))
            updater.dispatcher.add_handler(CommandHandler('restart', start))
            updater.dispatcher.add_handler(CommandHandler('help', help))
            updater.dispatcher.add_handler(CallbackQueryHandler(callback))
            updater.dispatcher.add_handler(MessageHandler(Filters.text, link_manager))
            updater.start_polling()     
            print("bot is live.")
            break
        except Exception as e:
            print(f"Error. Retrying in 10 sec ... : {e}")
            sleep(10)


go_live()