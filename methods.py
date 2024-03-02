from creds import ForceJoinId, Admin

from os import mkdir, path
from requests import get, head





home = path.dirname(path.realpath(__file__)) + "/"


for addres in [home + "cache", home + "cache/twitter", home + "cache/youtube", home + "cache/other"]:
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
import instaloader

def download_instagram_post(url):
    """Downloads the Instagram post from the provided URL and saves it to the specified target directory.

    Args:
        url (str): The URL of the Instagram post to download.

    Raises:
        instaloader.ProfileNotExistsException: If the profile specified in the target directory does not exist.
        instaloader.Post.NotAPostException: If the provided URL doesn't point to a valid Instagram post.
    """

    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    # Extract the username from the URL
    username = url.split("/")[-2]

    # Load the post metadata
    post = instaloader.Post.from_shortcode(loader.context, url)

    # Download the post and save it to the specified target directory
    loader.download_post(post, target=username)  # Use the extracted username as the target directory

# Example usage
url = "https://www.instagram.com/reel/C3-wFp7rI45/?utm_source=ig_web_copy_link"
download_instagram_post(url)




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
