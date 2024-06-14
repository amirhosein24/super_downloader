
from credentials.creds import Channel, Bot, Admin

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError


async def is_member(client, user_id):

    for channel in Channel:
        try:
            await client(GetParticipantRequest(channel=Channel[channel]["id"], participant=user_id))
            continue

        except UserNotParticipantError:
            return False

        except Exception as error:
            from traceback import extract_tb
            tb = extract_tb(error.__traceback__)
            Bot.send_message(chat_id=Admin, text=f"Error occurred in channel.is_member, line:{tb[-1].lineno}\nerror:\n\n{error}")
            return True

    return True
