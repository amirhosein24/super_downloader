from telethon import TelegramClient
from credentials.creds import ApiHash, ApiId, Admin, BotToken, Home
from os import remove

# telethon client to send files to user
client = TelegramClient(f"{Home}telbot/uploader", api_id=ApiId, api_hash=ApiHash).start(bot_token=BotToken)


async def send_to(chat_id, file_path, caption):
    try:
        print('------------------------------------')
        with open(file_path, 'rb') as file:
            uploaded_file = await client.upload_file(file, part_size_kb=512)
            print(uploaded_file)

        await client.send_file(chat_id, uploaded_file, caption=caption, force_document=False)

    except Exception as error:
        await client.send_message(Admin, f"error in uploader.send_to, error:\n{error}")

    # finally:
    #     if isinstance(file_path, str):
    #         remove(file_path)
    #     elif isinstance(file_path, list):
    #         for item in file_path:
    #             remove(item)


# TODO how to run send_to func ????

import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Welcome to your new bot.')


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("fdsfsdf")
    asyncio.run(send_to(5097685770, r"D:\elevoc_dnn_kernel.log", "+++++++"))

updater = Updater(BotToken)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()
