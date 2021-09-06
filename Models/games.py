import random
from bicho import listen_action, voz


def piedra_papel_tijeras():
    posible_actions = ["piedra", "papel", "tijeras"]
    computer_action = random.choice(posible_actions)
    q = listen_action().lower()
    if q == computer_action:
        voz(' es un empate :)')
    elif q == "piedra":
        if computer_action == "tijeras":
            voz(f"{computer_action}. haz ganado!")
        else:
            voz(f"{computer_action}. gané, SIUUUU!")
    elif q == "papel":
        if computer_action == "piedra":
            voz(f"{computer_action}. haz ganado!")
        else:
            voz(f"{computer_action}. gané, SIUUUU!")
    elif q == "tijeras":
        if computer_action == "piedra":
            voz(f"{computer_action}. gané, SIUUUU!")
        else:
            voz(f"{computer_action}. haz ganado!")