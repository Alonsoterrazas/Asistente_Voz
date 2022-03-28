import pywhatkit
import re
from Models.iaModel import predictCommand
from Options.Spotify.spotifyController import spotify_main, buscaLetra

# from Models.games import piedra_papel_tijeras


class Assistant:

    def __init__(self):
        self.regexYT = r'\b(?:reproduce)\s[a-z0-9\s]+\s(?:en)\s(?:youtube)'
        self.bandActive = False
        self.nameAssistant = 'bicho'

    def querying(self, query):
        print(query)
        # command = predictCommand(query)
        # print(command)
        if query.startswith(self.nameAssistant):
            # Remove first word
            query = query.split(' ', 1)[1]
            self.bandActive = True

        if not self.bandActive:
            return '$ignore$'

        if re.match(self.regexYT, query):
            index = query.find('en')
            query = query[10:index]
            pywhatkit.playonyt(query)
            self.bandActive = False
            return f'reproduciendo {query} en youtube.'

        if 'busca' in query:
            self.bandActive = False
            # Buscar la letra de la cancion que suena
            if query == 'busca la letra de esa canción' or 'busca la letra de esta canción':
                nombre = buscaLetra()
                if nombre:
                    pywhatkit.search(f'{nombre} lyrics')
                    return f'Buscando la letra de {nombre}.'
                return 'No detecto ninguna canción en spotify sonando.'

            query = query[6:]
            pywhatkit.search(query)
            return f'Buscando {query}, espera un momento.'

        # if 'alimenta al perro' in q:
        #     url = 'http://192.168.3.18/feedbuttonclick'
        #     try:
        #         requests.get(url, timeout=2)
        #     except ConnectTimeout:
        #         voz('El alimentador se encuentra fuera de conexion')
        #     except ReadTimeout:
        #         voz('se ha servido la comida')
        #         reproducir_arch('Siu')
        #     break

        if 'piedra papel o tijera' in query:
            # piedra_papel_tijeras()
            return

        if self.spotify_command(query):
            self.bandActive = False
            return spotify_main(query)

    def spotify_command(self, q):
        return 'spotify' or 'volumen' or 'modo aleatorio' or 'canción' or 'playlist' or 'la cola'\
               or 'pausa' or 'ponle play' or 'quita esa madre' in q

    def play_rockScissorsAndPaper(self):
        pass
