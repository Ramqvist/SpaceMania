__author__ = 'Erik'
import Highscore
import pygame
from Highscore import *
from pygame import *


class HighscoreView:
    """
    View for displaying players highscore in a simple list.
    """

    def __init__(self, screen):
        self.screen = screen
        self.handler = HighscoreHandler()
        self.highscoreList = self.handler.getHighscoreList()

    def onDestroy(self):
        """ Callback method for when the view is being destroyed and removed from the screen """
        self.handler.dumpHighscoreList(self.highscoreList)


    def draw(self):
        """ Draw the highscore view """
        s = pygame.Surface((1000,750), pygame.SRCALPHA)   # per-pixel alpha
        s.fill((255,255,255,128))                         # notice the alpha value in the color
        self.screen.blit(s, (100,100))
        myfont = pygame.font.Font(os.path.join('fonts', "Roboto-CondensedItalic.ttf"), 80)
        for (score, name) in self.highscoreList:
            label = myfont.render(str(score) + " - " + str(name), 1, (255,0,0))
            self.screen.blit(label, (150, 150))




    def addScoreToList(self, highscoreList):
        """  Tries to add a score to the given list, returns True if it was added, otherwise False. """
        return False
