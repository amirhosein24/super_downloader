from creds import ForceJoinId, Admin, Instagram

from os import mkdir, path
from requests import get, head

home = path.dirname(path.realpath(__file__)) + "/"

for addres in [home + "cache", home + "cache/twitter", home + "cache/youtube", home + "cache/insta", home + "cache/other"]:
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
from bs4 import BeautifulSoup
    
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
from pytube import YouTube
from datetime import timedelta



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

# print(youtube_getinfo("https://youtube.com/shorts/JSRwORjv-BE?si=dAEDUV109k21Vd66"))

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# import os

# # Scopes required by the YouTube API
# SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# def authenticate_youtube():
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'client_secrets.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     return build('youtube', 'v3', credentials=creds)

# def youtube_getinfo(youtube, video_id):
#     # Replace 'YOUR_VIDEO_ID' with the ID of the video you are trying to access
#     request = youtube.videos().list(
#         part='snippet,contentDetails,statistics',
#         id=video_id
#     )
#     response = request.execute()
    
#     data = {}
#     if response['items']:
#         video = response['items'][0]
#         data['title'] = video['snippet']['title']
#         data['length'] = video['contentDetails']['duration']
#         # ... Extract other data as needed

#     return data

# # Authenticate to YouTube API
# youtube = authenticate_youtube()

# # Call the function with a video ID
# video_data = youtube_getinfo(youtube, "YOUR_VIDEO_ID")
# print(video_data)

def youtube_getvideo(url, res):
    try:
        yt = YouTube(url)

        stream = yt.streams.filter(res=res, progressive=True).first()
        yield int(stream.filesize / (1024 * 1024))

        file = stream.download(output_path=home + "cache/youtube/")
        yield file, yt.title

    except Exception as e:
        print(f"Error downloading video: {e}")
        yield False, False


########################################################################################################################################## insta
import requests
import instagrapi

client = instagrapi.Client()
client.login(Instagram[0], Instagram[1])

def download_insta(chat_id, url):
    media_info = client.media_info(client.media_pk_from_url(url))
    caption = media_info.caption_text
    file_list  = []

    if media_info.resources:
        for index, item in enumerate(media_info.resources):
            
            if item.video_url :
                download_url = item.video_url
                filename = f"{chat_id}-{index}.mp4"
            else:
                download_url = item.thumbnail_url
                filename = f"{chat_id}-{index}.jpg"

            file_list.append(home + "cache/insta/" + filename)
            response = requests.get(download_url)
            with open(home + "cache/insta/" + filename, 'wb') as file:
                file.write(response.content)
    else:
        
        if media_info.video_url :
            download_url = media_info.video_url
            filename = f"{chat_id}.mp4"
        else:
            download_url = media_info.thumbnail_url
            filename = f"{chat_id}.jpg"

        file_list.append(home + "cache/insta/" + filename)
        response = requests.get(download_url)
        with open(home + "cache/insta/" + filename, 'wb') as file:
            file.write(response.content)

    return file_list, caption



########################################################################################################################################## tiktok

########################################################################################################################################## link 2 file4

from urllib.parse import urlparse


def downloader(url):
  response = get(url, allow_redirects=True)

  if response.status_code == 200:
    content_disposition = response.headers.get("content-disposition")
    if content_disposition:
      filename = content_disposition.split("filename=")[1].strip('"')
    else:
      parsed_url = urlparse(url)
      filename = parsed_url.path.split("/")[-1]

    with open(f"{home}cache/other/{filename}", "wb") as file:
      file.write(response.content)

    return filename
  else:
    print(f"Failed to download file: {response.status_code}")
    return None




def get_file_size(url):
  response = head(url, allow_redirects=True)

  if response.status_code == 200:

    content_length = response.headers.get("content-length")
    if content_length:
      return int(content_length) / (1024 * 1024)
    else:
      return None
  else:
    return None