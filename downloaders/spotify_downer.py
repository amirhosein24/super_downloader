

import subprocess

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from credentials.creds import Home


client_id = '---'
client_secret = '---'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def spot_download(link, bitrate="320k"):

    command = f"spotdl --bitrate {bitrate} {link}"

    command = f"spotdl --bitrate {bitrate} --output-dir {output_dir} --output {output_format} {link}"

    subprocess.run(command, check=True, shell=True)


def get_track_details(track_id):

    track = sp.track(track_id)

    name = track['name']
    artists = ', '.join([artist['name'] for artist in track['artists']])
    album = track['album']['name']
    duration = int(int(track['duration_ms'])/1000)

    minutes = duration // 60
    seconds = duration % 60

    track_details = f"""
    Track Name: {name}
    Artists: {artists}
    Album: {album}
    Duration: {minutes}:{seconds}
    """

    return track_details
