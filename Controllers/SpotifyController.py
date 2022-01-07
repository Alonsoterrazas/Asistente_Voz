from Models.spotify import *
from bicho import voz

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
        band = reproducir_playlist(pl)
        if band == -1:
            voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
            return
        voz(f'reproduciendo la playlist {pl} en spotify')
        return

    # Reproducir una canción
    if re.match(reRepro, q):
        if not validaDispositivos():
            voz('No tienes ningun dispositivo activo')
            return

        q = q[10:-11]
        voz(f'reproduciendo {q} en spotify, espere un momento')
        returnValue = reproducirCancion(q)
        if returnValue == 0 or returnValue == 1:
            return
        if returnValue == -2:
            voz('Ocurrió un error al reanudar la canción')
        return

    # Salta la cancion
    if q == 'salta la canción' or q == 'salta esa canción' or q == 'siguiente canción' or q == 'quita esa madre':
        voz('cambiando de canción')
        siguiente_cancion()
        return

    # Regresa la cancion
    if q == 'regresa la canción' or q == 'pon la canción anterior':
        voz('regresando la canción')
        regresar_cancion()
        return

    # Activa el modo aleatorio
    if q == 'pon modo aleatorio' or q == 'activa el modo aleatorio':
        state = get_shuffle_state()
        if state:
            voz('Ya esta activo el modo aleatorio')
            return
        shuffle(True)
        voz('Modo aleatorio activado')
        return

    # Desactiva el modo aleatorio
    if q == 'desactiva el modo aleatorio' or q == 'quita el modo aleatorio':
        state = get_shuffle_state()
        if not state:
            voz('Ya esta desactivo el modo aleatorio')
            return
        shuffle(False)
        voz('Modo aleatorio desactivado')
        return

    # Pausa la cancion
    if q == 'pausa la canción' or q == 'ponle pausa' or q == 'pon pausa':
        voz('pausando la cancion')
        pausar_playback()
        return

    # Reanuda la cancion
    if q == 'ponle play' or q == 'reanuda la canción':
        voz('reanudando la canción')
        reanudar_playback()
        return

    # Sube el volumen
    if q == 'sube el volumen' or q == 'súbele al volumen':
        voz('subiendo el volumen')
        cambiar_volumen(10)
        return

    # Baja el volumen
    if q == 'baja el volumen' or q == 'bájale al volumen':
        voz('bajando el volumen')
        cambiar_volumen(-10)
        return

    # Agrega cancion a la cola
    if re.match(reAggcola, q):
        tokens = q.split(' ')
        song = ' '.join(tokens[1: len(tokens)-3])
        voz(f'agregando {song} a la cola')
        agregar_en_cola(song)
        return

    # Cambia de dispositivo
    if re.match(reCambdisp, q):
        disp = q[24:]
        disp = disp.upper()
        voz(f'cambiando dispositivo a {disp}')
        cambiar_dispositivo(disp)
        return
    if re.match(reCambdisp2, q):
        tokens = q.split(' ')
        if tokens[3] == 'al':
            index = 4
        else:
            index = 5
        disp = ' '.join(tokens[index: len(tokens)])
        disp = disp.upper()
        voz(f'cambiando dispositivo a {disp}')
        cambiar_dispositivo(disp)
        return

    # Agrega cancion a la playlist
    if re.match(reAggCPl, q):
        tokens = q.split(' ')
        pl_i = tokens.index('playlist')
        song = ' '.join(tokens[1: pl_i-2])
        pl = ' '.join(tokens[pl_i+1:])
        band = agregar_cancion_pl(song, pl)
        if band == -1:
            voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
            return
        voz(f'{song} agregado a la playlist {pl}')
        return

    # Crear una playlist
    if re.match(reCreaPl, q):
        tokens = q.split(' ')
        plName = [tokens[i] for i in range(0, len(tokens)) if i >= 4]
        plName = ' '.join(plName)
        voz(f'creando la playlist {plName}')
        crear_playlist(plName)
        return

    # Agrega la cancion actualmente reproduciendose a la playlist
    if re.match(reAggCPL2, q):
        song = cancion_actual()
        tokens = q.split(' ')
        pl_i = tokens.index('playlist')
        pl = ' '.join(tokens[pl_i + 1:])
        band = agregar_cancion_pl(song, pl)
        if band == -1:
            voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
            return
        voz(f'Se ha agregado a la playlist {pl}')
        return

    # Elimina la cancion actualmente reproduciendose de la playlist
    if q == 'quita esta canción de la playlist' or q == 'saca esta canción de la playlist' or q == 'saca esta madre ' \
                                                                                                   'de la playlist':
        pl = playlist_actual()
        if pl == -1:
            voz('No estas escuchando ninguna playlist')
            return
        if pl == -2:
            voz('No puedes quitar canciones en esta playlist')
            return
        song = cancion_actual()
        band = borrar_cancion(song, pl)
        if band == -1:
            voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
            return
        if band == -2:
            voz('No se encontró esta canción dentro de la playlist')
            return
        siguiente_cancion()
        voz(f'Se ha eliminado a la playlist {pl}')
        return

    if 'equipos' in q:
        print(validaDispositivos())
        return

    if 'token' in q:
        get_token()
        return