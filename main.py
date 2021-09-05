from bicho import listen_action, voz, listen, piedra_papel_tijeras
import webbrowser
import datetime
import pywhatkit
import os
import yahoo_finance as yf
import pyjokes
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')
COMPUTADORA = config('COMPUTADORA_ID')
CELULAR = config('CELULAR_ID')

scopes = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL, scope=scopes))



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

        if 'reproduce en spotify' in q:
            q = q[20:]
            voz(f'reproduciendo {q} en spotify, espere un momento')
            sp.start_playback()

        if 'siguiente canción' in q:
            voz('cambiando de canción')
            sp.next_track()

        if 'pausa la canción' in q:
            voz('pausando la cancion')
            sp.pause_playback()
            continue

        if 'piedra papel o tijeras' in q:
            voz('preparate para el duelo')
            piedra_papel_tijeras()
            continue


        if 'equipos' in q:
            dispositivos = sp.devices()
            dispositivos = dispositivos['devices']
            for i in dispositivos:
                print(i)



        if q == 'adiós':
            voz('tendre que dejar de luchar siuuuu')
            break



def saludos():
    voz(''' Hola, Soy el bicho, SIUUU.
     comó puedo ayudarte? 
    ''')


# función que espera a que digas la palabra magic
def listener():
    while True:
        v = listen()
        v = v.lower() if v else None
        print(v)
        if v == "okay bicho":
            querying()


listener()












