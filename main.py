from requests.exceptions import ConnectTimeout, ReadTimeout
from bicho import Bicho
from Models.games import piedra_papel_tijeras
from Controllers.SpotifyController import spotify_main
import pywhatkit
import re
from Models.player import reproducir_arch
import requests

class Main:
    def __init__(self):
        self.regexsyt = r'\b(?:reproduce)\s[a-z0-9\s]+\s(?:en)\s(?:youtube)'
        self.bicho = Bicho()


    def querying(self):
        start = True
        while start:
            q = self.bicho.listen_action()
            if not q:
                continue
            q = q.lower()
            print(q)

            if re.match(self.regexsyt, q):
                index = q.find('en')
                q = q[10:index]
                self.bicho.voz(f'reproduciendo {q} en youtube.')
                pywhatkit.playonyt(q)
                continue

            if 'busca' in q:
                q = q[6:]
                self.bicho.voz(f'Buscando {q}, espera un momento ')
                pywhatkit.search(q)
                continue

            if 'alimenta al perro' in q:
                url = 'http://192.168.3.18/feedbuttonclick'
                try:
                    requests.get(url, timeout=2)
                except ConnectTimeout:
                    self.bicho.voz('El alimentador se encuentra fuera de conexion')
                    reproducir_arch('Siu')
                except ReadTimeout:
                    self.bicho.voz('se ha servido la comida')
                    reproducir_arch('Siu')
                continue

            if self.spotify_command(q):
                spotify_main(q)
                continue

            if 'piedra papel o tijeras' in q:
                self.bicho.voz('preparate para el duelo')
                piedra_papel_tijeras()
                continue

            if q == 'adiós':
                self.bicho.voz('tendré que dejar de luchar siuuuu')
                # TODO meter audio de fue muy bonito estar en madrid
                break


    def spotify_command(self,q):
        return 'spotify' or 'volumen' or 'modo aleatorio' or 'canción' or 'playlist' or 'la cola'\
               or 'pausa' or 'ponle play' or 'quita esa madre' in q


    # función que espera a que digas la palabra magic
    def wait_for_call(self):
        while True:
            v = self.bicho.call()
            v = v.lower() if v else None
            print(v)
            if v and 'okay bicho' in v:
                reproducir_arch('Siu')
                self.querying()


if __name__ == '__main__':
    main = Main()
    main.wait_for_call()
