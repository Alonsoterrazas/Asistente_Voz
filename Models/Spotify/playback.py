import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from decouple import config
import time
import re
import requests

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')

scopes = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-modify-private,' \
         'playlist-read-private,playlist-modify-public'

sa = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                  scope=scopes)
sp = spotipy.Spotify(auth_manager=sa)
states = ['context', 'track', 'off']
regexsuri = r'\b(?:spotify:track:)[A-Za-z0-9]+'


def reproducir_cancion(cancion):
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

        cola.pop(len(cola) - 1)
        sp.volume(volume)
        for track in cola:
            sp.add_to_queue(track)
        return True
    except SpotifyException:
        return False


def reanudar_playback():
    try:
        sp.start_playback()
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


def get_shuffle_state():
    x = sp.current_playback()
    return x['shuffle_state']


def shuffle(state):
    sp.shuffle(state=state)


def repetir():
    x = sp.current_playback()
    if x:
        x = x['repeat_state']
        index = states.index(x)
        index = index + 1 if index != 2 else 0
        sp.repeat(state=states[index])


def cambiar_dispositivo(device):
    sp.transfer_playback(device_id=config(device), force_play=True)


def agregar_en_cola(cancion):
    track = sp.search(q=f'track:{cancion}', type='track')
    time.sleep(.2)
    track = track['tracks']['items'][0]['uri']
    sp.add_to_queue(track)


def regresar_cancion():
    sp.previous_track()


def cambiar_volumen(valor):
    volume = sp.current_playback()['device']['volume_percent']
    volume += valor
    sp.volume(volume)


def reproducir_playlist(playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'] == playlist]
    if len(playlists) == 0:
        return -1
    sp.start_playback(context_uri=playlists[0]['uri'])
    return 1


def agregar_cancion_pl(cancion, playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'] == playlist]
    if len(playlists) == 0:
        return -1
    pl_id = playlists[0]['id']

    track = cancion
    if not re.match(regexsuri, cancion):
        track = sp.search(q=f'track:{cancion}', type='track')
        track = track['tracks']['items'][0]['uri']

    sp.playlist_add_items(playlist_id=pl_id, items=[track])
    return 1


def borrar_cancion(cancion, playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'] == playlist]
    if len(playlists) == 0:
        return -1
    pl_id = playlists[0]['id']

    if re.match(regexsuri, cancion):
        uri = cancion
    else:
        tracks = sp.playlist_items(playlist_id=pl_id)
        tracks = tracks['items']
        track = [t for t in tracks if t['track']['name'] == cancion]
        if len(track) == 0:
            return -2
        track = track[0]['track']
        uri = track['uri']
    body = {
        "tracks": [
            {
                "uri": uri
            }
        ]
    }

    token = sa.get_cached_token()['access_token']
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
    request = requests.delete(f'https://api.spotify.com/v1/playlists/{pl_id}/tracks', headers=headers, json=body)
    response = request.json()
    print(response)
    return 1


def crear_playlist(nombre):
    user = sp.current_user()
    sp.user_playlist_create(user=user['id'], name=nombre)
