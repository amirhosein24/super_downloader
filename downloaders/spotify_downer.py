

from os.path import join
from subprocess import run

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from creds import Home, Apps, Bot, Admin

client_credentials_manager = SpotifyClientCredentials(
    client_id=Apps["spotify"]["client_id"],
    client_secret=Apps["spotify"]["client_secret"])

sp = Spotify(client_credentials_manager=client_credentials_manager)


def spot_download(trackid, bitrate="128k"):
    try:
        output_dir = join(Home, "downloaders", "cache")
        command = f"spotdl --bitrate {bitrate} --output {output_dir} https://open.spotify.com/track/{trackid}"
        result = run(command, check=True, shell=True, capture_output=True, text=True)

        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if line.startswith("Downloaded"):
                file_path = output_dir + "\\" + line.split("\"")[1] + ".mp3"
                return file_path
    except Exception as error:
        Bot.send_message(
            Admin, f"error in spotify_downer.spot_download, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")
        return None


def get_track_details(link):
    try:
        track_id = link.split('/')[-1].split('?')[0]
        track = sp.track(track_id)

        name = track['name']
        duration = int(int(track['duration_ms'])/1000)
        # album = track['album']['name']
        # artists = ', '.join([artist['name'] for artist in track['artists']])

        return f"{name}   {duration//60:02}:{duration%60:02}", track_id
    except Exception as error:
        Bot.send_message(
            Admin, f"error in spotify_downer.get_track_details, error in line {error.__traceback__.tb_lineno}\n\nerror:\n{error}")
        return None
