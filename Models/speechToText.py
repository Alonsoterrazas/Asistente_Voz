import speech_recognition as sr
import Models.assistant as assist

r = sr.Recognizer()


def audioToText(audio):
    text = r.recognize_google(audio, language="es")
    response = assist.querying(text.lower())
    return response
