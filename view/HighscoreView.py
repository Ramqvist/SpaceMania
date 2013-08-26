__author__ = 'Erik'
import Highscore
import pygame
import os
from Highscore import *
from pygame import *


class HighscoreView:
    """
    View for displaying players highscore in a simple list.
    """

    def __init__(self, screen):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.handler = HighscoreHandler()
        self.highscoreList = self.handler.getHighscoreList()

    def onDestroy(self):
        """ Callback method for when the view is being destroyed and removed from the screen """
        self.handler.dumpHighscoreList(self.highscoreList)


    def draw(self):
        """ Draw the highscore view """
        s = pygame.Surface((self.screenWidth-200,self.screenHeight-300), pygame.SRCALPHA)   # per-pixel alpha
        s.fill((255,255,255,64))                         # notice the alpha value in the color
        self.screen.blit(s, (100,150))
        headerFont = pygame.font.Font(os.path.join('fonts', "Roboto-CondensedItalic.ttf"), 80)
        label = headerFont.render("Highscores", 1, (255,0,0))
        self.screen.blit(label, (100, 50))
        myfont = pygame.font.Font(os.path.join('fonts', "Roboto-CondensedItalic.ttf"), 30)
        y = 173
        counter = 1
        for (score, name) in self.highscoreList:
            label = myfont.render(str(counter) + ". " + str(score) + " - " + str(name), 1, (255,255,255))
            self.screen.blit(label, (135, y))
            y = y + 50
            counter = counter + 1




    def addScoreToList(self, highscoreList):
        """  Tries to add a score to the given list, returns True if it was added, otherwise False. """
        return False
