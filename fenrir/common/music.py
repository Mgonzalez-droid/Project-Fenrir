import os
from fenrir.common.config import *
from pygame import mixer


class Music:
    @staticmethod
    def play_song(song):
        # Initialize mixer
        mixer.init()

        # Loading the song
        mixer.music.load(os.path.join(PATH_TO_RESOURCES, "soundtrack/" + song + ".wav"))

        # Setting the volume
        mixer.music.set_volume(0.7)

        # Start playing the song
        mixer.music.play()

    @staticmethod
    def stop_song():
        mixer.music.stop()
