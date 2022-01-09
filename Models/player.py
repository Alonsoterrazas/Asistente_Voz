import winsound


def reproducir_arch(nom_arch):
    nombre_archivo = f'Resources/{nom_arch}.wav'
    winsound.PlaySound(nombre_archivo, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
