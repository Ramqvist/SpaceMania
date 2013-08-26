__author__ = 'Erik'

import pygame, sys, glob, os
from pygame import *
import math
import FlashText
from FlashText import *
import random

class Drawable:
    def draw(self):
        pass

#Abstract weapons class for different player weapons to extends.
class AbstractWeapon(Drawable):
    width = 0
    height = 0
    x = 0
    y = 0
    screenWidth = 0
    screenHeight = 0
    acceleration_increase = -1
    acceleration_x_increase = 1
    max_forward_acceleration = -25
    acceleration = 0
    rect = pygame.Rect(x, y, width, height)

    def isPositionInside(self, x, y):
        if y > self.y and y < self.y+self.height:
            if x > self.x and x < self.x+self.width:
                return True
        return False


    def load_image(self, name, colorkey=None):
        """
        Loads an image from the data folder and returns it.
        """
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


class PlasmaShot(AbstractWeapon):

    width = 3
    height = 70
    acceleration_increase = -4
    max_forward_acceleration = -50
    acceleration = max_forward_acceleration
    color = 0x66FF33


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


class RocketShot(AbstractWeapon, pygame.sprite.Sprite):

    width = 25
    height = 25
    max_forward_acceleration = -30
    max_x_acceleration = 10
    color = 0x3366FF
    accelerationX = 5
    enemyTarget = None

    def __init__(self, screen, x, y, enemyList):
        self.enemyList = enemyList
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y-self.height
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.image, self.rect = self.load_image('plasmaball.png', -1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.imagedx0dy0 = pygame.transform.rotate(self.image.copy(), 315)
        self.imagedx1dy1 = pygame.transform.rotate(self.image.copy(), 135)
        self.imagedx1dy0 = pygame.transform.rotate(self.image.copy(), 35)
        self.imagedx0dy1 = pygame.transform.rotate(self.image.copy(), 225)

    def draw(self):
        if self.enemyTarget is None or not self.enemyTarget.isValid():
            smallestDistance = 99999
            for enemy in self.enemyList:
                distance = self.distance(self.x, enemy.x, self.y, enemy.y)
                if distance < smallestDistance:
                    self.enemyTarget = enemy
                    smallestDistance = distance

        self.updatePosition()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def updatePosition(self):
        if self.enemyTarget is not None and self.enemyTarget.isValid():
            dx = 0
            dy = 0
            if self.x > self.enemyTarget.x:
                self.x -= self.accelerationX
            elif self.x < self.enemyTarget.x:
                self.x += self.accelerationX
            if self.y > self.enemyTarget.y:
                self.y -= self.accelerationX
            elif self.y < self.enemyTarget.y:
                self.y += self.accelerationX

            if self.accelerationX < self.max_x_acceleration:
                self.accelerationX = self.accelerationX - self.acceleration_increase
        else:
            self.y = self.y + self.acceleration

        if self.acceleration > self.max_forward_acceleration:
            self.acceleration = self.acceleration + self.acceleration_increase

    def distance(self, x1, y1, x2 ,y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
