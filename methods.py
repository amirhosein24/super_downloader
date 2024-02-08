from creds import ForceJoinId, Admin


from re import sub
from os import mkdir
from requests import get 
from bs4 import BeautifulSoup
from uuid import uuid4

try:
    mkdir("cache")
except:
    pass





def channel_checker(context, user_id):
    try:
        for channel in ForceJoinId.values():
            if context.bot.get_chat_member(chat_id=channel, user_id=user_id).status == 'member':
                continue
            else:
                return False
        return True
    except Exception as e:
        context.bot.send_message(chat_id=Admin, text=f"Error in channel checker by {user_id}:\nError : \n{e}")
        return True




def download_video(url, name) -> None:

    response = get(url)
    with open(f"cache/{name}.mp4", "wb") as file:
        file.write(response.content)


def create_url(url):

    api_url = f"https://twitsave.com/info?url={url}"

    try:
        response = get(api_url)
        data = BeautifulSoup(response.text, "html.parser")
        download_button = data.find_all("div", class_="origin-top-right")[0]
        quality_buttons = download_button.find_all("a")
        highest_quality_url = quality_buttons[0].get("href") # Highest quality video url
        
        # file_name = data.find_all("div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text # Video file name
        # file_name = sub(r"[^a-zA-Z0-9]+", ' ', file_name).strip() # Remove special characters from file name

        # if not file_name:
        #     file_name = str(uuid4()) + ".mp4"

        return highest_quality_url
    except:
        return False

def get_caption():
    pass