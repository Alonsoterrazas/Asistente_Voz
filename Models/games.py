import random


from bicho import Bicho
from Models.player import reproducir_arch

class Games:
    def __init__(self):
        self.bicho = Bicho()

    def piedra_papel_tijeras(self):
        posible_actions = ["piedra", "papel", "tijeras"]
        computer_action = random.choice(posible_actions)
        self.bicho.voz('¿Que quieres jugar?')

        while True:
            q = self.bicho.listen_action()
            if q:
                break
        q = q.lower()

        if q == computer_action:
            self.bicho.voz('es un empate :)')
            return
        if q == "piedra":
            if computer_action == "tijeras":
                self.bicho.voz(f"{computer_action}. haz ganado!")
            else:
                self.bicho.voz(f"{computer_action}. gané")
                reproducir_arch('Siu')
            return
        if q == "papel":
            if computer_action == "piedra":
                self.bicho.voz(f"{computer_action}. haz ganado!")
            else:
                self.bicho.voz(f"{computer_action}. gané")
                reproducir_arch('Siu')
            return
        if q == "tijeras":
            if computer_action == "piedra":
                self.bicho.voz(f"{computer_action}. gané")
                reproducir_arch('Siu')
            else:
                self.bicho.voz(f"{computer_action}. haz ganado!")
            return
        self.bicho.voz('Dejate de mamadas y di algo bien')

