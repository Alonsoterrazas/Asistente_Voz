from Options.Spotify.spotifyModel import *

reRepro = r'\b(?:reproduce)\s[A-Za-z0-9\s]+\s(?:en spotify)'
reAggcola = r'\b(?:agrega|mete|pon|añade)\s[A-Za-z0-9\s]+\s(?:en la cola|a la cola)'
reCambdisp = r'\b(?:reproduce spotify en)\s(?:el|la)\s[A-Za-z0-9\s]+'
reCambdisp2 = r'\b(?:pasa el spotify)\s(?:al|a la)\s[A-Za-z0-9\s]+'
reReproPl = r'\b(?:reproduce|pon)\s(?:la playlist)\s[A-Za-z0-9\s]+\s(?:en spotify)'
reAggCPl = r'\b(?:agrega|mete|pon|añade)\s[A-Za-z0-9\s]+\s(?:a|en)\s(?:la playlist)\s[A-Za-z0-9\s]+'
reAggCPL2 = r'\b(?:agrega|mete|pon|añade)\s(?:esta canción)\s(?:a|en)\s(?:la playlist)\s[A-Za-z0-9\s]+'
reCreaPl = r'\b(?:crea|haz)\s(?:una playlist llamada)\s[A-Za-z0-9\s]+'


def spotify_main(q):
    # Reproducir una playlist
    if re.match(reReproPl, q):
        tokens = q.split(' ')
        pl = ' '.join(tokens[3: len(tokens) - 2])
        band = playPlaylist(pl)
        if band == -1:
            return 'No se encontró ninguna playlist con ese nombre en tu biblioteca'
        return f'reproduciendo la playlist {pl} en spotify'

    # Reproducir una canción
    # TODO Cuando diga reproduce no solamente sean canciones, puedan ser playlists, albumes o rolas de un artista
    if re.match(reRepro, q):
        if not validateDevicesActive():
            return 'No tienes ningun dispositivo activo'

        q = q[10:-11]
        returnValue = playSong(q)
        if returnValue == 0 or returnValue == 1:
            return f'reproduciendo {q} en spotify'
        if returnValue == -2:
            return 'Ocurrió un error al reanudar la canción'

    # Salta la cancion
    if q == 'salta la canción' or q == 'salta esa canción' or q == 'siguiente canción' or q == 'quita esa madre':
        nextSong()
        return 'cambiando de canción'

    # Regresa la cancion
    if q == 'regresa la canción' or q == 'pon la canción anterior':
        previousTrack()
        return 'regresando la canción'

    # Activa el modo aleatorio
    if q == 'pon modo aleatorio' or q == 'activa el modo aleatorio':
        state = getShuffleState()
        if state:
            return 'Ya esta activo el modo aleatorio'
        setShuffleState(True)
        return 'Modo aleatorio activado'

    # Desactiva el modo aleatorio
    if q == 'desactiva el modo aleatorio' or q == 'quita el modo aleatorio':
        state = getShuffleState()
        if not state:
            return 'Ya esta desactivo el modo aleatorio'
        setShuffleState(False)
        return 'Modo aleatorio desactivado'

    # Pausa la cancion
    if q == 'pausa la canción' or q == 'ponle pausa' or q == 'pon pausa':
        pausePlayback()
        return 'pausando la cancion'

    # Reanuda la cancion
    if q == 'ponle play' or q == 'reanuda la canción':
        resumePlayback()
        return 'reanudando la canción'

    # Sube el volumen
    if q == 'sube el volumen' or q == 'súbele al volumen':
        controlVolumen(10)
        return 'subiendo el volumen'

    # Baja el volumen
    if q == 'baja el volumen' or q == 'bájale al volumen':
        controlVolumen(-10)
        return 'bajando el volumen'

    # Agrega cancion a la cola
    if re.match(reAggcola, q):
        tokens = q.split(' ')
        song = ' '.join(tokens[1: len(tokens)-3])
        addToQueue(song)
        return f'agregando {song} a la cola'

    # Cambia de dispositivo
    if re.match(reCambdisp, q):
        if not validateDevicesActive():
            return 'No tienes ningún dispositivo activo'
        disp = q[24:]
        disp = disp.lower()
        regreso = changeDevice(disp)
        if regreso == -1:
            return 'No mencionaste ningún apodo válido'
        if regreso == -2:
            return 'No encontré ningún dispositivo'
        return f'cambiando dispositivo a {disp}'

    if re.match(reCambdisp2, q):
        if not validateDevicesActive():
            return 'No tienes ningún dispositivo activo'
        tokens = q.split(' ')
        if tokens[3] == 'al':
            index = 4
        else:
            index = 5
        disp = ' '.join(tokens[index: len(tokens)])
        disp = disp.lower()
        regreso = changeDevice(disp)
        if regreso == -1:
            return 'No mencionaste ningún apodo válido'
        if regreso == -2:
            return 'No encontré ningún dispositivo'
        return f'cambiando dispositivo a {disp}'

    # Agrega cancion a la playlist
    if re.match(reAggCPl, q):
        tokens = q.split(' ')
        pl_i = tokens.index('playlist')
        song = ' '.join(tokens[1: pl_i-2])
        pl = ' '.join(tokens[pl_i+1:])
        band = addSongToPlaylist(song, pl)
        if band == -1:
            return 'No se encontró ninguna playlist con ese nombre en tu biblioteca'
        return f'{song} agregado a la playlist {pl}'

    # Crear una playlist
    if re.match(reCreaPl, q):
        tokens = q.split(' ')
        plName = [tokens[i] for i in range(0, len(tokens)) if i >= 4]
        plName = ' '.join(plName)
        createPlaylist(plName)
        return f'creando la playlist {plName}'

    # Agrega la cancion actualmente reproduciendose a la playlist
    if re.match(reAggCPL2, q):
        song = currentSong()
        tokens = q.split(' ')
        pl_i = tokens.index('playlist')
        pl = ' '.join(tokens[pl_i + 1:])
        band = addSongToPlaylist(song, pl)
        if band == -1:
            return 'No se encontró ninguna playlist con ese nombre en tu biblioteca'
        return f'Se ha agregado a la playlist {pl}'

    # Elimina la cancion actualmente reproduciendose de la playlist
    if q == 'quita esta canción de la playlist' or q == 'saca esta canción de la playlist' or q == 'saca esta madre ' \
                                                                                                   'de la playlist':
        pl = currentPlaylist()
        if pl == -1:
            return 'No estas escuchando ninguna playlist'
        if pl == -2:
            return 'No puedes quitar canciones en esta playlist'
        song = currentSong()
        band = deleteSongOnPlaylist(song, pl)
        if band == -1:
            return 'No se encontró ninguna playlist con ese nombre en tu biblioteca'
        if band == -2:
            return 'No se encontró esta canción dentro de la playlist'
        nextSong()
        return f'Se ha eliminado a la playlist {pl}'

    if 'equipos' in q:
        print(validateDevicesActive())
        return

    if 'token' in q:
        get_token()
        return


def buscaLetra():
    if validateDevicesActive():
        name = getNameCurrentTrack()
        return name
    return False
