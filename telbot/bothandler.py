
import database.database as db
from telbot import keyboards, channel, downer
from credentials.creds import Admin, BotToken

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


def start_handler(update: Update, context: CallbackContext):

    try:
        if db.add_user(
                update.effective_chat.id,
                update.effective_chat.first_name,
                update.effective_chat.last_name,
                update.effective_chat.username
        ):
            log_text = f"chat_id: {update.effective_chat.id}\nname: {update.effective_chat.first_name}_{update.effective_chat.last_name}\nusername: @{update.effective_chat.username}"
            context.bot.send_message(chat_id=Admin, text=log_text)

        if channel.is_member(update.effective_chat.id):
            update.message.reply_text(
                f"wellcome to our bot", reply_markup=keyboards.MainKey)
        else:
            update.message.reply_text(
                "join dudeeee", reply_markup=keyboards.join_channel_key())

    except Exception as error:
        from traceback import format_exc
        tb = format_exc()
        context.bot.send_message(
            chat_id=Admin, text=f"Error occurred in bothandler.start_handler, line:{tb.splitlines()[-1]}\nerror:\n\n{error}")
        update.message.reply_text(
            "مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        "how to use the bot : \n\n ....", reply_markup=keyboards.BackKey)


def link_handler(update: Update, context: CallbackContext):

    try:
        chat_id = update.effective_chat.id
        link = update.message.text

        if not channel.is_member(chat_id):
            update.message.reply_text(
                'لطفا برای استفاده از ربات در کانال ما جوین شوید. :)')
            return

        downer.thread_handler(update, context)

    except Exception as error:
        update.message.reply_text(
            'ی مشکلی پیش اومد ببشید, دوباره بفرست شاید تونستم')
        context.bot.send_message(
            chat_id=Admin, text=f'error in bothandler.link_handler by:{chat_id}\nlink:-----\n{link}\nerror:-----\n{error}')


def callback_handler(update: Update, context: CallbackContext):

    query = update.callback_query
    chat_id = query.from_user.id
    command = query.data

    try:
        if command == 'joined':
            if channel.is_member(chat_id):
                query.edit_message_text('ربات فعال شد الان میتونی استفاده کنی', reply_markup=keyboards.MainKey)
            else:
                query.answer('جوین نشدی که :(')

        elif command == "help":
            print("ssssssss")
            query.edit_message_text(
                "how to use the bot : \n\n ....", reply_markup=keyboards.BackKey)

        elif command == "account":
            query.edit_message_text(
                "acount texttttttt", reply_markup=keyboards.AccountMenu)

        elif command == "back_to_main":
            query.edit_message_text(
                f"main menu", reply_markup=keyboards.MainKey)

        elif command == "back_to_account":
            query.edit_message_text(
                f"acount texttttttt", reply_markup=keyboards.AccountMenu)

        elif command == "get_prem":
            query.edit_message_text(
                f"main menu", reply_markup=keyboards.BuyMenu)


        elif command.startswith("dcb"):
            downer.download_callback(update, context)

    except Exception as error:
        from traceback import format_exc
        tb = format_exc()
        context.bot.send_message(
            chat_id=Admin, text=f"Error occurred in main_bot.callback_handler, line:{tb.splitlines()[-1]}\nerror:\n\n{error}")
        query.message.reply_text(
            "مشکلی در سیستم پیش امد, لطفا چند لحظه دیگر دوباره تلاش کنید")


def go_live():
    updater = Updater(token=BotToken, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, link_handler))
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    print("goin live ...")
    updater.start_polling()
    print("bot is live.")

    updater.idle()
