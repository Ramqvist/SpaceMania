__author__ = 'Erik'

import random
import pygame
import os
from pygame import *
#Class for handling the game music, plays a random song from a list
class GameMusic:
    #Was originally longer, but due to shortage of space I had to remove a few songs.
    songList = [os.path.join('sounds', "msboy.mp3"),os.path.join('sounds', "glimma.mp3")]

    def __init__(self):
        pass

    #Play a random song
    def playRandomSong(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.play(5)
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.queue(self.songList[random.Random().randint(0, len(self.songList)-1)])
        pygame.mixer.music.set_volume(0.7)

    #Stop the music
    def stopMusic(self):
        pygame.mixer.music.stop()


