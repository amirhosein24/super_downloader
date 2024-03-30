import creds
import methods
import keyboards
import DataBase as db

from time import sleep
from os import remove, path, listdir, rename

from asyncio import new_event_loop, set_event_loop
from threading import Thread, enumerate

from telethon.tl.types import DocumentAttributeVideo
from telethon import TelegramClient
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

home = path.dirname(path.realpath(__file__)) + "/"

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
            update.message.reply_text(f"سلام {firstname}, به ربات دانلودر خوش آومدین\n لینک فایل یا پست شبکه اجتماعی مد نظرت رو بفرست تا برات دانلودش کنم ╰(*°▽°*)╯")
        except Exception as error:
            context.bot.send_message(chat_id=creds.Admin, text=f"Error in thread_start by {chat_id}\nerror : \n{error}")

def thread_help(update, context):
        update.message.reply_text("how to use the bot : \n\n ....")
        if not methods.channel_checker(context, update.message.chat_id):
            update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard, reply_to_message_id=update.message.message_id)
            return

def thread_premium(update, context):
        update.message.reply_text("با خرید اشتراک شما میتوانید هر فایلی با هر حجمی رو دانلود کنید", reply_markup=keyboards.buymenu)
        update.message.reply_text(
            "لطفا بعد از خرید از صفحه انجام تراکنش یا پیام برداشت از حساب عکس گرفته و برای ربات بفرستید تا حساب شما شارژ شود.",
            reply_markup=keyboards.cancelbuy)


def thread_link_manager(update, context):

    try:
        chat_id = update.message.chat_id
        link    = update.message.text


        if link == "❌ لغو خرید ❌":
            update.message.reply_text(f"سلام {update.message.chat.first_name}, به ربات دانلودر توییتر خوش آومدی \nلینک توییتت رو بفرست اینجا تا برات فیلم هاشو بفرستم",
                                       reply_markup=keyboards.RemoveKeys)
            return
        
        if not methods.channel_checker(context, chat_id):
            update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.ForceJoinKeyboard, reply_to_message_id=update.message.message_id)
            return
        
        # twitter section
        elif (link.startswith("https://x.com") or link.startswith("https://twitter.com")):      

            wait_message = context.bot.send_message(chat_id=chat_id, text="در حال پردازش ...", reply_to_message_id=update.message.message_id)

            url, caption = methods.create_url(context, link)
            if not url:
                context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="داخل این لینک هیچ فیلمی پیدا نکردم")
                return
            
            context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="داره دانلود میشه صبر کن یکم ...")

            file_names = [f"{home}cache/twitter/{chat_id}_{item}.mp4" for item in range(len(url))]
            i = 0
            for item in url:
                methods.download_video(item, file_names[i])
                i += 1
            context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="دانلود شد, الان میفرستمش برات")
            if len(file_names) == 1: # if its one video in the tweet
                run_filesender(file_sender(chat_id, file_names[0], caption))
            else: # if its a group video
                run_filesender(file_sender(chat_id, file_names, caption))
            context.bot.deleteMessage(chat_id=chat_id, message_id=wait_message.message_id)
            context.bot.send_message(chat_id=chat_id, text="""（づ￣3￣）づ╭❤️～""", reply_markup=keyboards.SponsorKeyboard)
            db.AddUsageNum(chat_id)

        # youtube section
        elif link.startswith("https://www.youtube.com") or link.startswith("https://youtu.be") or link.startswith("https://youtube.com"):      
            wait_message = context.bot.send_message(chat_id=chat_id, text="در حال پردازش ...", reply_to_message_id=update.message.message_id)
            data, working = methods.youtube_getinfo(link)
            if data and working:
                context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text=data["title"] + "\nlength : " + data["length"], reply_markup=keyboards.CreateKey(data))
            elif not working:
                context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="this video cant be downloaded")
                context.bot.send_message(chat_id=creds.Admin, text=data)

        # instagram section
        elif link.startswith("https://www.instagram.com") or link.startswith("https://instagram.com"):      

            # context.bot.send_message(chat_id=chat_id, text="در حال حاضر دانلود اینستاگرام غیر فعال میباشد.", reply_to_message_id=update.message.message_id)

            wait_message = context.bot.send_message(chat_id=chat_id, text="در حال پردازش ...", reply_to_message_id=update.message.message_id)
            file_list, caption = methods.download_insta(chat_id, link)
            run_filesender(file_sender(chat_id, file_list, caption))
            context.bot.send_message(chat_id=chat_id, text="""（づ￣3￣）づ╭❤️～""", reply_markup=keyboards.SponsorKeyboard)
            context.bot.delete_message(chat_id=chat_id, message_id=wait_message.message_id)


        else:
            
            try:
                file_size = methods.get_file_size(link)
            except:
                context.bot.send_message(chat_id=chat_id, text="لینک درست شناسایی نشد, از صحت لینک دانلود فایل مطمن شوید")
                return

            if file_size > 100 and not db.is_prem(chat_id):
                context.bot.send_message(chat_id=chat_id, text="برای دانلود فایل ها با حجم بالاتر از ۱۰۰ مگابایت به اشتراک پریمیوم نیاز دارید\n از دستور /premium استفاده کنید")
                return
                
            wait_message = context.bot.send_message(chat_id=chat_id, text="در حال دانلود ...", reply_to_message_id=update.message.message_id)
            file = methods.downloader(link)
            context.bot.edit_message_text(chat_id=chat_id, message_id=wait_message.message_id, text="فایل دانلود شد,  در حال آپلود ...")
            run_filesender(file_sender(chat_id, home + "cache/other/" + file))
            context.bot.send_message(chat_id=chat_id, text="""（づ￣3￣）づ╭❤️～""", reply_markup=keyboards.SponsorKeyboard)
            context.bot.deleteMessage(chat_id=chat_id, message_id=wait_message.message_id)

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







async def file_sender(chat_id, file_path, caption=None):
    async with TelegramClient(home + "telethon", creds.ApiId, creds.ApiHash) as client:

    



        if caption:
            caption = f"{caption}\n\n<a href='https://t.me/x_downloadbot'>Downloader Bot | ربات دانلودر </a>"
        else:
            caption = "<a href='https://t.me/x_downloadbot'>Downloader Bot | ربات دانلودر </a>"


        attributes = [DocumentAttributeVideo(duration=3, w=1280, h=720, supports_streaming=True)]



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
 

def run_filesender(coro):
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

                    if not (query.message.reply_to_message.text).startswith("/start"): 
                        thread_link_manager(query, context)
                else:
                    if chat_id == creds.Admin :
                        query.answer("اوففف ادمینن")        
                        query.message.reply_text('choose command :', reply_markup=keyboards.AdminKeyboard)
                    else:
                        query.answer("جوین نشدی که :(") 

            elif command.split("-")[0] == "youtube" :   # youtube manager

                generator = methods.youtube_getvideo(query.message.reply_to_message.text, command.split("-")[1])

                if next(generator) > 100 and not db.is_prem(chat_id):
                    context.bot.send_message(chat_id=chat_id, text="برای دانلود فایل ها با حجم بالاتر از ۱۰۰ مگابایت به اشتراک پریمیوم نیاز دارید\n از دستور /premium استفاده کنید")
                    return

                query.edit_message_text("دانلود شروع شد ...")
                file_path, title = next(generator)    
                query.edit_message_text("دانلود تمام شد , در حال آپلود...")
                run_filesender(file_sender(chat_id, file_path, title))
                context.bot.send_message(chat_id=chat_id, text="""（づ￣3￣）づ╭❤️～""", reply_markup=keyboards.SponsorKeyboard)
                context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
                if path.isfile(file_path):
                    remove(file_path)

            # if admin  #TODO bring admin down
            elif chat_id == creds.Admin :
    
                if command == 'sendall': #TODO complete this section
                    admin_command = "sendall"
                    query.message.reply_text('sent your text to sent to all users ')

                elif command == "db":
                    context.bot.send_document(chat_id=chat_id, document=open(home+'db.sqlite', "rb"))

                elif command.startswith("month"):

                    month = int(command.split("-")[1])
                    user = query.message.caption
                    
                    try:
                        db.add_prem(user, month)
                        if month == 0 :
                            context.bot.send_message(chat_id=user, text=f"اعتبار حساب شما افزایش پیدا نکرد، از صحت عکس ارسالی مطمئن شوید.")
                        else:
                            context.bot.send_message(chat_id=user, text=f"حساب شما {month} ماه شارژ شد")
                        context.bot.edit_message_caption(chat_id=chat_id, caption=f"{query.data} added to {user}", message_id=query.message.message_id)
    
                    except Exception as error:
                        context.bot.send_message(chat_id=chat_id, text=f"error in add month\n error : {error}")

        except Exception as error:     
            print(error)
            context.bot.send_message(chat_id=chat_id, text="ی مشکلی پیش اومد ببشید, دوباره بفرست برام شاید تونستم")
            context.bot.send_message(chat_id=creds.Admin, text=f"error in call back manager by {chat_id}\nerror:\n{error}")
           


def thread_forward(update, context):

    chat_id = update.message.chat_id

    try:
        photo_id = update.message.photo[-1].file_id
        pic = context.bot.send_photo(chat_id=creds.Admin, photo=photo_id, caption=chat_id, reply_markup=keyboards.admin_addmenu)
        if update.message.caption:
            context.bot.send_message(chat_id=creds.Admin, text=update.message.caption, reply_to_message_id=pic.message_id)
        update.message.reply_text("در حال برسی, چند دقیقه صبر کنید ...", reply_to_message_id=update.message.message_id, reply_markup=keyboards.RemoveKeys)
        return

    except Exception as error:
        update.message.reply_text("مشکلی در سیستم پیش آمد, لطفا دوباره تلاش کنید.")
        context.bot.send_message(chat_id=creds.Admin, text=f"error in thread forward by {update.message.caption}\nerror : {error}")


###########################################################################################################################################################
###########################################################################################################################################################

def start(update, context):
    Thread(target=thread_start, args=(update, context, )).start()

def link_manager(update, context):
    if not active_thread(str(update.message.chat_id)): # makes user use one download at a time
        Thread(target=thread_link_manager, args=(update, context, ), name=str(update.message.chat_id)).start()
    else:
        update.message.reply_text("لطفا صبر کنید تا فایل قبل دانلود شود.")

def help(update, context):
    Thread(target=thread_help, args=(update, context, )).start()

def callback(update, context):
    Thread(target=thread_callback, args=(update, context, )).start()

def premium(update, context):
    Thread(target=thread_premium, args=(update, context, )).start()

def forward_photo(update, context):
    Thread(target=thread_forward, args=(update, context,)).start()

def go_live():
    print("going live...")
    while True:
        try:
            updater = Updater(token=creds.BotToken, use_context=True)
            updater.dispatcher.add_handler(CommandHandler('start', start))
            updater.dispatcher.add_handler(CommandHandler('restart', start))
            updater.dispatcher.add_handler(CommandHandler('help', help))
            updater.dispatcher.add_handler(CommandHandler('premium', premium))
            updater.dispatcher.add_handler(CallbackQueryHandler(callback))
            updater.dispatcher.add_handler(MessageHandler(Filters.photo, forward_photo))
            updater.dispatcher.add_handler(MessageHandler(Filters.text, link_manager))
            updater.start_polling()     
            print("bot is live.")
            break
        except Exception as e:
            print(f"Retrying in 10 sec... Error: {e}")
            sleep(10)

if __name__ == "__main__":
    go_live()