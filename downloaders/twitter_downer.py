

import requests
from typing import List, Dict, Any

# Suppress the InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def scrape_media(tweet_id: int) -> List[Dict[str, Any]]:
    try:
        response = requests.get(
            f'https://api.vxtwitter.com/Twitter/status/{tweet_id}', verify=False)
        response.raise_for_status()
        tweet_data = response.json()
        # print("Scraped Tweet Data:", tweet_data)

        media_extended = tweet_data.get('media_extended', [])
        tweet_text = tweet_data.get('text', '')  # Ensure the correct key is used for the caption

        # Combine the media data with the tweet text (caption)
        media_with_captions = []
        for media in media_extended:
            media_with_captions.append({
                'media': media,
                'caption': tweet_text
            })

        return media_with_captions
    except requests.exceptions.RequestException as e:
        print(e)
        return []
    except Exception as e:
        print(e)
        return []


def download_media(tweet_data: List[dict], chat_id) -> List[str]:
    """Download media from the provided list of Twitter media dictionaries."""
    files = []
    for index, media in enumerate(tweet_data):
        media_url = media['media']['url']
        try:
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

            filepath = f"downloaders/cache/{chat_id}_{index}_{media['media']['type']}.{file_extension}"

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            files.append(filepath)

        except requests.exceptions.RequestException as e:
            print(f"Failed to download media from {media_url}: {e}")

    return files


def main_download(context, chat_id, link):

    tweet_id = link.split("status/")[-1].split("/")[0]

    if tweet_id:
        media = scrape_media(int(tweet_id))

        files = download_media(media, chat_id)

        if files:
            return files, media[0]['caption']
        else:
            return [], None

    else:
        return [], None
