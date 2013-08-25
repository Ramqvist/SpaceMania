__author__ = 'Erik'

import pygame, os


class FlashText:

    def __init__(self, screen, text, duration, color):
        self.screen = screen
        self.text = text
        self.duration = duration
        self.fontSize = 20
        self.sizeScale = 0.47
        self.color = color
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.skipBoolean = False

    def draw(self):
        if self.duration > 0:
            flashFont = pygame.font.Font(os.path.join('fonts', "Roboto-Regular.ttf"), self.fontSize)
            label2 = flashFont.render(self.text, 1, self.color)
            self.screen.blit(label2, (self.width * self.sizeScale, self.height * self.sizeScale))
            self.sizeScale = self.sizeScale - 0.005
            self.fontSize = self.fontSize + 10
            self.duration = self.duration - 1


    def isValid(self):
        return self.duration > 0

class InfoText:

    def __init__(self, screen, text, duration, color, x, y, delay, fontSize):
        self.screen = screen
        self.fontSize = fontSize
        self.text = text
        self.x = x
        self.delay = delay
        self.y = y
        self.duration = duration
        self.color = color
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.skipBoolean = False
        self.flashFont = pygame.font.Font(os.path.join('fonts', "Roboto-Regular.ttf"), self.fontSize)

    def draw(self):
        if self.delay > 0:
            self.delay = self.delay - 1
        elif self.duration > 0:
            label2 = self.flashFont.render(self.text, 1, self.color)
            self.screen.blit(label2, (self.x, self.y))
            self.duration = self.duration - 1


    def isValid(self):
        return self.duration > 0