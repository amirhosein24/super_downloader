
from credentials.creds import Channel, Bot, Admin

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

from traceback import format_exc


async def is_member(client, user_id):

    for channel in Channel:
        try:
            await client(GetParticipantRequest(channel=Channel[channel]["id"], participant=user_id))
            continue

        except UserNotParticipantError:
            return False

        except:
            Bot.send_message(chat_id=Admin, text=format_exc())
            return True

    return True
