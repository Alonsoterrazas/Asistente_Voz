import pyttsx3
import speech_recognition as sr
import concurrent.futures
from Models.speechToText import audioToText


r = sr.Recognizer()

engine = pyttsx3.init()
# rate = engine.getProperty('rate')
# engine.setProperty('rate', rate - 20)
idRegistroVoz = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_DANIEL_11.0'
engine.setProperty('voice', idRegistroVoz)


# Say the text message
def talk(message):
    engine.say(message)
    engine.runAndWait()


# Escucha tu micrófono y te regresa el audio en texto
def listen_action():
    with sr.Microphone() as fuente:
        audio = r.listen(fuente)
        try:
            with concurrent.futures.ThreadPoolExecutor() as thread:
                returnValue = thread.submit(audioToText, audio)
                returnValue = returnValue.result()
                talk(returnValue)
        except sr.UnknownValueError:
            return "No entendí"
        except sr.RequestError:
            return "Ocurrió un error. verifique su connexion a internet"

