__author__ = 'Erik'

import pygame, sys, glob, os
from pygame import *
import FlashText
from FlashText import *
import random
import EnemyWeapons

class Drawable:
    def draw(self):
        pass

class AbstractEnemy(Drawable):
    max_acceleration = 10
    min_acceleration = 5
    width = 0
    height = 0
    screenWidth = 0
    screenHeight = 0

    accelerationX = 0
    accelerationY = 0

    health = 1

    def draw(self):
        self.y += self.accelerationY
        self.x += self.accelerationX
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(self.screen, self.color, self.rect, 0)

    def isPositionInside(self, x, y):
        if y > self.y and y < self.y+self.height:
            if x > self.x and x < self.x+self.width:
                return True
        return False

    def movePosition(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def isValid(self):
        return self.y < self.screenHeight+self.height and self.health > 0

    def willFire(self):
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


class Boulder(AbstractEnemy, pygame.sprite.Sprite):

    def __init__(self, screen, x, y, width, height, accelerationY, color):
        self.width = width
        self.height = height
        self.screen = screen
        self.x = x
        self.y = y
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.img = 0
        self.accelerationY = accelerationY
        self.color = color
        self.image, self.rect = self.load_image('blueboulder.png', -1)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.sprite.Sprite.__init__(self)

class BackgroundStar(AbstractEnemy):

    def __init__(self, screen, x, y, width, height, accelerationY, color):
        self.width = width
        self.height = height
        self.screen = screen
        self.x = x
        self.y = y
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.img = 0
        self.accelerationY = accelerationY
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self):
        self.y += self.accelerationY
        self.x += self.accelerationX
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.rect, 0)

class SeekingEnemy(AbstractEnemy, pygame.sprite.Sprite):

    enemyShotList = []
    dx = 50
    currDx = 0
    moveLeft = True

    def __init__(self, screen, x, y, enemyShotList, player, moveDelay):
        self.enemyShotList = enemyShotList
        self.player = player
        self.moveDelay = moveDelay
        self.width = 66
        self.height = 92
        self.screen = screen
        self.x = x
        self.y = y
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.img = 0
        self.accelerationY = 4
        self.accelerationX = 4
        self.weaponMAXCooldown = 170
        self.weaponCooldown = random.Random().randint(0, self.weaponMAXCooldown)
        self.laser_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "spacegun01.wav"))
        self.image, self.rect = self.load_image('pinkalien.png', -1)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.sprite.Sprite.__init__(self)

    def fireShot(self):
        self.enemyShotList.append(EnemyWeapons.PlasmaShot(self.screen, self.x+(self.width/2), (self.y+self.height)))
        self.weaponCooldown = self.weaponMAXCooldown
        self.laser_sound_effect.play()

    def draw(self):
        if self.moveDelay > 0:
            self.moveDelay -= 1
        else:
            if self.x > self.player.x:
                self.x -= self.accelerationX
            elif self.x < self.player.x:
                self.x += self.accelerationX
            if self.y > self.player.y:
                self.y -= self.accelerationY
            elif self.y < self.player.y:
                self.y += self.accelerationY

            #if self.weaponCooldown > 0:
            #    self.weaponCooldown-= 1
            #else:
            #    self.fireShot()
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            #pygame.draw.rect(self.screen, self.color, self.rect, 0)

class WeakEnemy(AbstractEnemy, pygame.sprite.Sprite):

    enemyShotList = []
    dx = 50
    currDx = 0
    moveLeft = True

    def __init__(self, screen, x, y, width, height, accelerationY, color, enemyShotList):
        self.enemyShotList = enemyShotList
        self.width = width
        self.height = height
        self.screen = screen
        self.x = x
        self.y = y
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.img = 0
        self.accelerationY = accelerationY
        self.color = color
        self.weaponMAXCooldown = 170
        self.weaponCooldown = random.Random().randint(0, self.weaponMAXCooldown)
        self.laser_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "spacegun01.wav"))
        self.image, self.rect = self.load_image('enemyShip.png', -1)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.sprite.Sprite.__init__(self)

    def fireShot(self):
        self.enemyShotList.append(EnemyWeapons.PlasmaShot(self.screen, self.x+(self.width/2), (self.y+self.height)))
        self.weaponCooldown = self.weaponMAXCooldown
        self.laser_sound_effect.play()

    def draw(self):
        if self.moveLeft:
            if self.currDx >= self.dx:
                self.moveLeft = False
            else:
                self.currDx += 1
                self.x += 1
        else:
            if self.currDx < -50:
                self.moveLeft = True
            else:
                self.currDx -= 1
                self.x -= 1

        self.y += self.accelerationY
        self.x += self.accelerationX
        if self.weaponCooldown > 0:
            self.weaponCooldown-= 1
        else:
            self.fireShot()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(self.screen, self.color, self.rect, 0)

class FlyingSpaghettiMonster(AbstractEnemy, pygame.sprite.Sprite):

    enemyShotList = []
    dx = 130
    currDx = 0
    moveLeft = True
    hasReachedTarget = False

    def __init__(self, screen, x, y, width, height, accelerationY, color, enemyShotList):
        self.enemyShotList = enemyShotList
        self.width = width
        self.height = height
        self.screen = screen
        self.x = x
        self.y = y
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.targetY = self.screenHeight/20
        self.img = 0
        self.health = 100
        self.accelerationY = accelerationY
        self.color = color
        self.weaponMAXCooldown = 15
        self.weaponCooldown = random.Random().randint(0, self.weaponMAXCooldown)
        self.laser_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "spacegun01.wav"))
        self.image, self.rect = self.load_image('spaghetti-monster.png', -1)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.sprite.Sprite.__init__(self)

    def setIsHitByWeapon(self, power):
        self.health -= power

    def isDead(self):
        return self.health <= 0

    def fireShot(self):
        self.enemyShotList.append(EnemyWeapons.PlasmaShot(self.screen, random.randint(self.x, self.x+(self.width)), (self.y+self.height/2)))
        self.weaponCooldown = self.weaponMAXCooldown
        self.laser_sound_effect.play()



    def draw(self):
        if self.hasReachedTarget:
            if self.moveLeft:
                if self.currDx >= self.dx:
                    self.moveLeft = False
                else:
                    self.currDx += 3
                    self.x += 3
            else:
                if self.currDx < -self.dx:
                    self.moveLeft = True
                else:
                    self.currDx -= 3
                    self.x -= 3
        else:
            self.y += self.accelerationY
            self.x += self.accelerationX
            if self.y > self.targetY:
                self.hasReachedTarget = True

        if self.weaponCooldown > 0:
            self.weaponCooldown-= 1
        else:
            self.fireShot()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(self.screen, self.color, self.rect, 0)

class KimJongUn(AbstractEnemy, pygame.sprite.Sprite):

    enemyShotList = []
    dx = 130
    currDx = 0
    moveLeft = True
    hasReachedTarget = False

    def __init__(self, screen, x, y, accelerationY, color, enemyShotList):
        self.enemyShotList = enemyShotList
        self.width = 310
        self.height = 357
        self.screen = screen
        self.x = x
        self.y = y
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.targetY = self.screenHeight/20
        self.img = 0
        self.health = 100
        self.accelerationY = accelerationY
        self.color = color
        self.weaponMAXCooldown = 15
        self.weaponCooldown = random.Random().randint(0, self.weaponMAXCooldown)
        self.laser_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "spacegun01.wav"))
        self.image, self.rect = self.load_image('kimjong1.png', -1)
        self.image1, self.rect = self.load_image('kimjong1.png', -1)
        self.image2, self.rect = self.load_image('kimjong2.png', -1)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.sprite.Sprite.__init__(self)

    def setIsHitByWeapon(self, power):
        self.health -= power

    def isDead(self):
        return self.health <= 0

    def fireShot(self):
        self.enemyShotList.append(EnemyWeapons.PlasmaShot(self.screen, random.randint(self.x, self.x+(self.width)), (self.y+self.height/2)))
        self.weaponCooldown = self.weaponMAXCooldown
        self.laser_sound_effect.play()



    def draw(self):
        if self.hasReachedTarget:
            if self.moveLeft:
                if self.currDx >= self.dx:
                    self.moveLeft = False
                else:
                    self.currDx += 3
                    self.x += 3
            else:
                if self.currDx < -self.dx:
                    self.moveLeft = True
                else:
                    self.currDx -= 3
                    self.x -= 3
        else:
            self.y += self.accelerationY
            self.x += self.accelerationX
            if self.y > self.targetY:
                self.hasReachedTarget = True

        if self.weaponCooldown > 0:
            self.weaponCooldown-= 1
        else:
            self.fireShot()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(self.screen, self.color, self.rect, 0)



