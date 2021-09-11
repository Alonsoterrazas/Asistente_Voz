import random
from bicho import listen_action, voz
from Models.player import reproducir_arch


def piedra_papel_tijeras():
    posible_actions = ["piedra", "papel", "tijeras"]
    computer_action = random.choice(posible_actions)
    voz('¿Que quieres jugar?')

    while True:
        q = listen_action(2)
        if q:
            break
    q = q.lower()

    if q == computer_action:
        voz('es un empate :)')
        return
    if q == "piedra":
        if computer_action == "tijeras":
            voz(f"{computer_action}. haz ganado!")
        else:
            voz(f"{computer_action}. gané")
            reproducir_arch('Siu')
        return
    if q == "papel":
        if computer_action == "piedra":
            voz(f"{computer_action}. haz ganado!")
        else:
            voz(f"{computer_action}. gané")
            reproducir_arch('Siu')
        return
    if q == "tijeras":
        if computer_action == "piedra":
            voz(f"{computer_action}. gané")
            reproducir_arch('Siu')
        else:
            voz(f"{computer_action}. haz ganado!")
        return
    voz('Dejate de mamadas y di algo bien')
    piedra_papel_tijeras()
