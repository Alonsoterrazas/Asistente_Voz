from requests.exceptions import ConnectTimeout, ReadTimeout
from bicho import listen_action, voz, call
from Models.games import piedra_papel_tijeras
from Controllers.SpotifyController import spotify_main, buscaLetra
import pywhatkit
import re
from Models.player import reproducir_arch
import requests

regexsyt = r'\b(?:reproduce)\s[a-z0-9\s]+\s(?:en)\s(?:youtube)'


def querying():
    start = True
    while start:
        q = listen_action()
        # q = 'baja el volumen'
        if not q:
            continue
        q = q.lower()
        print(q)

        if re.match(regexsyt, q):
            index = q.find('en')
            q = q[10:index]
            voz(f'reproduciendo {q} en youtube.')
            pywhatkit.playonyt(q)
            break

        if 'busca' in q:
            # Buscar la letra de la cancion que suena
            if q == 'busca la letra de esa canción':
                nombre = buscaLetra()
                if nombre:
                    voz(f'Buscando la letra de {nombre}')
                    pywhatkit.search(f'{nombre} lyrics')
                    return
                voz('No detecto ninguna canción en spotify sonando')
                return

            q = q[6:]
            voz(f'Buscando {q}, espera un momento')
            pywhatkit.search(q)
            break

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

        if 'piedra papel o tijera' in q:
            voz('preparate para el duelo')
            piedra_papel_tijeras()
            break

        if spotify_command(q):
            spotify_main(q)
            break


def spotify_command(q):
    if 'spotify' in q:
        return True
    if 'volumen' in q:
        return True
    if 'modo aleatorio' in q:
        return True
    if 'playlist' in q:
        return True
    if 'la cola' in q:
        return True
    if 'pausa' in q:
        return True
    if 'ponle play' in q:
        return True
    if 'quita esa madre' in q:
        return True
    return False


# función que espera a que digas la palabra magic
def wait_for_call():
    while True:
        v = call(4)
        v = v.lower() if v else None
        print(v)
        if v and 'okay bicho' in v:
            reproducir_arch('Siu')
            querying()


if __name__ == '__main__':
    wait_for_call()
    # querying()
