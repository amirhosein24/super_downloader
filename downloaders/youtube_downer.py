from pytube import YouTube
from datetime import timedelta


def youtube_getinfo(url):
    try:
        yt = YouTube(url)

        data = {}
        data["title"], data["length"] = yt.title, str(
            timedelta(seconds=yt.length))  # in seconds
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
