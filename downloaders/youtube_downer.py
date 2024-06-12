
from credentials.creds import Home

from pytube import YouTube
from datetime import timedelta


def download(url, itag):

    yt = YouTube(url)

    for stream in yt.streams:

        if stream.itag == itag:
            file = stream.download(output_path=Home + "downloaders/cache/")
            return file

    return False


def getinfo(link):

    yt = YouTube(link)
    data = {}

    for stream in yt.streams:

        if stream.mime_type.startswith("video") and not stream.is_progressive:
            if not stream.resolution in data:
                data[stream.resolution] = {"itag": stream.itag,
                                           "size": round(stream.filesize / (1024 * 1024), 1)}

            elif stream.mime_type.split("/")[1] == "mp4":
                data[stream.resolution] = {"itag": stream.itag,
                                           "size": round(stream.filesize / (1024 * 1024), 1)}

        elif stream.mime_type == "audio/mp4":
            data[stream.abr] = {"itag": stream.itag,
                                "size": round(stream.filesize / (1024 * 1024), 1)}

        data["title"], data["length"] = yt.title, str(
            timedelta(seconds=yt.length))  # in seconds

    return data
