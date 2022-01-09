import random
from bicho import call, voz
from Models.player import reproducir_arch


def piedra_papel_tijeras():
    posible_actions = ["piedra", "papel", "tijeras"]
    computer_action = random.choice(posible_actions)
    voz('Que quieres jugar')

    while True:
        q = call(2)
        if q:
            break
    q = q.lower()

    print(q)
    respuesta = [e for e in posible_actions if e in q]
    if len(respuesta) == 1:
        respuesta = respuesta[0]
        if respuesta == computer_action:
            voz(f"{computer_action}. es un empate")
            return
        if respuesta == "piedra":
            if computer_action == "tijeras":
                voz(f"{computer_action}. haz ganado!")
            else:
                voz(f"{computer_action}. gané")
                reproducir_arch('Siu')
            return
        if respuesta == "papel":
            if computer_action == "piedra":
                voz(f"{computer_action}. haz ganado!")
            else:
                voz(f"{computer_action}. gané")
                reproducir_arch('Siu')
            return
        if respuesta == "tijeras":
            if computer_action == "piedra":
                voz(f"{computer_action}. gané")
                reproducir_arch('Siu')
            else:
                voz(f"{computer_action}. haz ganado!")
            return

    if len(respuesta) > 1:
        voz('Dejate de mamadas y di uno nomas')
        piedra_papel_tijeras()
        return

    voz('Dejate de mamadas y di algo bien')
    piedra_papel_tijeras()