
from credentials.creds import Channel, Bot, Admin
from telegram import ChatMember


def is_member(chat_id):

    for channel in Channel:
        try:
            chat_member = Bot.get_chat_member(chat_id=Channel[channel]["id"], user_id=chat_id)
            if chat_member.status not in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.CREATOR]:
                return False

        except Exception as error:
            Bot.send_message(chat_id=Admin, text=f"Error occurred in channel.is_member, error:\n\n{error}")
            return True

    return True
