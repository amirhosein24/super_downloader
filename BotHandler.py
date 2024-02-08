
import methods
import keyboards
import DataBase as db
import creds

from os import remove

from time        import sleep
from threading              import Thread, enumerate
from telegram.ext           import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler





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

        if not link.startswith("https://x.com"):        
            update.message.reply_text("user tweeter link bitch ")
            return

        url = methods.create_url(link)
        if not url:
            update.message.reply_text("use correct link and only tweeter link") 
            return

        wait = context.bot.send_message(chat_id=chat_id, text="downloading ....")
        methods.download_video(url, chat_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=wait.message_id, text="downloaded, uploading... ")
        context.bot.send_video(chat_id=chat_id, video=open(f"cache/{chat_id}.mp4", 'rb'))
        remove(f"cache/{chat_id}.mp4")
        db.AddUsageNum(chat_id)

    except Exception as error:
        context.bot.send_message(chat_id=creds.Admin, text=f"error in link_manager by {chat_id}\nerror:\n{error}")
        context.bot.send_message(chat_id=chat_id, message_id=wait.message_id, text="error happend")








def thread_callback(update, context):

        query = update.callback_query

        if query.data == 'joined':
            if methods.channel_checker(context, query.message.chat_id):
                query.edit_message_text(" go onnnnnn use this bitch")
            else:
                query.answer("جوین نشدی که :(")        




#########################################################################################
#########################################################################################

def start(update, context):
    Thread(target=thread_start, args=(update, context, )).start()

def link_manager(update, context):
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
            # updater.dispatcher.add_handler(CommandHandler('admin', admin))
            updater.dispatcher.add_handler(CallbackQueryHandler(callback))
            updater.dispatcher.add_handler(MessageHandler(Filters.text, link_manager))
            updater.start_polling()     
            print("bot is live.")
            break
        except Exception as e:
            print(f"Error. Retrying in 10 sec ... : {e}")
            sleep(10)


go_live()