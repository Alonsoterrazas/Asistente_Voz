import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from decouple import config
import time
import re
import requests
from Models.storeData import getObjectFromPickle, saveObjectOnPickle

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')

scopes = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-modify-private,' \
         'playlist-read-private,playlist-modify-public,user-library-modify,user-library-read,user-top-read'

sa = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                  scope=scopes)
sp = spotipy.Spotify(auth_manager=sa)
states = ['context', 'track', 'off']
regexsuri = r'\b(?:spotify:track:)[A-Za-z0-9]+'


# Empieza a reproducir una cancion sin perder la cola
# Regresa
# 1 en caso de exito
# 0 si la cancion se encuentra reproduciendose
# -2 si algun error interno ocurre
def reproducirCancion(cancion):
    try:
        track = obtenerURICancion(cancion)

        cp = sp.currently_playing()
        # Existe cancion reproduciendose
        if cp:
            cp = cp['item']['uri']
            if track == cp:
                return 0

        sp.start_playback(uris=[track])
        return 1
    except SpotifyException:
        return -2


def cancion_actual():
    cp = sp.currently_playing()
    return cp['item']['uri']


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
    return dis


def validaDispositivos():
    devices = sp.devices()
    devices = devices['devices']
    if len(devices) == 0:
        return False
    activeDevices = [d for d in devices if d['is_active']]
    if len(activeDevices) == 0:
        return False
    return True


def get_token():
    print(sa.get_access_token())


def get_shuffle_state():
    x = sp.current_playback()
    return x['shuffle_state']


def shuffle(state):
    sp.shuffle(state=state)


def playlist_actual():
    x = sp.current_playback()
    x = x['context']
    if not x:
        return -1
    if x['type'] != 'playlist':
        return -1
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['uri'] == x['uri']]
    if len(playlists) == 0:
        return -2
    return playlists[0]['name']


def repetir():
    x = sp.current_playback()
    if x:
        x = x['repeat_state']
        index = states.index(x)
        index = index + 1 if index != 2 else 0
        sp.repeat(state=states[index])


# Smartphone Computer CastAudio
# Cambia el dispositivo donde se reproduce el spotify
# Regresa
# 0 en caso de exito
# -1 si no se menciono ningun apodo valido
# -2 si no encontro ningun dispositivo activo
def cambiar_dispositivo(device):
    nicknamesPhone = ['teléfono', 'cel', 'celular']
    nicknamesPC = ['pc', 'computadora', 'laptop', 'compu']
    nicknamesBocinas = ['bocina']

    userDevices = dispositivos()
    devicesEncontrados = [d for d in userDevices if d['name'] == device]
    if len(devicesEncontrados) > 0:
        sp.transfer_playback(device_id=devicesEncontrados[0]['id'], force_play=True)
        return 0

    typeToFound = ''
    if device in nicknamesPhone:
        typeToFound = 'Smartphone'
    if device in nicknamesPC:
        typeToFound = 'Computer'
    if device in nicknamesBocinas:
        typeToFound = 'CastAudio'
    if typeToFound == '':
        return -1

    devicesEncontrados = [d for d in userDevices if d['type'] == typeToFound]
    if len(devicesEncontrados) == 0:
        return -2
    sp.transfer_playback(device_id=devicesEncontrados[0]['id'], force_play=True)
    return 0


def agregar_en_cola(cancion):
    track = obtenerURICancion(cancion)
    sp.add_to_queue(track)


def regresar_cancion():
    sp.previous_track()


def cambiar_volumen(valor):
    volume = sp.current_playback()['device']['volume_percent']
    volume += valor
    sp.volume(volume)


# Reproduce una playlist
# Regresa
# -1 si no encuentra la playlist
# 1 en caso de exito
def reproducir_playlist(playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'].lower() == playlist]
    if len(playlists) == 0:
        return -1
    sp.start_playback(context_uri=playlists[0]['uri'])
    return 1


def agregar_cancion_pl(cancion, playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'].lower() == playlist]
    if len(playlists) == 0:
        return -1
    pl_id = playlists[0]['id']

    track = cancion
    if not re.match(regexsuri, cancion):
        track = obtenerURICancion(cancion)

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
        track = [t for t in tracks if t['track']['name'].lower() == cancion]
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
    return 1


def crear_playlist(nombre):
    user = sp.current_user()
    sp.user_playlist_create(user=user['id'], name=nombre)


def obtenerURICancion(nombre):
    # Buscar en canciones guardadas
    cancionesGuardadas = getObjectFromPickle('savedTracks')
    if not cancionesGuardadas:
        if guardarCanciones():
            cancionesGuardadas = getObjectFromPickle('savedTracks')
        else:
            # Si falla el metodo guardar canciones no se toma en cuenta
            cancionesGuardadas = []

    cancionesEncontradas = \
        [track['track'] for track in cancionesGuardadas if track['track']['name'].lower() == nombre.lower()]
    if len(cancionesEncontradas) == 0:
        cancionesBusqueda = sp.search(q=f'track:{nombre}', type='track')
        cancionesBusqueda = cancionesBusqueda['tracks']['items']
        # Buscar por artista
        artistasGuardados = getObjectFromPickle('savedArtistas')
        if not artistasGuardados:
            if guardarArtistas():
                artistasGuardados = getObjectFromPickle('savedArtistas')
            else:
                # Mismo caso que las canciones
                artistasGuardados = []

        artistasUris = [artista['uri'] for artista in artistasGuardados]
        cancionesEncontradas = \
            [track for track in cancionesBusqueda if track['artists'][0]['uri'] in artistasUris]
        if len(cancionesEncontradas) > 0:
            return cancionesEncontradas[0]['uri']

        # La mas popular que encuentre
        return cancionesBusqueda[0]['uri']

    if len(cancionesEncontradas) > 1:
        cancionesEncontradas = sorted(cancionesEncontradas, key=lambda i: i['popularity'])

    return cancionesEncontradas[0]['uri']


def guardarCanciones():
    cont = 0
    cantCanciones = 1
    savedTracks = []
    while cantCanciones != 0:
        canciones = sp.current_user_saved_tracks(limit=50, offset=(cont * 50))
        canciones = canciones['items']
        savedTracks.extend(canciones)
        cantCanciones = len(canciones)
        cont += 1

    return saveObjectOnPickle(savedTracks, 'savedTracks')


def guardarArtistas():
    cont = 0
    cantArtistas = 1
    savedArtistas = []
    while cantArtistas != 0:
        artistas = sp.current_user_top_artists(offset=(cont * 20), time_range='long_term')
        artistas = artistas['items']
        savedArtistas.extend(artistas)
        cantArtistas = len(artistas)
        cont += 1

    saveObjectOnPickle(savedArtistas, 'savedArtistas')


def getNameSongPlaying():
    current = sp.currently_playing()
    name = current['item']['name']
    return name
