import random


def piedra_papel_tijeras(option):
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
