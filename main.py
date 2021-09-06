from bicho import listen_action, voz, call
from Models.games import piedra_papel_tijeras
from Controllers.SpotifyController import spotify_main
from Models.Spotify.playback import *
import webbrowser
import time
import pywhatkit
import os
from decouple import config


def querying():
    saludos()
    start = True
    while start:
        q = listen_action()
        if not q:
            continue
        q = q.lower()
        print(q)
        if q == 'youtube':
            voz('reproduciendo youtube.')
            webbrowser.open('https://www.youtube.com')
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



def saludos():
    voz(''' Hola, Soy el bicho, SIUUU.
     comó puedo ayudarte? 
    ''')


# función que espera a que digas la palabra magic
def wait_for_call():
    while True:
        v = call()
        v = v.lower() if v else None
        print(v)
        if v and 'okay bicho' in v:
            querying()


# wait_for_call()
reproducir_cancion('Kill this love')











