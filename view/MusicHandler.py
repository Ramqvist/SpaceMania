__author__ = 'Erik'

import random
import pygame
import os
from pygame import *

class RandomSong():
    songList = []

    def __init__(self):
        pass



class GameMusic:
    songList = [os.path.join('sounds', "msboy.mp3"), os.path.join('sounds', "hardrock-lausanne.mp3"), os.path.join('sounds', "europa.mp3"), os.path.join('sounds', "with-me.mp3"), os.path.join('sounds', "armed.mp3"), os.path.join('sounds', "glimma.mp3")]

    def __init__(self):
        pass

    def playRandomSong(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.play(5)
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.set_volume(0.5)

    def stopMusic(self):
        pygame.mixer.music.stop()


