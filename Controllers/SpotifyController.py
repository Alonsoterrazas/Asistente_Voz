import re
from Models.Spotify.playback import reanudar_playback, siguiente_cancion, pausar_playback, dispositivos, get_token, reproducir_cancion
from bicho import voz
'''
reproduce {c} en spotify
salta la cancion
regresa la cancion
pon modo aleatorio 
pausa la cancion
reanuda la cancion
sube el volumen
baja el volumen
agrega {c} a la cola
quita {c} de la cola
reproduce spotify en el/la {d}
reproduce la playlist {p} en spotify
agrega {c} a la playlist {p}
crea una playlist llamada {p}
agrega esta cancion a la playlist {p}
quita esa cancion de la playlist

'''
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

