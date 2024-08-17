
import requests

from credentials.creds import Bot, Admin, Home

# Suppress the InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def scrape_media(tweet_id: int) -> list[dict[str, any]]:
    try:
        response = requests.get(
            f'https://api.vxtwitter.com/Twitter/status/{tweet_id}', verify=False)
        response.raise_for_status()
        tweet_data = response.json()

        media_extended = tweet_data.get('media_extended', [])
        # Ensure the correct key is used for the caption
        tweet_text = tweet_data.get('text', '')

        # Combine the media data with the tweet text (caption)
        media_with_captions = []
        for media in media_extended:
            media_with_captions.append({
                'media': media,
                'caption': tweet_text
            })

        return media_with_captions

    # except requests.exceptions.RequestException as e:
    #     print(e)
    #     return []

    except Exception as error:
        Bot.send_message(
            Admin, f"error in twitter_downer.scrape_media, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")
        return []


def download_media(tweet_data: list[dict], chat_id) -> list[str]:
    """Download media from the provided list of Twitter media dictionaries."""
    files = []
    for index, media in enumerate(tweet_data):

        try:
            media_url = media['media']['url']
            response = requests.get(media_url, stream=True, verify=False)
            response.raise_for_status()

            if media['media']['type'] == 'image':
                file_extension = 'jpg'
            elif media['media']['type'] == 'animated_gif':
                file_extension = 'gif'
            elif media['media']['type'] == 'video':
                file_extension = 'mp4'
            else:
                continue

            filepath = f"{Home}downloaders/cache/{chat_id}_{index}_{media['media']['type']}.{file_extension}"

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            files.append(filepath)

        # except requests.exceptions.RequestException as e:
        #     print(f"Failed to download media from {media_url}: {e}")

        except Exception as error:
            Bot.send_message(
                Admin, f"error in twitter_downer.download_media, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")

    return files


def main_download(context, chat_id, link) -> tuple[list, str]:
    try:
        tweet_id = link.split("status/")[-1].split("/")[0]
        tweet_id = tweet_id.split("?")[0] if "?" in tweet_id else tweet_id

        if tweet_id:
            media = scrape_media(int(tweet_id))
            files = download_media(media, chat_id)
            if files:
                return files, media[0]['caption']
            else:
                return [], None

        else:
            return [], None

    except Exception as error:
        Bot.send_message(
            Admin, f"error in twitter_downer.main_download, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")
        return [], None
