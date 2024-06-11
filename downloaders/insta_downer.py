import requests
import instaloader
from credentials.creds import Home, Bot, Admin


insta_loader = instaloader.Instaloader()


def download_slide(video_url, filename):

    response = requests.get(video_url, stream=True)

    response.raise_for_status()

    file_format = response.headers.get('Content-Type').split("/")[1]

    with open(Home + f"downloaders/cache/{filename}.{file_format}", 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def instagram(chat_id, link):

    try:

        shortcode = link.split('/')[-2]
        post = instaloader.Post.from_shortcode(insta_loader.context, shortcode)

        # Carousel post (multiple images/videos)
        if post.typename == 'GraphSidecar':

            for _, node in enumerate(post.get_sidecar_nodes()):

                if node.is_video:
                    video_url = node.video_url
                    download_slide(video_url, f"{chat_id}_{shortcode}_{_}")

                else:
                    photo_url = node.display_url
                    download_slide(photo_url, f"{chat_id}_{shortcode}_{_}")

        else:
            if post.is_video:  # Single video post
                video_url = post.video_url
                download_slide(video_url, f"{chat_id}_{shortcode}")

            else:    # Single image post
                media_url = post.url
                download_slide(media_url, f"{chat_id}_{shortcode}")

        return True

    except Exception as error:
        Bot.send_message(
            Admin, f"error in instagram, error:\n{error}\n\nnlink:\n{link}")
        return None
