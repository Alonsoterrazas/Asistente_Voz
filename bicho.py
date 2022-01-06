import pyttsx3
import speech_recognition as sr

class Bicho:
    def __init__(self):
        self.engine = pyttsx3.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 40)
        id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_DANIEL_11.0'
        self.engine.setProperty('voice', id)
        self.r = sr.Recognizer()


    # El asistente habla el mensaje
    def voz(self,message):
        self.engine.say(message)
        self.engine.runAndWait()


    # Escucha tu micrófono y te regresa el audio en texto
    def listen_action(self):
        with sr.Microphone() as fuente:
            audio = self.r.listen(fuente)
            try:
                q = self.r.recognize_google(audio, language="es")
                return q
            except sr.UnknownValueError:
                self.voz('''No entendí que dijiste.
                Podrías repetirlo''')
                return None
            except sr.RequestError:
                self.voz("Ocurrió un error. verifique su connexion a internet Siuuuu")
                return None
            except:
                return None


    def call(self):
        with sr.Microphone() as fuente:
            audio = self.r.record(fuente, 4)
            try:
                q = self.r.recognize_google(audio, language="es")
                return q
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
            except:
                return None
