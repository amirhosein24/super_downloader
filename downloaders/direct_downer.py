
from urllib.parse import urlparse
from requests import get, head

from credentials.creds import Home


def download(url):
    response = get(url, allow_redirects=True)

    if response.status_code == 200:
        content_disposition = response.headers.get("content-disposition")

        if content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        else:
            parsed_url = urlparse(url)
            filename = parsed_url.path.split("/")[-1]

        with open(f"{Home}downloaders/cache/{filename}", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

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
