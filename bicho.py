import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 40)
idRegistroVoz = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_DANIEL_11.0'
engine.setProperty('voice', idRegistroVoz)
r = sr.Recognizer()


# El asistente habla el mensaje
def voz(message):
    engine.say(message)
    engine.runAndWait()


# Escucha tu micrófono y te regresa el audio en texto
def listen_action():
    with sr.Microphone() as fuente:
        audio = r.listen(fuente)
        try:
            q = r.recognize_google(audio, language="es")
            return q
        except sr.UnknownValueError:
            voz('''No entendí que dijiste.
            Podrías repetirlo''')
            return None
        except sr.RequestError:
            voz("Ocurrió un error. verifique su connexion a internet")
            return None
        except:
            return None


def call(duracion):
    with sr.Microphone() as fuente:
        audio = r.record(fuente, duracion)
        try:
            q = r.recognize_google(audio, language="es")
            return q
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except:
            return None
