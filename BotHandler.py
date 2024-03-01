
import creds
import methods
import keyboards
import DataBase as db


from time import sleep
from os import remove, path



from telethon.tl.types import DocumentAttributeVideo
from telethon import TelegramClient
from telegram import InputMediaVideo
from threading import Thread, enumerate
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from asyncio import new_event_loop, set_event_loop



home = path.dirname(path.realpath(__file__))






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

            wait_message = context.bot.send_message(chat_id=chat_id, text="داره دانلود میشه صبر کن یکم ...", reply_to_message_id=update.message.message_id)



            file_names = [f"{home}/cache/twitter/{chat_id}_{item}.mp4" for item in range(len(url))]
  
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




        elif link.startswith("https://www.youtube.com") or link.startswith("https://youtu.be") or link.startswith("https://youtube.com"):      # youtube section

            wait_message = context.bot.send_message(chat_id=chat_id, text="در حال پردازش ...", reply_to_message_id=update.message.message_id)

            data, working = methods.youtube_getinfo(link)

            if data and working:
                context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text=data["title"] + "\nlength : " + data["length"], reply_markup=keyboards.CreateKey(data))
            elif not working:

                context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="this video cant be downloaded")
                context.bot.send_message(chat_id=creds.Admin, text=data)



    except Exception as error:
        
        context.bot.send_message(chat_id=chat_id, text="ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
        context.bot.send_message(chat_id=creds.Admin, text=f"error in link_manager by {chat_id}\nerror:\n{error}")


    finally:
        pass 
        # try: TODO
        #     for file in listdir(__file__[:-13]+"/cache/"):
        #         if str(file).startswith(str(chat_id)):
        #             remove(__file__[:-13]+"/cache/"+file)
        # except:
        #     pass




async def file_sender(chat_id, file_path, caption, duration):
    try : 
        async with TelegramClient("telethon", creds.ApiId, creds.ApiHash) as client:
            attributes = [DocumentAttributeVideo(duration=duration, w=1280, h=720)]
            await client.send_file(chat_id, file_path, attributes=attributes, caption=caption)    #TODO all formats files video audio ...


    except Exception as error:
        print("error in file sender", str(error))
    finally:

        if path.isfile(file_path):
            remove(file_path)


def run_in_thread(coro):
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(coro)









def thread_callback(update, context):

        query = update.callback_query
        chat_id = query.message.chat_id
        command = query.data


        try:

            if command == 'joined':
                if methods.channel_checker(context, chat_id):
                    query.edit_message_text("ربات فعال شد الان میتونی استفاده کنی ")
                    # thread_link_manager(query, context)
                    # print(query.message.reply_to_message.text)
                else:
                    if chat_id == creds.Admin :
                        query.answer("اوففف ادمینن")        
                        query.message.reply_text('choose command :', reply_markup=keyboards.AdminKeyboard)
                    else:
                        query.answer("جوین نشدی که :(")        

            elif command.split("-")[0] == "youtube" :   # youtube manager

                query.edit_message_text("دانلود شروع شد ...")
                file_path, title, duration = methods.youtube_getvideo(query.message.reply_to_message.text, command.split("-")[1])
    
                query.edit_message_text("دانلود تمام شد , در حال آپلود...")

                run_in_thread(file_sender(chat_id, file_path, title, duration))
                
                context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)



            # if admin  #TODO bring admin down
            elif chat_id == creds.Admin :
    
                if command == 'sendall': #TODO complete this section
                    admin_command = "sendall"
                    query.message.reply_text('sent your text to sent to all users ')

                elif command == "db":
                    context.bot.send_document(chat_id=chat_id, document=open(home+'db.sqlite', "rb"))

                return

        except Exception as error:     
            context.bot.send_message(chat_id=chat_id, text="ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
            context.bot.send_message(chat_id=creds.Admin, text=f"error in link_manager by {chat_id}\nerror:\n{error}")
           
           
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