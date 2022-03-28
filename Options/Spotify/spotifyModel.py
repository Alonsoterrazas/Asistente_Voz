import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from decouple import config
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
def playSong(cancion):
    try:
        track = getURITrack(cancion)

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


# Reproduce una playlist
# Regresa
# -1 si no encuentra la playlist
# 1 en caso de exito
def playPlaylist(playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'].lower() == playlist]
    if len(playlists) == 0:
        return -1
    sp.start_playback(context_uri=playlists[0]['uri'])
    return 1


def currentSong():
    cp = sp.currently_playing()
    return cp['item']['uri']


def resumePlayback():
    try:
        sp.start_playback()
        return True
    except SpotifyException:
        return False


def pausePlayback():
    try:
        sp.pause_playback()
        return True
    except SpotifyException:
        return False


def nextSong():
    try:
        sp.next_track()
        return True
    except SpotifyException:
        return False


def devices():
    devs = sp.devices()
    devs = devs['devices']
    return devs


def validateDevicesActive():
    devs = sp.devices()
    devs = devs['devices']
    if len(devs) == 0:
        return False
    activeDevices = [d for d in devs if d['is_active']]
    if len(activeDevices) == 0:
        return False
    return True


def get_token():
    print(sa.get_access_token())


def getShuffleState():
    x = sp.current_playback()
    return x['shuffle_state']


def setShuffleState(state):
    sp.shuffle(state=state)


def currentPlaylist():
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


def repeat():
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
def changeDevice(device):
    nicknamesPhone = ['teléfono', 'cel', 'celular']
    nicknamesPC = ['pc', 'computadora', 'laptop', 'compu']
    nicknamesBocinas = ['bocina']

    userDevices = devices()
    devicesFounded = [d for d in userDevices if d['name'] == device]
    if len(devicesFounded) > 0:
        sp.transfer_playback(device_id=devicesFounded[0]['id'], force_play=True)
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

    devicesFounded = [d for d in userDevices if d['type'] == typeToFound]
    if len(devicesFounded) == 0:
        return -2
    sp.transfer_playback(device_id=devicesFounded[0]['id'], force_play=True)
    return 0


def addToQueue(cancion):
    track = getURITrack(cancion)
    sp.add_to_queue(track)


def previousTrack():
    sp.previous_track()


def controlVolumen(valor):
    volume = sp.current_playback()['device']['volume_percent']
    volume += valor
    sp.volume(volume)


def addSongToPlaylist(track, playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'].lower() == playlist]
    if len(playlists) == 0:
        return -1
    pl_id = playlists[0]['id']

    track = track
    if not re.match(regexsuri, track):
        track = getURITrack(track)

    sp.playlist_add_items(playlist_id=pl_id, items=[track])
    return 1


def deleteSongOnPlaylist(track, playlist):
    playlists = sp.current_user_playlists()
    playlists = playlists['items']
    playlists = [pl for pl in playlists if pl['name'] == playlist]
    if len(playlists) == 0:
        return -1
    pl_id = playlists[0]['id']

    if re.match(regexsuri, track):
        uri = track
    else:
        tracks = sp.playlist_items(playlist_id=pl_id)
        tracks = tracks['items']
        track = [t for t in tracks if t['track']['name'].lower() == track]
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


def createPlaylist(name):
    user = sp.current_user()
    sp.user_playlist_create(user=user['id'], name=name)


def getURITrack(name):
    # Buscar en canciones guardadas
    savedTracks = getObjectFromPickle('savedTracks')
    if not savedTracks:
        if saveTracks():
            savedTracks = getObjectFromPickle('savedTracks')
        else:
            # Si falla el metodo guardar canciones no se toma en cuenta
            savedTracks = []

    tracksFounded = \
        [track['track'] for track in savedTracks if track['track']['name'].lower() == name.lower()]
    if len(tracksFounded) == 0:
        tracksSearch = sp.search(q=f'track:{name}', type='track')
        tracksSearch = tracksSearch['tracks']['items']
        # Buscar por artista
        savedArtists = getObjectFromPickle('savedArtistas')
        if not savedArtists:
            if saveArtists():
                savedArtists = getObjectFromPickle('savedArtistas')
            else:
                # Mismo caso que las canciones
                savedArtists = []

        artistasUris = [artista['uri'] for artista in savedArtists]
        tracksFounded = \
            [track for track in tracksSearch if track['artists'][0]['uri'] in artistasUris]
        if len(tracksFounded) > 0:
            return tracksFounded[0]['uri']

        # La mas popular que encuentre
        return tracksSearch[0]['uri']

    if len(tracksFounded) > 1:
        tracksFounded = sorted(tracksFounded, key=lambda i: i['popularity'])

    return tracksFounded[0]['uri']


def saveTracks():
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


def savePlaylists():
    cont = 0
    cantPlaylists = 1
    savedPlaylists = []
    while cantPlaylists != 0:
        playlist = sp.current_user_playlists(limit=50, offset=(cont * 50))
        playlist = playlist['items']
        savedPlaylists.extend(playlist)
        cantPlaylists = len(playlist)
        cont += 1

    return saveObjectOnPickle(savedPlaylists, 'savedPlaylists')


def saveArtists():
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


def getNameCurrentTrack():
    current = sp.currently_playing()
    name = current['item']['name']
    return name


savePlaylists()