
import database.database as db
from telbot import keyboards, channel, downer
from credentials.creds import Admin, BotToken, Logger, Home

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


def admin_handler(update: Update, context: CallbackContext):
    if update.effective_chat.id == Admin:
        update.message.reply_text(f"admin yoooooooo", reply_markup=keyboards.AdminMainKey)


def start_handler(update: Update, context: CallbackContext):

    try:
        if db.add_user(
                update.effective_chat.id,
                update.effective_chat.first_name,
                update.effective_chat.last_name,
                update.effective_chat.username
        ):
            log_text = f"chat_id: {update.effective_chat.id}\nname: {update.effective_chat.first_name}_{update.effective_chat.last_name}\nusername: @{update.effective_chat.username}"
            context.bot.send_message(chat_id=Logger, text=log_text)

        if channel.is_member(update.effective_chat.id):
            update.message.reply_text(f"wellcome to our bot", reply_markup=keyboards.MainKey)
        else:
            update.message.reply_text("join dudeeee", reply_markup=keyboards.join_channel_key())

    except Exception as error:
        context.bot.send_message(
            chat_id=Admin, text=f"Error occurred in bothandler.start_handler, line:{error.__traceback__.tb_lineno}\nerror:\n\n{error}")
        update.message.reply_text("مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text("how to use the bot : \n\n ....", reply_markup=keyboards.BackKey)


def link_handler(update: Update, context: CallbackContext):

    try:
        chat_id = update.effective_chat.id
        if chat_id == Logger:
            return

        link = update.message.text

        if not channel.is_member(chat_id):
            update.message.reply_text('لطفا برای استفاده از ربات در کانال ما جوین شوید. :)', reply_markup=keyboards.join_channel_key())
            return

        downer.thread_add(update, context)

    except Exception as error:
        update.message.reply_text('ی مشکلی پیش اومد ببشید, دوباره بفرست ')
        context.bot.send_message(chat_id=Admin, text=f'error in bothandler.link_handler by:{chat_id}\nlink:\n{link}\nerror in line {error.__traceback__.tb_lineno}:\n{error}')


def callback_handler(update: Update, context: CallbackContext):

    query = update.callback_query
    command = query.data

    try:
        if command == 'joined':
            if channel.is_member(query.from_user.id):
                query.edit_message_text('ربات فعال شد الان میتونی استفاده کنی', reply_markup=keyboards.MainKey)
            else:
                query.answer('جوین نشدی که :(')

        elif command == "help":
            query.edit_message_text("how to use the bot : \n\n ....", reply_markup=keyboards.BackKey)

        elif command == "account":
            query.edit_message_text("acount texttttttt", reply_markup=keyboards.AccountMenu)

        elif command == "back_to_main":
            query.edit_message_text(f"main menu", reply_markup=keyboards.MainKey)

        elif command == "back_to_account":
            query.edit_message_text(f"acount texttttttt", reply_markup=keyboards.AccountMenu)

        elif command == "get_prem":
            query.edit_message_text(f"main menu", reply_markup=keyboards.BuyMenu)

        elif command.startswith("dcb"):  # download callback handler
            downer.download_callback(query, context)

        elif command == "view_threadlist":
            from telbot.downer import thread_list
            thread_message = context.bot.send_message(chat_id=Admin, text=str(thread_list))
            # for i in range(100):   # TODO
            #     try:
            #         context.bot.edit_message_text(chat_id=Admin, message_id=thread_message.message_id, text=str(thread_list))
            #     except:
            #         pass
            # context.bot.delete_message(chat_id=Admin, message_id=thread_message.message_id)

        elif command == "getdb":
            context.bot.send_document(chat_id=Admin, document=open(Home+"database/db.sqlite", "rb"))

        elif command == "sendtoall":
            pass

    except Exception as error:
        context.bot.send_message(chat_id=Admin, text=f"Error occurred in main_bot.callback_handler, line:{error.__traceback__.tb_lineno}\nerror:\n\n{error}")
        query.message.reply_text("مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


updater = Updater(token=BotToken, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(CommandHandler('admin', admin_handler))
updater.dispatcher.add_handler(CommandHandler('help', help_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, link_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
