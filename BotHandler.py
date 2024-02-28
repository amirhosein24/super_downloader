
import creds
import methods
import keyboards
import DataBase as db


from time import sleep
from os import remove, listdir, path
from telethon import TelegramClient
from telegram import InputMediaVideo
from threading import Thread, enumerate
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import asyncio

""" TODO
rewrite thread link
better detail
after query cheking automatically does the job that was asked
"""

home = path.dirname(path.realpath(__file__))



# bot = TelegramClient(home + 'telethon', creds.ApiId, creds.ApiHash).start(bot_token=creds.BotToken)


import asyncio
import threading












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
            update.message.reply_text(f"سلام {firstname}, به ربات دانلودر توییتر خوش آومدی \nلینک توییتت رو بفرست اینجا تا برات فیلم هاشو بفرستم")
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
        





        if (link.startswith("https://x.com") or link.startswith("https://twitter.com")):      # twitter section


            url, caption = methods.create_url(context, link)

            if not url:
                update.message.reply_text("داخل این لینک هیچ فیلمی پیدا نکردم") 
                return

            wait_message = context.bot.send_message(chat_id=chat_id, text="داره دانلود میشه صبر کن یکم ...")
            file_names = [f"{__file__[:-13]}/cache/{chat_id}_{item}.mp4" for item in range(len(url))]

            i = 0
            for item in url:
                methods.download_video(item, file_names[i])
                i += 1

            context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="دانلود شد, الان میفرستمش برات")
            
            if len(file_names) == 1: # if its one video in the tweet
                context.bot.send_video(chat_id=chat_id, video=open(file_names[0], 'rb'), caption=caption, reply_markup=keyboards.SponsorKeyboard)
            else: # if its a group video
                media_files = []
                lastitem = file_names.pop()
                media_files.append(InputMediaVideo(open(lastitem, "rb"), caption=caption))            

                for item in file_names:
                    media_files.append(InputMediaVideo(open(item, 'rb')))
                context.bot.send_media_group(chat_id=chat_id, media=media_files)
                
                context.bot.send_message(chat_id=chat_id, text="""
                                                                ( •_•)                       (•_• )
                                                                ( ง )ง                       ୧( ୧ )
                                                                /︶\                          /︶\\
                                                                """, reply_markup=keyboards.SponsorKeyboard)


            context.bot.deleteMessage(chat_id=chat_id, message_id=wait_message.message_id)
            db.AddUsageNum(chat_id)





        if (link.startswith("https://www.youtube.com") or link.startswith("https://youtu.be")):      # youtube section




            # Create a thread to run the coroutine
            thread = threading.Thread(target=run_in_thread, args=(file_sender(chat_id, "THE GARFIELD MOVIE Official Trailer (2024).mp4"),))
            thread.start()


            print("gogogogogo")



            wait_message = context.bot.send_message(chat_id=chat_id, text="در حال پردازش ...")
            # data = methods.youtube_getinfo(link)
            # print(data)
            # context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text=data["title"] + "\nlength : " + data["length"])
            # context.bot.send_video(chat_id=chat_id, video=open(file_names[0], 'rb'), caption=caption, reply_markup=keyboards.SponsorKeyboard)
            # update.message.reply_text(data) 


    except Exception as error:
        print(error)

        # context.bot.send_message(chat_id=creds.Admin, text=f"error in link_manager by {chat_id}\nerror:\n{error}")
        # context.bot.send_message(chat_id=chat_id, text="ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
    finally:
        pass 
        # try: TODO
        #     for file in listdir(__file__[:-13]+"/cache/"):
        #         if str(file).startswith(str(chat_id)):
        #             remove(__file__[:-13]+"/cache/"+file)
        # except:
        #     pass



async def file_sender(chat_id, file_path):
    print("--------------------------------------------------------------------- ")
    async with TelegramClient("telethon", creds.ApiId, creds.ApiHash) as client:
        print("hhhhhhhhhhhhhhhhhhhhh")
        # client.start(bot_token=creds.BotToken)
        if str(file_path).endswith("mp4"):
            await client.send_video(chat_id, file_path) #TODO all formats files video audio ...
        else:
            await client.send_file(chat_id, file_path) #TODO all formats files video audio ...


def run_in_thread(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)













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
    if not active_thread(str(update.message.chat_id)): # makes user use one download at a time
        Thread(target=thread_link_manager, args=(update, context, ), name=str(update.message.chat_id)).start()

def help(update, context):
    Thread(target=thread_help, args=(update, context, )).start()

def callback(update, context):
    Thread(target=thread_callback, args=(update, context, )).start()

def go_live():
    print("going live...")
    while True:
        try:
            updater = Updater(token=creds.BotToken, use_context=True)
            updater.dispatcher.add_handler(CommandHandler('start', start))
            updater.dispatcher.add_handler(CommandHandler('restart', start))
            updater.dispatcher.add_handler(CommandHandler('help', help))
            updater.dispatcher.add_handler(CallbackQueryHandler(callback))
            updater.dispatcher.add_handler(MessageHandler(Filters.text, link_manager))
            updater.start_polling()     
            print("bot is live.")
            break
        except Exception as e:
            print(f"Retrying in 10 sec... Error: {e}")
            sleep(10)


if __name__ == "__main__":
    go_live()