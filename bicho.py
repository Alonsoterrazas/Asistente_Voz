import pyttsx3
import speech_recognition as sr
import random

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 40)
id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_DANIEL_11.0'
engine.setProperty('voice', id)
r = sr.Recognizer()


# El asistente habla el mensaje
def voz(message):
    engine.say(message)
    engine.runAndWait()


# Escucha tu micrófono y te regresa el audio en texto
def listen_action():
    with sr.Microphone() as fuente:
        print("estoy escuchando")
        audio = r.record(fuente, 4)
        try:
            q = r.recognize_google(audio, language="es")
            return q
        except sr.UnknownValueError:
            voz('''No entendí que dijiste.
            Podrías repetirlo''')
            return None
        except sr.RequestError:
            voz("Ocurrió un error. verifique su connexion a internet Siuuuu")
            return None
        except:
            return None


def call():
    with sr.Microphone() as fuente:
        audio = r.record(fuente, 4)
        try:
            q = r.recognize_google(audio, language="es")
            return q
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except:
            return None
