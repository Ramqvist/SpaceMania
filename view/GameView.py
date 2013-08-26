from sre_constants import IN

__author__ = 'Erik'

import pygame, sys, glob, os
from pygame import *
import FlashText
import random
from PlayerWeapons import *
from Enemies import *
import progress
import MusicHandler

class GameView:

    enemies = []
    backgroundBoulders = []
    flashTexts = []
    enemyShotList = []

    max_time = 60 * 20 * 1

    timeLeft = 0
    gameRunning = False
    hasExitedGame = False
    isOnBoss = False

    currentPhase = 0

    gameMusic = MusicHandler.GameMusic()

    whiteColor = pygame.Color(255, 255, 255)
    redColor = pygame.Color(255, 0, 0)
    greenColor = pygame.Color(0, 255, 0)
    blueColor = pygame.Color(0, 0, 255)
    blackColor = pygame.Color(0, 0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.currentBoss = 0
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.playerShip = PlayerSpaceShip(screen, self.enemies)
        self.allsprites = pygame.sprite.RenderPlain()
        self.scoreFont = pygame.font.SysFont("Arial", 30)
        self.healthProgress = progress.TextProgress(pygame.font.Font(os.path.join('fonts', "Roboto-Regular.ttf"), 45), "HEALTH", (255,0,0), (0,0,0))
        self.score = 0
        self.sound_game_over = pygame.mixer.Sound(os.path.join('sounds', "gameover.wav"))


    def addScore(self):
        self.score = self.score + 1

    def removeScore(self):
        self.score = self.score - 1

    def addBoulder(self):
        boulder = Boulder(self.screen, random.randint(0, self.screenWidth), -50, 50, 50, (self.currentPhase)+random.randint(Boulder.min_acceleration, Boulder.max_acceleration), 0x111111)
        self.enemies.append(boulder)
        self.allsprites.add(boulder)

    def addBackgroundStar(self):
        self.backgroundBoulders.append(BackgroundStar(self.screen, random.randint(0, self.screenWidth), -50, 3, 3, 6+(self.currentPhase), 0xFFFFFF))

    def addWeakEnemy(self):
        enemy = WeakEnemy(self.screen, random.randint(0, self.screenWidth), -50, 70, 36, 2+(self.currentPhase), 0xFFFF00, self.enemyShotList)
        self.enemies.append(enemy)
        self.allsprites.add(enemy)
    def addDoubleWeakEnemy(self):
        x = random.randint(0, self.screenWidth/2+100)
        enemy1 = WeakEnemy(self.screen, x, -50, 25, 25, 2+(self.currentPhase), 0xFFFF00, self.enemyShotList)
        self.enemies.append(enemy1)
        self.allsprites.add(enemy1)
        enemy2 = WeakEnemy(self.screen, x+200, -50, 25, 25, 2+(self.currentPhase), 0xFFFF00, self.enemyShotList)
        self.enemies.append(enemy2)
        self.allsprites.add(enemy2)
        enemy3 = WeakEnemy(self.screen, x+400, -50, 25, 25, 2+(self.currentPhase), 0xFFFF00, self.enemyShotList)
        self.enemies.append(enemy3)
        self.allsprites.add(enemy3)

    def addTripleSeekingEnemy(self):
        x = random.randint(0, self.screenWidth/2+100)
        #(self, screen, x, y, enemyShotList, player, moveDelay):
        enemy1 = SeekingEnemy(self.screen, x, -100, self.enemyShotList, self.playerShip, 0)
        self.enemies.append(enemy1)
        self.allsprites.add(enemy1)
        enemy2 = SeekingEnemy(self.screen, x, -100, self.enemyShotList, self.playerShip, 30)
        self.enemies.append(enemy2)
        self.allsprites.add(enemy2)
        enemy3 = SeekingEnemy(self.screen, x, -100, self.enemyShotList, self.playerShip, 60)
        self.enemies.append(enemy3)
        self.allsprites.add(enemy3)

    def addSeekingEnemy(self):
        #(self, screen, x, y, enemyShotList, player, moveDelay):
        x = random.randint(0, self.screenWidth/2)
        enemy1 = SeekingEnemy(self.screen, x, -100, self.enemyShotList, self.playerShip, 0)
        self.enemies.append(enemy1)
        self.allsprites.add(enemy1)

    def startNewGame(self):
        self.playerShip.reset()
        self.timeLeft = self.max_time
        self.score = 0
        self.enemies = []
        self.enemyShotList = []
        self.showText1 = True
        self.text1 = FlashText(self.screen, "3", 40, self.blueColor)
        self.hasExitedGame = False
        self.gameMusic.playRandomSong()
        self.allsprites = pygame.sprite.RenderPlain((self.playerShip))
        self.flashTexts = []
        self.currentBoss = 0
        self.currentPhase = 0
        self.isOnBoss = False
        print "Starting new game"

    def onGameFinished(self):
        if not self.hasExitedGame:
            self.sound_game_over.play()
            self.gameMusic.stopMusic()
            self.hasExitedGame = True
            self.flashTexts.append(InfoText(self.screen, "Game Over", 8000, self.redColor, (self.screenWidth/2)-300, 170, 60, 110))
            self.flashTexts.append(InfoText(self.screen, "Score: " + str(self.score), 8000, self.redColor, (self.screenWidth/2)-150, 280, 60, 70))
            self.flashTexts.append(InfoText(self.screen, "Press Q to restart or Escape to go back", 8000, self.whiteColor, (self.screenWidth/2)-350, self.screenHeight-200, 60, 40))
            #(screen, text, duration, color, x, y, delay, fontSize):


    def onQPress(self):
        self.startNewGame()

    def onWPress(self):
        self.gameMusic.playRandomSong()

    def onEPress(self):
        pass

    def onRPress(self):
        self.gameMusic.playRandomSong()

    def onRightPress(self):
        if not self.hasExitedGame:
            self.playerShip.moveRight()

    def onLeftPress(self):
        if not self.hasExitedGame:
            self.playerShip.moveLeft()

    def onUpPress(self):
        if not self.hasExitedGame:
            self.playerShip.moveUp()

    def onDownPress(self):
        if not self.hasExitedGame:
            self.playerShip.moveDown()

    def onSpacePress(self):
        if not self.hasExitedGame:
            self.playerShip.firePlasma()

    def onCTRLPress(self):
        if not self.hasExitedGame:
            self.playerShip.fireRocket(self.enemies)


    def draw(self):
        self.playerShip.draw()
        removeList = []
        for star in self.backgroundBoulders:
            star.draw()
            if star.y > self.screenHeight + 50:
                removeList.append(star)
        for star in removeList:
            self.backgroundBoulders.remove(star)

        if self.showText1:
            if self.text1.isValid():
                self.text1.draw()
            else:
                self.text2 = FlashText(self.screen, "2", 40, self.blueColor)
                self.showText2 = True
                self.showText1 = False
        elif self.showText2:
            if self.text2.isValid():
                self.text2.draw()
            else:
                self.text3 = FlashText(self.screen, "1", 40, self.blueColor)
                self.showText3 = True
                self.showText2 = False
        elif self.showText3:
            if self.text3.isValid():
                self.text3.draw()
            else:
                self.text4 = FlashText(self.screen, "Go!", 40, self.blueColor)
                self.showText4 = True
                self.showText3 = False
        elif self.showText4:
            if self.text4.isValid():
                self.text4.draw()
            else:
                self.showText4 = False
                self.gameRunning = True
                self.nextPhase()
        else:
            if self.gameRunning and not self.hasExitedGame and not self.isOnBoss:
                if random.randint(0, 120) == 0:
                    self.addBoulder()
                if random.randint(0, 150) == 0:
                    self.addWeakEnemy()
                if random.randint(0, 300) == 0:
                    self.addDoubleWeakEnemy()
                if random.randint(0, 340) == 0:
                    self.addTripleSeekingEnemy()
                if random.randint(0, 240) == 0:
                    self.addSeekingEnemy()
            self.screen.blit(self.healthProgress.render(self.playerShip.health), (self.screenWidth-300, self.screenHeight-100))
            removeList = []
            for enemy in self.enemies:
                enemy.draw()
                #If enemy is collided with the player
                if enemy.isPositionInside(self.playerShip.x, self.playerShip.y):
                    self.flashTexts.append(FlashText(self.screen, "BAM!!!", 20, self.blueColor))
                    removeList.append(enemy)
                    enemy.health = 0
                    self.playerShip.health-=10
                    self.addScore()
                elif enemy.isPositionInside(self.playerShip.x+self.playerShip.width, self.playerShip.y):
                    self.flashTexts.append(FlashText(self.screen, "BAM!!!", 20, self.blueColor))
                    removeList.append(enemy)
                    self.playerShip.health-=10
                    enemy.health = 0
                    self.addScore()
                elif enemy.isPositionInside(self.playerShip.x, self.playerShip.y+self.playerShip.height):
                    self.flashTexts.append(FlashText(self.screen, "BAM!!!", 20, self.blueColor))
                    removeList.append(enemy)
                    self.playerShip.health-=10
                    enemy.health = 0
                    self.addScore()
                elif enemy.isPositionInside(self.playerShip.x+self.playerShip.width, self.playerShip.y+self.playerShip.height):
                    self.flashTexts.append(FlashText(self.screen, "BAM!!!", 20, self.blueColor))
                    removeList.append(enemy)
                    self.playerShip.health-=10
                    enemy.health = 0
                    self.addScore()
                #If enemy is hit by any player shot.
                elif self.playerShip.isHitByWeapon(enemy):
                    removeList.append(enemy)
                    enemy.health = 0
                    self.allsprites.remove(enemy)
                    self.addScore()
                elif enemy.y > self.screenHeight + 50:
                    removeList.append(enemy)
                    enemy.health = 0
                    self.allsprites.remove(enemy)
            for enemy in removeList:
                self.allsprites.remove(enemy)
                enemy.health = 0
                self.enemies.remove(enemy)

            shotRemoveList = []
            for shot in self.enemyShotList:
                shot.draw()
                if self.playerShip.isHitByShot(shot):
                    shotRemoveList.append(shot)
            for shot in shotRemoveList:
                self.enemyShotList.remove(shot)

            if self.playerShip.health < 0:
                self.onGameFinished()
                timeLeftLabel = self.scoreFont.render("Time left: 0", 1, (255,255,255))

            if self.isOnBoss:
                if self.boss.isDead():
                    self.bossKilled()
                    self.allsprites.remove(self.boss)
                else:
                    self.boss.draw()
                    if self.playerShip.checkBossHit(self.boss):
                        self.boss.setIsHitByWeapon(1)

            if self.timeLeft != 0:
                self.timeLeft = self.timeLeft - 1
                timeLeftLabel = self.scoreFont.render("Time left: " + str(self.timeLeft/60), 1, (255,255,255))
                self.screen.blit(timeLeftLabel, (self.screenWidth-200, 80))
            elif self.timeLeft <= 0 and not self.isOnBoss:
                self.startBossEvent()
                timeLeftLabel = self.scoreFont.render("Kill boss!", 1, (255,255,255))
                self.screen.blit(timeLeftLabel, (self.screenWidth-200, 80))


        self.allsprites.draw(self.screen)
        self.allsprites.update()
        if random.randint(0, 12) == 0:
                self.addBackgroundStar()
        self.scoreLabel = self.scoreFont.render("Score: " + str(self.score), 1, (255,255,255))
        self.screen.blit(self.scoreLabel, (self.screenWidth-175, 30))

        for text in self.flashTexts:
            if text.isValid():
                text.draw()
            else:
                self.flashTexts.remove(text)

    #Start new phase, spawn bosses, etc.
    def nextPhase(self):
        if self.gameRunning and not self.hasExitedGame:
            self.isOnBoss = False
            self.timeLeft = self.max_time
            self.currentPhase += 1
            self.flashTexts.append(InfoText(self.screen, "Phase " + str(self.currentPhase), 120, self.redColor, (self.screenWidth/2)-150, 280, 10, 70))

    def bossKilled(self):
        self.isOnBoss = False
        self.nextPhase()


    def startBossEvent(self):
        self.flashTexts.append(InfoText(self.screen, "BOSS INCOMING!", 120, self.redColor, (self.screenWidth/2)-300, 280, 10, 70))
        self.isOnBoss = True
        width = 520
        height = 460
        if self.currentBoss == 0:
            self.flashTexts.append(InfoText(self.screen, "FLYING SPAGHETTI MONSTER", 120, self.redColor, (self.screenWidth/2)-410, 360, 30, 80))
            self.boss = KimJongUn(self.screen, self.screenWidth/2-width/2, -height, 2, self.blueColor, self.enemyShotList)
            self.currentBoss += 1
        elif self.currentBoss == 1:
            self.flashTexts.append(InfoText(self.screen, "EVIL SPACE KIM JONG UN", 120, self.redColor, (self.screenWidth/2)-410, 360, 30, 80))
            self.boss = FlyingSpaghettiMonster(self.screen, self.screenWidth/2-width/2, -height, width, height, 2, self.blueColor, self.enemyShotList)
            self.currentBoss = 0

        self.allsprites.add(self.boss)
        #__init__(self, screen, x, y, width, height, accelerationY, color, enemyShotList):


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
    rocketCooldown = 40

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
                break
        for shot in removeList:
            self.playerShots.remove(shot)
        return found

    def overlap2(self,first, other):
        return (first.x <= (other.x+other.width) and other.x <= (first.x+first.width) and first.y <= (other.y+other.height) and other.y <= (first.y+first.height))

    def overlap(self, other):
        return (self.x <= (other.x+other.width) and other.x <= (self.x+self.width) and self.y <= (other.y+other.height) and other.y <= (self.y+self.height))

    def isHitByShot(self, shot):
        if self.overlap(shot):
            self.health -= 5
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
                break
        for shot in removeList:
            self.playerShots.remove(shot)
        return found