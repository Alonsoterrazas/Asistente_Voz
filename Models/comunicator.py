import pyttsx3
import speech_recognition as sr
import concurrent.futures
from Models.speechToText import SpeechToText


r = sr.Recognizer()
stt = SpeechToText()

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
        with concurrent.futures.ThreadPoolExecutor() as thread:
            returnValue = thread.submit(stt.audioToTextFromGoogle, audio)
            returnValue = returnValue.result()
            if returnValue is not None:
                talk(returnValue)
