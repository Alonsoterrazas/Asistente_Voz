import random
from Models.player import play_file


class Games:
    def __init__(self):
        self.currentGame = None

    def startGame(self, game):
        self.currentGame = game

    def play(self, option):
        if self.currentGame == 'ppt':
            self.currentGame = None
            result = self.piedra_papel_tijeras(option)
            if result[1] == 2:
                play_file('Siu')
            return f"{result[0]}. {'He ganado' if result[1] == 2 else 'Ganaste'}"

    # 1 gana el jugador, 2 el bot, 0 empate
    def piedra_papel_tijeras(self, option):
        posible_actions = ["piedra", "papel", "tijeras"]
        computer_action = random.choice(posible_actions)

        respuesta = [e for e in posible_actions if e in option]
        if len(respuesta) == 1:
            respuesta = respuesta[0]
            if respuesta == computer_action:
                return computer_action, 0
            if respuesta == "piedra":
                if computer_action == "tijeras":
                    return computer_action, 1
                else:
                    return computer_action, 2
            if respuesta == "papel":
                if computer_action == "piedra":
                    return computer_action, 1
                else:
                    return computer_action, 2
            if respuesta == "tijeras":
                if computer_action == "papel":
                    return computer_action, 1
                else:
                    return computer_action, 2

        if len(respuesta) > 1:
            return computer_action, -1

        return computer_action, -2
