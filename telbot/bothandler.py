
import database.database as db
from telbot import keyboards, channel, downer
from creds import Admin, BotToken, Logger, Home

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


def admin_handler(update: Update, context: CallbackContext):
    if update.effective_chat.id == Admin:
        update.message.reply_text(
            f"admin yoooooooo", reply_markup=keyboards.AdminMainKey)


def start_handler(update: Update, context: CallbackContext):

    try:
        if db.add_user(
                update.effective_chat.id,
                update.effective_chat.first_name,
                update.effective_chat.last_name,
                update.effective_chat.username
        ):
            log_text = f"chat_id: {update.effective_chat.id}\nname: {update.effective_chat.first_name} - {update.effective_chat.last_name}\nusername: @{update.effective_chat.username}"
            context.bot.send_message(chat_id=Logger, text=log_text)

        if channel.is_member(update.effective_chat.id):
            update.message.reply_text(
                f"به ربات ابر دانلودر خوش اومدی, لینک پست رو بفرست تا دانلودش کنم و اینجا بفرستم.", reply_markup=keyboards.MainKey)
        else:
            update.message.reply_text(
                'لطفا برای استفاده از ربات در کانال ما عضو بشید. :)', reply_markup=keyboards.join_channel_key())

    except Exception as error:
        context.bot.send_message(
            chat_id=Admin, text=f"Error occurred in bothandler.start_handler, line:{error.__traceback__.tb_lineno}\nerror:\n\n{error}")
        update.message.reply_text(
            "مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        "how to use the bot : \n\n ....", reply_markup=keyboards.BackKey)


def link_handler(update: Update, context: CallbackContext):

    try:
        chat_id = update.effective_chat.id
        if chat_id == Logger:
            return

        link = update.message.text

        if not channel.is_member(chat_id):
            update.message.reply_text(
                'لطفا برای استفاده از ربات در کانال ما عضو بشید. :)', reply_markup=keyboards.join_channel_key())
            return

        downer.thread_add(update, context)

    except Exception as error:
        update.message.reply_text('ی مشکلی پیش اومد ببشید, دوباره بفرست ')
        context.bot.send_message(chat_id=Admin, text=f'error in bothandler.link_handler by:{chat_id}\nlink:\n{link}\nerror in line {error.__traceback__.tb_lineno}:\n{error}')


def callback_handler(update: Update, context: CallbackContext):

    query = update.callback_query
    chat_id = query.from_user.id
    command = query.data

    try:
        if command == 'joined':
            if channel.is_member(query.from_user.id):
                query.edit_message_text(
                    'به ربات ابر دانلودر خوش اومدی, لینک پست رو بفرست تا دانلودش کنم و اینجا بفرستم.', reply_markup=keyboards.MainKey)
            else:
                query.answer('عضو نشدی که :(')

        elif not channel.is_member(query.from_user.id):
            query.message.reply_text(
                'لطفا برای استفاده از ربات در کانال ما عضو بشید. :)', reply_markup=keyboards.join_channel_key())

        elif command == "help":
            query.edit_message_text(
                "نکات استفاده از ربات:  \n\n ....", reply_markup=keyboards.BackKey)

        elif command == "account":
            prem_till = db.handle_prem_till(chat_id)
            usagenum = db.usage_num(chat_id)
            usagesize = db.usage_size(chat_id)

            prem_till = "رایگان" if not prem_till else f"پریمیوم تا تاریخ {prem_till}"
            text = ("""حجم دانلود شده توسط شما : USAGESIZE مگابایت\n\nتعداد پست دانلود شده توسط شما : USAGENUM\n\nحالت حساب : PREM_TILL\n\nکد حساب شما : CHAT_ID""".
                    replace("CHAT_ID", str(chat_id)).
                    replace("PREM_TILL", prem_till).
                    replace("USAGESIZE", str(usagesize)).
                    replace("USAGENUM", str(usagenum)))
            query.edit_message_text(text, reply_markup=keyboards.AccountMenu)

        elif command == "back_to_main":
            query.edit_message_text(
                f"منو اصلی : ", reply_markup=keyboards.MainKey)

        elif command == "get_prem":
            query.edit_message_text(
                f"⭕️⭕️حتمی بعد از خرید از صفحه انجام تراکنش یا برداشت از حساب عکس گرفته و همین جا ارسال کنید تا حساب شما شارژ شود.⭕️⭕️", reply_markup=keyboards.BuyMenu)

        # ############################################ download callback handler
        elif command.startswith("dcb"):
            downer.download_callback(query, context)

        # ############################################ Admin section
        elif command.startswith("month"):
            _, month, chat_id = command.split("_")
            if month == "0":
                query.edit_message_caption(f"nothing was added to {chat_id}")
                context.bot.send_message(
                    chat_id=chat_id, text=f"اعتبار حساب شما افزایش پیدا نکرد. از درست بودن عکس ارسالی مطمن شوید.")

            else:
                prem_till = db.handle_prem_till(chat_id, add=int(month))
                query.edit_message_caption(f"{month} month added to {chat_id}, till : {prem_till}")
                context.bot.send_message(
                    chat_id=chat_id, text=f"حساب شما تا تاریخ حساب شما تا تاریخ {prem_till} شارژ شد.")
                context.bot.send_document(chat_id=Admin, document=open(
                    Home+"database/db.sqlite", "rb"))

        elif command == "view_threadlist":
            from telbot.downer import thread_list
            thread_message = context.bot.send_message(
                chat_id=Admin, text=str(thread_list))

        elif command == "getdb":
            context.bot.send_document(chat_id=Admin, document=open(
                Home+"database/db.sqlite", "rb"))

        elif command == "sendtoall":
            pass

    except Exception as error:
        context.bot.send_message(chat_id=Admin, text=f"Error occurred in main_bot.callback_handler, line:{error.__traceback__.tb_lineno}\nerror:\n\n{error}")
        query.message.reply_text(
            "مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


def photo_handler(update: Update, context: CallbackContext):
    try:
        chat_id = update.message.chat_id
        photo = update.message.photo[-1].file_id
        context.bot.send_photo(chat_id=Admin, photo=photo,
                               reply_markup=keyboards.admin_payment_menu(chat_id))
        update.message.reply_text(
            "پرداخت شما در اولین فرصت توسط پشتیبانی تایید میشود, بعد از تایید همین جا اعلام میشود.\n\nاز ارسال دوباره و یا تکراری خودداری کنید. 🔴\nبعضی وقتا پشتیبانی خوابه لطفا صبور باشید.", reply_to_message_id=update.message.message_id)

    except Exception as error:
        context.bot.send_message(chat_id=Admin, text=f"Error occurred in main_bot.photo_handler, line:{error.__traceback__.tb_lineno}\nerror:\n\n{error}")
        update.message.reply_text(
            "مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


updater = Updater(token=BotToken, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(CommandHandler('admin', admin_handler))
updater.dispatcher.add_handler(CommandHandler('help', help_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, link_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
