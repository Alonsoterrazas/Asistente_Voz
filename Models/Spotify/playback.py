import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from decouple import config

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')
CELULAR = config('CELULAR_ID')

scopes = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                              scope=scopes))
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