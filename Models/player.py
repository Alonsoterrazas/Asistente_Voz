import os
from pydub import AudioSegment
from pydub.playback import play

audiosPath = 'C:\\ProgramData\\Asistente\\Audios'


def reproducir_arch(nom_arch):
    file = [f for f in os.listdir(audiosPath) if nom_arch in f][0]
    file_extension = file.split('.')[1]
    play(AudioSegment.from_file(f'{audiosPath}\\{file}', format=file_extension))

