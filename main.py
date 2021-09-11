from bicho import listen_action, voz, call
from Models.games import piedra_papel_tijeras
from Controllers.SpotifyController import spotify_main
import pywhatkit
import re
import winsound

nombre_archivo = 'Resources/Siu.wav'
regexs = r'\b(?:reproduce)\s[a-z0-9\s]+\s(?:en)\s(?:youtube)'


def querying():
    start = True
    while start:
        q = listen_action()
        if not q:
            continue
        q = q.lower()
        print(q)

        if re.match(regexs, q):
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

        if 'spotify' in q:
            spotify_main(q)
            continue

        if 'piedra papel o tijeras' in q:
            voz('preparate para el duelo')
            piedra_papel_tijeras()
            continue

        if q == 'adiós':
            voz('tendre que dejar de luchar siuuuu')
            break


# función que espera a que digas la palabra magic
def wait_for_call():
    while True:
        v = call()
        v = v.lower() if v else None
        print(v)
        if v and 'okay bicho' in v:
            winsound.PlaySound(nombre_archivo, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
            querying()

wait_for_call()












