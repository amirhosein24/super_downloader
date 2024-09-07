

from pytube import YouTube
from datetime import timedelta

from subprocess import run
from os import remove, path

from creds import Home


def download(chat_id, url, itag):
    yt = YouTube(url)

    try:
        for stream in yt.streams:

            if str(stream.itag) == "139":
                audio_file = stream.download(
                    output_path=Home + f"downloaders/cache/", filename=f"{chat_id}_audio.mp4")

            elif str(stream.itag) == itag:
                video_file = stream.download(
                    output_path=Home + f"downloaders/cache/", filename=f"{chat_id}_video.mp4")

        command = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            Home + "downloaders/cache/" + yt.title + ".mp4"
        ]

        run(command)
        return Home + "downloaders/cache/" + yt.title + ".mp4"

    except Exception as e:
        print(f"error in yt downer download : {e}")
        return False

    finally:
        if path.exists(video_file):
            remove(video_file)
        if path.exists(audio_file):
            remove(audio_file)


def getinfo(link):

    yt = YouTube(link)
    data = {}

    for stream in yt.streams:
        print(stream)
        if stream.mime_type.startswith("video") and not stream.is_progressive:
            if stream.resolution not in data:
                data[stream.resolution] = {
                    "itag": stream.itag, "size": round(stream.filesize / (1024 * 1024), 1)
                }

            elif stream.mime_type.split("/")[1] == "mp4":
                data[stream.resolution] = {
                    "itag": stream.itag, "size": round(stream.filesize / (1024 * 1024), 1)
                }

        elif stream.mime_type == "audio/mp4":
            data[stream.abr] = {
                "itag": stream.itag, "size": round(stream.filesize / (1024 * 1024), 1)
            }

        data["title"], data["length"] = yt.title, str(
            timedelta(seconds=yt.length))  # in seconds

    return data
