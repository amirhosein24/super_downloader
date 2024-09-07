
from telegram import ChatMember
from creds import Channel, Bot, Admin


def is_member(chat_id):

    for channel_name in Channel:
        try:
            if Bot.get_chat_member(chat_id=Channel[channel_name]["id"], user_id=chat_id).status not in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.CREATOR]:
                return False

        except Exception as error:
            Bot.send_message(
                chat_id=Admin, text=f"Error occurred in channel.is_member, error:\n\n{error}")
            return True

    return True
