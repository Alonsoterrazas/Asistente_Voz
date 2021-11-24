import os

from requests.exceptions import ConnectTimeout, ReadTimeout
from bicho import Bicho
from Models.games import Games
from Controllers.SpotifyController import Spotify_controller
import pywhatkit
import re
from Models.player import reproducir_arch
import requests
from Views.Configuracion import VentanaConfiguracion


class Main:
    def __init__(self):
        self.spotify_controller = Spotify_controller()
        self.games = Games()
        self.regexsyt = r'\b(?:reproduce)\s[a-z0-9\s]+\s(?:en)\s(?:youtube)'
        self.bicho = Bicho()
        self.regexsruta = r'\b(?:abre)\s[a-z0-9\s]'

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
                break

            if 'busca' in q:
                q = q[6:]
                self.bicho.voz(f'Buscando {q}, espera un momento ')
                pywhatkit.search(q)
                break

            if 'abre la configuración' in q:
                self.bicho.voz(f'abriendo la ventana de configuración')
                vc = VentanaConfiguracion()
                vc.mostrarVista()
                break

            if re.match(self.regexsruta, q):
                index = q.find('e')
                nombre = q[index + 2:]
                self.bicho.voz(f'abriendo {nombre}')

                with open('data.txt', 'r') as file:
                    filedata = file.read()
                    indexnombre = filedata.index(nombre)
                    indexruta1 = filedata.index("'", indexnombre) + 1
                    indexruta2 = filedata.index("'", indexruta1)
                    ruta = filedata[indexruta1:indexruta2]
                os.system(f'"{ruta}"')
                break



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
                break

            if self.spotify_command(q):
                self.spotify_controller.spotify_main(q)
                break

            if 'piedra papel o tijeras' in q:
                self.bicho.voz('preparate para el duelo')
                self.games.piedra_papel_tijeras()
                break

            if q == 'adiós':
                self.bicho.voz('tendré que dejar de luchar siuuuu')
                # TODO meter audio de fue muy bonito estar en madrid
                break

    def spotify_command(self, q):
        return 'spotify' or 'volumen' or 'modo aleatorio' or 'canción' or 'playlist' or 'la cola' \
               or 'pausa' or 'ponle play' or 'quita esa madre' in q

    # función que espera a que digas la palabra magic
    def wait_for_call(self):
        while True:
            v = self.bicho.call()
            v = v.lower() if v else None
            print(v)
            with open('data.txt', 'r') as file:
                filedata = file.read()
                indexcmdact = filedata.index('COMANDO_ACTIVACION')
                indexcmdviejo1 = filedata.index("'", indexcmdact) + 1
                indexcmdviejo2 = filedata.index("'", indexcmdviejo1)
                comact = filedata[indexcmdviejo1:indexcmdviejo2]
            if v and comact in v:
                reproducir_arch('Siu')
                self.querying()


if __name__ == '__main__':
    main = Main()
    main.wait_for_call()


