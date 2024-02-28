from creds import ForceJoinId, Admin

from os import mkdir, path
from requests import get
from bs4 import BeautifulSoup



try:
    mkdir(path.dirname(path.realpath(__file__)) + "/cache")
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
















# import re
# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://ssstwitter.com/")
#     page.get_by_role("button", name="Close").click()
#     page.get_by_placeholder("Insert link").fill("https://x.com/1youngfairo/status/1760390577684648266?s=20")
#     page.get_by_role("button", name="Download").click()

#     print("loading it")

#     page.wait_for_load_state("networkidle")

#     print("gogo")
#     selector = 'button[id^="download"]'
#     button = page.query_selector(selector)
#     print(button)


#     # Using regex to extract the download URL
#     # download_url_match = re.search(r"url='(.*?)'", str(download))

#     # if download_url_match:
#     #     download_url = download_url_match.group(1)
#     #     print(download_url)
#     # else:
#     #     print("Download URL not found.")

#     # input("------------------")


#     # print(download.url)
#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)









########################################################################################################################################## youtube

from pytube import YouTube
from datetime import timedelta


def youtube_getinfo(url):
    try:
        yt = YouTube(url)

        data = {}
        data["title"], data["length"] = yt.title, str(timedelta(seconds=yt.length)) #in seconds

        video = yt.streams.filter(progressive=False, file_extension='mp4')

        for stream in video:
            resolution = str(stream.resolution)
            file_size = str(round(stream.filesize / (1024 * 1024), 2))
            data[resolution] = [file_size, stream.itag] 
        return data

    except Exception as e:
        print(f"Error: {e}")
        return None



def youtube_getvideo(url, itag=None):
    try:
        yt = YouTube(url)

        video = yt.streams.get_by_itag(itag)
        video.download()

        print("Video downloaded successfully")

    except Exception as e:
        print(f"Error downloading video: {e}")


########################################################################################################################################## insta






########################################################################################################################################## tiktok




########################################################################################################################################## link 2 file