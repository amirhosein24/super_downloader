
from os import remove, _exit
from telethon import TelegramClient
from asyncio import get_event_loop

from credentials.creds import ApiHash, ApiId, Admin, BotToken, Home


print("MTPROTO going live...", end=" ")
try:
    client = TelegramClient(f"{Home}telbot/MTPROTO", api_id=ApiId, api_hash=ApiHash).start(bot_token=BotToken)
    print("done.")
except Exception as error:
    print(f"error: {error}, exiting app.")
    _exit(0)
mtprotoLoop = get_event_loop()


async def telethon_sender_mtproto(chat_id: int, file_path, caption: str = None):

    try:
        for fileavcd in file_path:
            with open(fileavcd, 'rb') as file:
                uploaded_file = await client.upload_file(file, part_size_kb=512)
                print(uploaded_file)

            await client.send_file(chat_id, uploaded_file, caption=caption, force_document=False)

    except Exception as error_:
        await client.send_message(Admin, f"error in uploader.telethon_sender_mtproto, line:{error_.__traceback__.tb_lineno}:\n{error_}")

    finally:
        for item in file_path:
            remove(item)


def sender(chat_id, file_path, caption):
    mtprotoLoop.run_until_complete(telethon_sender_mtproto(chat_id, file_path, caption))
