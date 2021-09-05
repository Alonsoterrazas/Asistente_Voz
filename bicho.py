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
        r.pause_threshold = 0.8
        print("estoy escuchando")
        audio = r.listen(fuente)
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


def listen():
    with sr.Microphone() as fuente:
        #microfonos = fuente.list_microphone_names()
        #for mic in microfonos:
            #print(mic)
        audio = r.listen(fuente)
        try:
            q = r.recognize_google(audio, language="es")
            return q
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except:
            return None

#def prueba():
   # for device_index in sr.Microphone.list_working_microphones():
    #    m = sr.Microphone(device_index=device_index)
     #   print(m)
      #  break
    #else:
     #   print("No working microphones found!")

def piedra_papel_tijeras():

        posible_actions =  ["piedra", "papel", "tijeras"]
        computer_action =  random.choice(posible_actions)
        q = listen_action()
        print(q)
        if q == computer_action:
            voz(' es un empate :)')
        elif q == "piedra":
           if computer_action == "tijeras":
               voz(f"haz elegido {q} y la computadora ha elegido {computer_action} haz ganado!")
           else:
               voz(f"haz elegido {q} y la computadora ha elegido {computer_action}  el ganador soy yo, SIUUUU!")
        elif q == "papel":
            if computer_action == "piedra":
                voz(f"haz elegido {q} y la computadora ha elegido {computer_action} el ganador eres tu!")
            else:
                voz(f"haz elegido {q} y la computadora ha elegido {computer_action} el ganador soy yo, SIUUUU!")
        elif q == "tijeras":
            if computer_action == "piedra":
                voz(f"haz elegido {q} y la computadora ha elegido {computer_action} el ganador soy yo, SIUUUU!")
            else:
                voz(f"haz elegido {q} y la computadora ha elegido {computer_action} el ganador eres tu!")




