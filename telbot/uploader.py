
from os import remove, _exit
from os.path import isfile
from asyncio import get_event_loop

from telethon import TelegramClient

from telbot.keyboards import SponsorKeyboard_mtproto
from credentials.creds import ApiHash, ApiId, Admin, BotToken, Home


print("MTPROTO going live...", end=" ")
try:
    client = TelegramClient(f"{Home}telbot/MTPROTO", api_id=ApiId, api_hash=ApiHash).start(bot_token=BotToken)
    print("done.")
except Exception as error:
    print(f"error: {error}, exiting app.")
    _exit(0)
mtprotoLoop = get_event_loop()


async def telethon_sender_mtproto(chat_id: int, file_path: list, caption: str = ""):

    try:
        media_group = []
        for media in file_path:
            with open(media, 'rb') as f:
                media_group.append(
                    await client.upload_file(f, part_size_kb=512)
                )

        if len(media_group) == 1:  # TODO send the sponsers if its media group
            media_group = media_group[0]

        caption = caption + "\n\n➖➖➖➖➖➖\n🆔 @sup_downloader_bot    ربات دانلودر"
        await client.send_file(chat_id, media_group, caption=caption, force_document=False, allow_cache=False, buttons=SponsorKeyboard_mtproto)

    except Exception as error_:
        await client.send_message(Admin, f"error in uploader.telethon_sender_mtproto, line:{error_.__traceback__.tb_lineno}:\n{error_}")

    finally:
        for media in file_path:
            if isfile(media):
                remove(media)


def sender(chat_id, file_path, caption):
    mtprotoLoop.run_until_complete(telethon_sender_mtproto(chat_id, file_path, caption))
