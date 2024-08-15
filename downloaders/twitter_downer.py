
from requests import get
from bs4 import BeautifulSoup

from credentials.creds import Admin, Home


def download_video(url, name) -> None:
    response = get(url)

    with open(f"{Home}downloaders/cache/{name}", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    return f"{Home}downloaders/cache/{name}"


def create_url(context, chat_id, url):

    api_url = f"https://twitsave.com/info?url={url}"
    try:
        response = get(api_url)
        data = BeautifulSoup(response.text, "html.parser")
        download_button = data.find_all("div", class_="origin-top-right")

        highest_quality_url = []
        for item in download_button:
            quality_buttons = item.find_all("a")
            highest_quality_url.append(quality_buttons[0].get("href"))  # Highest quality video url

        try:
            caption = data.find_all(
                "div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text  # Video caption
        except:
            caption = None

        files = []

        for url in highest_quality_url:
            files.append(download_video(url, chat_id))

        return (files, caption)

    except Exception as error:
        context.bot.send_message(
            chat_id=Admin, text=f"Error in create url : {url}\n\nerror : \n{error}")
        return False, False
