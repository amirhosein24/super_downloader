from creds import ForceJoinId, Admin

from os import mkdir, path
from requests import get
from bs4 import BeautifulSoup


from pytube import YouTube
from datetime import timedelta



home = path.dirname(path.realpath(__file__))


for addres in [home + "/cache", home + "/cache/twitter", home + "/cache/youtube"]:
    try:
        mkdir(addres)
    except:
        pass

########################################################################################################################################## telegram

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



########################################################################################################################################## twiiter
def download_video(url, name) -> None:
    response = get(url)

    with open(name, "wb") as file:

        file.write(response.content)


def create_url(context, url):

    api_url = f"https://twitsave.com/info?url={url}"
    try:
        response = get(api_url)
        data = BeautifulSoup(response.text, "html.parser")
        download_button = data.find_all("div", class_="origin-top-right")

        highest_quality_url = []
        for item in download_button:
            quality_buttons = item.find_all("a")
            highest_quality_url.append(quality_buttons[0].get("href")) # Highest quality video url

        try:
            caption = data.find_all("div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text # Video caption
        except:
            caption = None

        return highest_quality_url, caption

    except Exception as error:
        context.bot.send_message(chat_id=Admin, text=f"Error in create url : {url}\n\nerror : \n{error}")
        return False, False 



########################################################################################################################################## youtube

def youtube_getinfo(url):
    try:
        yt = YouTube(url)

        data = {}
        data["title"], data["length"] = yt.title, str(timedelta(seconds=yt.length)) #in seconds
        video = yt.streams.filter(progressive=True)

        for stream in video:
            resolution = str(stream.resolution)
            file_size = str(round(stream.filesize / (1024 * 1024), 2))
            if resolution not in data or file_size < data[resolution]:
                data[resolution] = file_size 
        return data, True

    except Exception as error:

        return str(error), False





def youtube_getvideo(url, res):
    try:
        yt = YouTube(url)

        stream = yt.streams.filter(res=res, progressive=True).first()

        file = stream.download(output_path=home + "/cache/youtube/")

        return file, yt.title, yt.length


    except Exception as e:
        print(f"Error downloading video: {e}")
        return False, False, False


########################################################################################################################################## insta

########################################################################################################################################## tiktok

########################################################################################################################################## link 2 file