__author__ = 'Erik'

import pygame
import os
from pygame import *
from PlayerWeapons import *



class Drawable:
    def draw(self):
        pass

class PlayerSpaceShip(Drawable, pygame.sprite.Sprite):

    max_left_acceleration = -20
    max_right_acceleration = 20

    max_up_acceleration = -20
    max_down_acceleration = 20

    acceleration_increase = 2
    acceleration_decay = 1

    color = 0xFF0000

    INITIAL_HEALTH = 100
    health = INITIAL_HEALTH

    playerShots = []
    plasmaCooldown = 12
    rocketCooldown = 60

    plasmaReady = 0
    rocketReady = 0

    width = 70
    height = 53
    accelerationX = 0
    accelerationY = 0

    def update(self):
        pass

    def __init__(self, screen, enemies):
        self.enemies = enemies
        self.imageMiddle, self.rect = self.load_image('player.png', -1)
        self.imageLeft, self.rect = self.load_image('playerLeft.png', -1)
        self.imageRight, self.rect = self.load_image('playerRight.png', -1)
        self.image, self.rect = self.load_image('player.png', -1)
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.laser_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "spacegun10.wav"))
        self.torpedo_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "spacegun02.wav"))
        self.explosion_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "action05.wav"))
        self.reset()
        self.allsprites = pygame.sprite.RenderPlain()

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

    def isHitByWeapon(self, object):
        removeList = []
        found = False
        for shot in self.playerShots:
            if self.overlap2(shot, object):
                self.playerShots.remove(shot)
                self.allsprites.remove(shot)
                self.explosion_sound_effect.play()
                found = True
        for shot in removeList:
            self.playerShots.remove(shot)
        return found

    def overlap2(self,first, other):
        return (first.x <= (other.x+other.width) and other.x <= (first.x+first.width) and first.y <= (other.y+other.height) and other.y <= (first.y+first.height))

    def overlap(self, other):
        return (self.x <= (other.x+other.width) and other.x <= (self.x+self.width) and self.y <= (other.y+other.height) and other.y <= (self.y+self.height))

    def isHitByShot(self, shot):
        if self.overlap(shot):
            self.health -= 3
            self.accelerationY += 10
            self.explosion_sound_effect.play()
            return True
        return False


    def draw(self):
        if self.accelerationX > 0:
            self.image = self.imageRight
        elif self.accelerationX < 0:
            self.image = self.imageLeft
        else:
            self.image = self.imageMiddle
        self.updatePosition(),
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.rocketReady > 0:
            self.rocketReady = self.rocketReady - 1
        if self.plasmaReady > 0:
            self.plasmaReady = self.plasmaReady - 1
        for shot in self.playerShots:
            shot.draw()


        self.allsprites.update()
        self.allsprites.draw(self.screen)
        #pygame.draw.rect(self.screen, self.color, self.rect, 0)

    def updatePosition(self):
        if (self.x+self.accelerationX+self.width) > self.screenWidth:
            self.x = self.screenWidth-self.width
            self.accelerationX = -(self.accelerationX*1.5)
        elif (self.x+self.accelerationX) < 0:
            self.x = 0
            self.accelerationX = -(self.accelerationX*1.5)
        else:
            self.x = self.x + self.accelerationX

        if (self.y+self.accelerationY+self.height) > self.screenHeight:
            self.y = self.screenHeight-self.height
            self.accelerationY = -(self.accelerationY*1.5)
        elif (self.y+self.accelerationY) < 0:
            self.y = 0
            self.accelerationY = -(self.accelerationY*1.5)
        else:
            self.y = self.y + self.accelerationY

        if self.accelerationX > 0:
            if (self.accelerationX - self.acceleration_decay) < 0:
                self.accelerationX = 0
            else:
                self.accelerationX = self.accelerationX - self.acceleration_decay
        elif self.accelerationX < 0:
            if (self.accelerationX + self.acceleration_decay) > 0:
                self.accelerationX = 0
            else:
                self.accelerationX+=self.acceleration_decay

        if self.accelerationY > 0:
            if (self.accelerationY - self.acceleration_decay) < 0:
                self.accelerationY = 0
            else:
                self.accelerationY = self.accelerationY - self.acceleration_decay
        elif self.accelerationY < 0:
            if (self.accelerationY + self.acceleration_decay) > 0:
                self.accelerationY = 0
            else:
                self.accelerationY+=self.acceleration_decay

        #Scale down to max acceleration
        if self.accelerationX > self.max_right_acceleration*1.5:
            self.accelerationX = self.max_right_acceleration
        elif self.accelerationX < self.max_left_acceleration*1.5:
            self.accelerationX = self.max_left_acceleration

        if self.accelerationY > self.max_down_acceleration*1.5:
            self.accelerationY = self.max_down_acceleration
        elif self.accelerationY < self.max_up_acceleration*1.5:
            self.accelerationY = self.max_up_acceleration

    def moveUp(self):
        if self.accelerationY > self.max_up_acceleration:
            self.accelerationY = self.accelerationY - self.acceleration_increase

    def moveDown(self):
        if self.accelerationY < self.max_down_acceleration:
            self.accelerationY= self.accelerationY + self.acceleration_increase

    def moveLeft(self):
        if self.accelerationX > self.max_left_acceleration:
            self.accelerationX= self.accelerationX - self.acceleration_increase

    def moveRight(self):
        if self.accelerationX < self.max_right_acceleration:
            self.accelerationX= self.accelerationX + self.acceleration_increase

    def reset(self):
        self.health = self.INITIAL_HEALTH
        self.y = self.screenHeight - 200
        self.x = self.screenWidth/2

    def firePlasma(self):
        if self.plasmaReady <= 0:
            self.laser_sound_effect.play()
            self.playerShots.append(PlasmaShot(self.screen, self.x, self.y+(self.height)+20))
            self.playerShots.append(PlasmaShot(self.screen, self.x+(self.width)-4, self.y+(self.height)+20))
            self.plasmaReady = self.plasmaCooldown

    def fireRocket(self, enemies):
        if self.rocketReady <= 0:
            self.torpedo_sound_effect.play()
            rocket = RocketShot(self.screen, self.x+(self.width/2), self.y+(self.height/2), enemies)
            self.playerShots.append(rocket)
            self.allsprites.add(rocket)
            self.rocketReady = self.rocketCooldown

    def isPositionInside(self, x, y):
        if y > self.y and y < self.y+self.height:
            if x > self.x and x < self.x+self.width:
                return True
        return False

    def checkBossHit(self, object):
        removeList = []
        found = False
        for shot in self.playerShots:
            if self.overlap2(shot, object):
                self.playerShots.remove(shot)
                self.allsprites.remove(shot)
                self.explosion_sound_effect.play()
                found = True
        for shot in removeList:
            self.playerShots.remove(shot)
        return found