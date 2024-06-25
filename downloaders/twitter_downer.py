import requests
import re
from typing import List, Dict, Any, Optional

# Suppress the InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def extract_tweet_ids(text: str) -> Optional[List[str]]:
    """Extract tweet IDs from message."""
    unshortened_links = ''
    for link in re.findall(r"t\.co/[a-zA-Z0-9]+", text):
        try:
            unshortened_link = requests.get('https://' + link).url
            unshortened_links += '\n' + unshortened_link
        except requests.exceptions.RequestException as e:
            print(f"Failed to unshorten link {link}: {e}")

    tweet_ids = re.findall(
        r"(?:twitter|x)\.com/.{1,15}/(?:web|status(?:es)?)/([0-9]{1,20})", text + unshortened_links)
    tweet_ids = list(dict.fromkeys(tweet_ids))
    return tweet_ids or None

def scrape_media(tweet_id: int) -> List[Dict[str, Any]]:
    try:
        response = requests.get(
            f'https://api.vxtwitter.com/Twitter/status/{tweet_id}', verify=False)
        response.raise_for_status()
        tweet_data = response.json()
        print("Scraped Tweet Data:", tweet_data)

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

def download_media(tweet_media: List[dict], chat_id) -> List[str]:
    """Download media from the provided list of Twitter media dictionaries."""
    files = []
    for media in tweet_media:
        media_url = media['media']['url']
        try:
            response = requests.get(media_url, stream=True, verify=False)
            response.raise_for_status()

            if media['media']['type'] == 'photo':
                file_extension = 'jpg'
            elif media['media']['type'] == 'animated_gif':
                file_extension = 'gif'
            elif media['media']['type'] == 'video':
                file_extension = 'mp4'
            else:
                continue

            filename = f"{chat_id}_{media['media']['type']}.{file_extension}"
            filepath = f"downloaders/cache/{filename}"

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            files.append(filepath)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download media from {media_url}: {e}")
    return files

def download_twitter_media(context, chat_id, link):
    tweet_ids = extract_tweet_ids(link)
    if tweet_ids:
        all_files = []
        captions = []
        for tweet_id in tweet_ids:
            media = scrape_media(int(tweet_id))
            if media:
                files = download_media(media, chat_id)
                all_files.extend(files)
                if media:
                    captions.append(media[0]['caption'])  # Assuming all media in a tweet have the same caption
            else:
                context.bot.send_message(
                    chat_id=chat_id, text=f"No media found for this tweet: {link}")
        if all_files:
            return all_files, captions
        else:
            return [], []
    else:
        context.bot.send_message(
            chat_id=chat_id, text=f"Error, No supported tweet link found: {link}")
        return [], []
