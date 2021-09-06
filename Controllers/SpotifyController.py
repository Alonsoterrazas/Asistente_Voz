import re
from Models.Spotify.playback import reanudar_playback, siguiente_cancion, pausar_playback, dispositivos,get_token, reproducir_cancion
from bicho import voz

def spotify_main(q):
    # Reproducir una canción/playlist
    regex = r'\b(?:reproduce)\s[A-Za-z0-9\s]+\s(?:en)\s(?:spotify)'
    if re.match(regex, q):
        index = q.find('en')
        q = q[10:index]
        voz(f'reproduciendo {q} en spotify, espere un momento')
        if not reproducir_cancion(q):
            voz('Ocurrió un error al reanudar la canción')
        return

    if 'siguiente canción' in q:
        voz('cambiando de canción')
        siguiente_cancion()
        return

    if 'pausa la canción' in q:
        voz('pausando la cancion')
        pausar_playback()
        return

    if 'equipos' in q:
        dispositivos()
        return

    if 'token' in q:
        get_token()
        return
