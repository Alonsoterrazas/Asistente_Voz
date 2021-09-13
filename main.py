from bicho import listen_action, voz, call
from Models.games import piedra_papel_tijeras
from Controllers.SpotifyController import spotify_main
import pywhatkit
import re
from Models.player import reproducir_arch

regexsyt = r'\b(?:reproduce)\s[a-z0-9\s]+\s(?:en)\s(?:youtube)'


def querying():
    start = True
    while start:
        q = listen_action(4)
        if not q:
            continue
        q = q.lower()
        print(q)

        if re.match(regexsyt, q):
            index = q.find('en')
            q = q[10:index]
            voz(f'reproduciendo {q} en youtube.')
            pywhatkit.playonyt(q)
            continue

        if 'busca' in q:
            q = q[6:]
            voz(f'Buscando {q}, espera un momento ')
            pywhatkit.search(q)
            continue

        if spotify_command(q):
            spotify_main(q)
            continue

        if 'piedra papel o tijeras' in q:
            voz('preparate para el duelo')
            piedra_papel_tijeras()
            continue

        if q == 'adiós':
            voz('tendré que dejar de luchar siuuuu')
            break


def spotify_command(q):
    return 'spotify' or 'el volumen' or 'modo aleatorio' or 'canción' or 'playlist' or 'la cola'\
           or 'pausa' or 'ponle play' or 'quita esa madre' in q


# función que espera a que digas la palabra magic
def wait_for_call():
    while True:
        v = call()
        v = v.lower() if v else None
        print(v)
        if v and 'okay bicho' in v:
            reproducir_arch('Siu')
            querying()


wait_for_call()












