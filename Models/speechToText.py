import speech_recognition as sr
from Models.assistant import Assistant


class SpeechToText:

    def __init__(self):
        self.r = sr.Recognizer()
        self.assistant = Assistant()

    def audioToTextFromGoogle(self, audio):
        try:
            text = self.r.recognize_google(audio, language="es")
            response = self.assistant.querying(text.lower())
            if response == '$ignore$':
                return None
            return response
        except sr.UnknownValueError:
            if self.assistant.bandActive:
                return "No entendí"
        except sr.RequestError:
            if self.assistant.bandActive:
                return "Ocurrió un error. verifique su conexion a internet"
