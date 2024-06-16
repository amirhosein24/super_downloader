
from telethon import TelegramClient
from credentials.creds import ApiHash, ApiId, Admin, BotToken, Home
from os import remove

# telethon client to send files to user
client = TelegramClient(f"{Home}telbot/uploader", api_id=ApiId,
                        api_hash=ApiHash).start(bot_token=BotToken)


async def send_to(chat_id, file_path, caption, duration):

    try:

        # upload in 20 mg chunks 
        with open(file_path, 'rb') as file:
            uploaded_file = await client.upload_file(file, part_size_kb=20_480, timeout=15, max_retries=4)

        await client.send_file(chat_id, uploaded_file, caption=caption, attributes=[('duration', duration)], force_document=False)

    except Exception as error:
        await client.send_message(Admin, f"error in uploader.send_to, error:\n{error}")

    finally:

        # clear cache after sending
        if isinstance(file_path, str):
            remove(file_path)
        elif isinstance(file_path, list):
            for item in file_path:
                remove(item)
