import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from decouple import config
import os
import time

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')

scopes = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sa = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                  scope=scopes)
sp = spotipy.Spotify(auth_manager=sa)
states = ['context', 'track', 'off']
'''
-Reanudar el playback
-añadir a la cola
-pausar el playback
-Pasar siguiente cancion
-regresar cancion
-reproducir una cancion
-cambiar de dispositivo
-activar/desactivar shuffle
-activar/desactivar repeat
'''


def reproducir_cancion(cancion, device='COMPUTADORA'):
    try:
        track = sp.search(q=f'track:{cancion}', type='track')
        time.sleep(.2)
        track = track['tracks']['items'][0]['uri']
        cp = sp.currently_playing()
        cp = cp['item']['uri']
        if track == cp:
            return
        sp.add_to_queue(track)
        cola = []
        volume = sp.current_playback()['device']['volume_percent']
        sp.volume(0)
        while cp != track:
            sp.next_track()
            time.sleep(.1)
            cp = sp.currently_playing()
            cp = cp['item']['uri']
            cola.append(cp)
        cola.pop(len(cola)-1)
        sp.volume(volume)
        for track in cola:
            sp.add_to_queue(track)
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

def shuffle(device=None):
    x = sp.current_playback()
    x = x['shuffle_state']
    if device:
        sp.shuffle(state=not x, device_id=config(device))
    else:
        sp.shuffle(state=not x,)



def repetir(device=None):
    x = sp.current_playback()
    if x:
        x = x['repeat_state']
        index = states.index(x)
        index = index + 1 if index != 2 else 0
        if device:
            sp.repeat(state=states[index], device_id=config(device))
        else:
            sp.repeat(state=states[index],)


def cambiar_dispositivo(device):
    sp.transfer_playback(device_id=config(device), force_play=True)


def queue(cancion, device='COMPUTADORA'):
    track = sp.search(q=f'track:{cancion}', type='track')
    time.sleep(.2)
    track = track['tracks']['items'][0]['uri']
    sp.add_to_queue(track, device_id=config(device))


def regresar_cancion():
    sp.previous_track()

def cambiar_volumen(valor):
    volume = sp.current_playback()['device']['volume_percent']
    volume += valor
    sp.volume(volume)


