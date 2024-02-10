
import creds
import methods
import keyboards
import DataBase as db

from os import remove, getcwd, listdir
from time        import sleep
from telegram import InputMediaVideo
from threading              import Thread, enumerate
from telegram.ext           import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


""" TODO
complete threading , one at time to upload for a preson
better detail
ad
after query cheking automatically does the job that was asked
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


            if db.add_user(int(chat_id), username, firstname, lastname):
                context.bot.send_message(chat_id=creds.Admin, text=f"bot started by:\nchat_id: {chat_id}\nname: {firstname}-{lastname}\nusername: @{username}")               
            if not methods.channel_checker(context, chat_id):
                update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard, reply_to_message_id=update.message.message_id)
                return
            update.message.reply_text(f"سلام {firstname}, به ربات دانلودر توییتر خوش آومدی \nلینک توییتت رو بفرست اینجا تا برات فیلمشو بفرستم")
        except Exception as error:
            context.bot.send_message(chat_id=creds.Admin, text=f"Error in thread_start by {chat_id}\nerror : \n{error}")



def thread_help(update, context):
        update.message.reply_text("how to use the bot : \n\n ....")
        if not methods.channel_checker(context, update.message.chat_id):
            update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard, reply_to_message_id=update.message.message_id)
            return



def thread_link_manager(update, context):

    try:
        chat_id = update.message.chat_id
        link    = update.message.text

        if not methods.channel_checker(context, chat_id):
            update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard, reply_to_message_id=update.message.message_id)
            return
        
        if not (link.startswith("https://x.com") or link.startswith("https://twitter.com")):        
            update.message.reply_text("لینک توییتر رو برام بفرست :(")
            return

        url, caption = methods.create_url(context, link)

        if not url:
            update.message.reply_text("مطمنی لینکی که فرستادی درسته ؟ ") 
            return

        wait = context.bot.send_message(chat_id=chat_id, text="داره دانلود میشه صبر کن یکم ...")
        nameist = [f"cache/{chat_id}_{item}.mp4" for item in range(len(url))]

        i = 0
        for item in url:
            methods.download_video(item, nameist[i])
            i += 1

        context.bot.edit_message_text(chat_id=chat_id, message_id=wait.message_id, text="دانلود شد, الان میفرستمش برات")
        
        if len(nameist) == 1:
            context.bot.send_video(chat_id=chat_id, video=open(nameist[0], 'rb'), caption=caption, reply_markup=keyboards.SponsorKeyboard)
        else:
            media_files = []
            lastitem = nameist.pop()
            media_files.append(InputMediaVideo(open(lastitem, "rb"), caption=caption))            

            for item in nameist:
                media_files.append(InputMediaVideo(open(item, 'rb')))
            context.bot.send_media_group(chat_id=chat_id, media=media_files)

        context.bot.deleteMessage(chat_id=chat_id, message_id=wait.message_id)
        db.AddUsageNum(chat_id)

    except Exception as error:
        context.bot.send_message(chat_id=creds.Admin, text=f"error in link_manager by {chat_id}\nerror:\n{error}")
        context.bot.send_message(chat_id=chat_id, text="ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")

    finally:
        for file in listdir(getcwd()+"/cache/"):
            if str(file).startswith(str(chat_id)):
                remove("cache/"+file)


def thread_callback(update, context):

        query = update.callback_query

        if query.data == 'joined':
            if methods.channel_checker(context, query.message.chat_id):
                query.edit_message_text("ربات فعال شد الان میتونی استفاده کنی ")
                # thread_link_manager(query, context)
                # print(query.message.reply_to_message.text)
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