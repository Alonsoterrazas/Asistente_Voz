import re
from Models.spotify import siguiente_cancion, pausar_playback, dispositivos, get_token, reproducir_cancion, \
    regresar_cancion, shuffle, get_shuffle_state, reproducir_playlist, agregar_cancion_pl, crear_playlist, reanudar_playback, \
    agregar_en_cola, cambiar_dispositivo, cambiar_volumen, borrar_cancion, cancion_actual, playlist_actual


class Spotify_controller:
    def __init__(self, bicho):
        self.bicho = bicho
        self.reRepro = r'\b(?:reproduce)\s[A-Za-z0-9\s]+\s(?:en spotify)'
        self.reAggcola = r'\b(?:agrega|mete|pon|añade)\s[A-Za-z0-9\s]+\s(?:en la cola|a la cola)'
        self.reCambdisp = r'\b(?:reproduce spotify en)\s(?:el|la)\s[A-Za-z0-9\s]+'
        self.reCambdisp2 = r'\b(?:pasa el spotify)\s(?:al|a la)\s[A-Za-z0-9\s]+'
        self.reReproPl = r'\b(?:reproduce|pon)\s(?:la playlist)\s[A-Za-z0-9\s]+\s(?:en spotify)'
        self.reAggCPl = r'\b(?:agrega|mete|pon|añade)\s[A-Za-z0-9\s]+\s(?:a|en)\s(?:la playlist)\s[A-Za-z0-9\s]+'
        self.reCreaPl = r'\b(?:crea|haz)\s(?:una playlist llamada)\s[A-Za-z0-9\s]+'
        self.reAggCPL2 = r'\b(?:agrega|mete|pon|añade)\s(?:esta canción)\s(?:a|en)\s(?:la playlist)\s[A-Za-z0-9\s]+'


    def spotify_main(self, q):
        if re.match(self.reReproPl, q):
            tokens = q.split(' ')
            pl = ' '.join(tokens[3: len(tokens) - 2])
            band = reproducir_playlist(pl)
            if band == -1:
                self.bicho.voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
                return
            self.bicho.voz(f'reproduciendo la playlist {pl} en spotify')
            return
        # Reproducir una canción
        if re.match(self.reRepro, q):
            q = q[10:-11]
            self.bicho.voz(f'reproduciendo {q} en spotify, espere un momento')
            if not reproducir_cancion(q):
                self.bicho.voz('Ocurrió un error al reanudar la canción')
            return

        if q == 'salta la canción' or q == 'salta esa canción' or q == 'siguiente canción' or q == 'quita esa madre':
            self.bicho.voz('cambiando de canción')
            siguiente_cancion()
            return

        if q == 'regresa la canción' or q == 'pon la canción anterior':
            self.bicho.voz('regresando la canción')
            regresar_cancion()
            return

        if q == 'pon modo aleatorio' or q == 'activa el modo aleatorio':
            state = get_shuffle_state()
            if state:
                self.bicho.voz('Ya esta activo el modo aleatorio')
                return
            shuffle(True)
            self.bicho.voz('Modo aleatorio activado')
            return

        if q == 'desactiva el modo aleatorio' or q == 'quita el modo aleatorio':
            state = get_shuffle_state()
            if not state:
                self.bicho.voz('Ya esta desactivo el modo aleatorio')
                return
            shuffle(False)
            self.bicho.voz('Modo aleatorio desactivado')
            return

        if q == 'pausa la canción' or q == 'ponle pausa' or q == 'pon pausa':
            self.bicho.voz('pausando la cancion')
            pausar_playback()
            return

        if q == 'ponle play' or q == 'reanuda la canción':
            self.bicho.voz('reanudando la canción')
            reanudar_playback()
            return

        if q == 'sube el volumen' or q == 'súbele al volumen':
            self.bicho.voz('subiendo el volumen')
            cambiar_volumen(10)
            return

        if q == 'baja el volumen' or q == 'bájale al volumen':
            self.bicho.voz('bajando el volumen')
            cambiar_volumen(-10)
            return

        if re.match(self.reAggcola, q):
            tokens = q.split(' ')
            song = ' '.join(tokens[1: len(tokens)-3])
            self.bicho.voz(f'agregando {song} a la cola')
            agregar_en_cola(song)
            return

        if re.match(self.reCambdisp, q):
            disp = q[24:]
            disp = disp.upper()
            self.bicho.voz(f'cambiando dispositivo a {disp}')
            cambiar_dispositivo(disp)
            return
        if re.match(self.reCambdisp2, q):
            tokens = q.split(' ')
            if tokens[3] == 'al':
                index = 4
            else:
                index = 5
            disp = ' '.join(tokens[index: len(tokens)])
            disp = disp.upper()
            self.bicho.voz(f'cambiando dispositivo a {disp}')
            cambiar_dispositivo(disp)
            return

        if re.match(self.reAggCPl, q):
            tokens = q.split(' ')
            pl_i = tokens.index('playlist')
            song = ' '.join(tokens[1: pl_i-2])
            pl = ' '.join(tokens[pl_i+1:])
            band = agregar_cancion_pl(song, pl)
            if band == -1:
                self.bicho.voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
                return
            self.bicho.voz(f'{song} agregado a la playlist {pl}')
            return

        if re.match(self.reCreaPl, q):
            tokens = q.split(' ')
            pl = ' '.join(tokens[4])
            self.bicho.voz(f'creando la playlist {pl}')
            crear_playlist(pl)
            return

        if re.match(self.reAggCPL2, q):
            song = cancion_actual()
            tokens = q.split(' ')
            pl_i = tokens.index('playlist')
            pl = ' '.join(tokens[pl_i + 1:])
            band = agregar_cancion_pl(song, pl)
            if band == -1:
                self.bicho.voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
                return
            self.bicho.voz(f'Se ha agregado a la playlist {pl}')
            return

        if q == 'quita esta canción de la playlist' or q == 'saca esta canción de la playlist' or q == 'saca esta madre de la playlist':
            pl = playlist_actual()
            if pl == -1:
                self.bicho.voz('No estas escuchando ninguna playlist')
                return
            if pl == -2:
                self.bicho.voz('No puedes quitar canciones en esta playlist')
                return
            song = cancion_actual()
            band = borrar_cancion(song, pl)
            if band == -1:
                self.bicho.voz('No se encontró ninguna playlist con ese nombre en tu biblioteca')
                return
            if band == -2:
                self.bicho.voz('No se encontró esta canción dentro de la playlist')
                return
            self.bicho.voz(f'Se ha eliminado a la playlist {pl}')
            return

        if 'equipos' in q:
            dispositivos()
            return

        if 'token' in q:
            get_token()
            return