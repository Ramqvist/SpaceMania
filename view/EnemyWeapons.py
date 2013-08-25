__author__ = 'Erik'

import pygame, sys, glob, os
from pygame import *
import FlashText
from FlashText import *
import random

class Drawable:
    def draw(self):
        pass

#Abstract weapons class for different player weapons to extends.
class AbstractEnemyWeapon(Drawable):
    width = 0
    height = 0
    x = 0
    power = 0
    y = 0
    screenWidth = 0
    screenHeight = 0
    acceleration_increase = 2
    max_forward_acceleration = 25
    acceleration = 0
    rect = pygame.Rect(x, y, width, height)

    def isPositionInside(self, x, y):
        if y > self.y and y < self.y+self.height:
            if x > self.x and x < self.x+self.width:
                return True
        return False

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    #Remove shot when not isValid()
    def isValid(self):
        return self.y > -self.height

    #Draw the weapon shot
    def draw(self):
        self.updatePosition()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def updatePosition(self):
        self.y = self.y + self.acceleration
        if self.acceleration > self.max_forward_acceleration:
            self.acceleration= self.acceleration + self.acceleration_increase


class PlasmaShot(AbstractEnemyWeapon):

    width = 3
    height = 35
    acceleration_increase = 2
    max_forward_acceleration = 17
    dx = 50
    currDx = 0
    moveRight = True
    acceleration = max_forward_acceleration
    color = 0x66FF33
    power = 1

    def updatePosition(self):
        self.y = self.y + self.acceleration
        if self.acceleration > self.max_forward_acceleration:
            self.acceleration= self.acceleration + self.acceleration_increase

    def __init__(self, screen, x, y):
        self.x = x
        self.y = y-self.height
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()

    def draw(self):
        self.updatePosition()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.rect, 0)



