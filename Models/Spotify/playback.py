import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from decouple import config

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')

scopes = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sa = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                  scope=scopes)
sp = spotipy.Spotify(auth_manager=sa)
'''
Reanudar el playback
añadir a la cola
pausar el playback
Pasar siguiente cancion
regresar cancion
reproducir una cancion
cambiar de dispositivo
activar/desactivar shuffle
activar/desactivar repeat
'''


def reproducir_cancion(cancion, device='COMPUTADORA'):
    try:
        track = sp.search(q=f'track:{cancion}', type='track')
        track = track['tracks']['items'][0]['uri']
        sp.add_to_queue(track)
        cp = ''
        while cp != track:
            sp.next_track()
            cp = sp.currently_playing()
            cp = cp['item']['uri']
            print('-------')
            print(cp)
            print(track)
            print('-------')
        return True
    except SpotifyException:
        try:
            track = sp.search(q=f'track:{cancion}', type='track')
            track = track['tracks']['items'][0]['uri']
            sp.add_to_queue(track, device_id=config(device))
            sp.next_track()
            return True
        except SpotifyException:
            return False


def reanudar_playback(device='COMPUTADORA'):
    try:
        sp.start_playback()
        return True
    except SpotifyException:
        try:
            sp.start_playback(config(device))
            return True
        except SpotifyException:
            return False


def siguiente_cancion():
    sp.next_track()


def pausar_playback():
    try:
        sp.pause_playback()
        return True
    except SpotifyException:
        return False


def dispositivos():
    dis = sp.devices()
    dis = dis['devices']
    for i in dis:
        print(i)


def get_token():
    print(sa.get_access_token())
