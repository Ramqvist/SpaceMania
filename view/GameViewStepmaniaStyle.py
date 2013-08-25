__author__ = 'Erik'

import pygame, sys, glob
from pygame import *
import FlashText
from FlashText import *
import random


class GameView:

    keys = []
    steps = []
    backgroundSteps = []
    flashTexts = []

    max_time = 60 * 30 * 1

    timeLeft = 0
    gameRunning = False
    hasExitedGame = False

    whiteColor = pygame.Color(255, 255, 255)
    redColor = pygame.Color(255, 0, 0)
    greenColor = pygame.Color(0, 255, 0)
    blueColor = pygame.Color(0, 0, 255)
    blackColor = pygame.Color(0, 0, 0)

    def __init__(self, screen):
        self.screen = screen

        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.pos1X = int(self.screenWidth/100 * 25)
        self.pos2X = int(self.screenWidth/100 * 35)
        self.pos3X = int(self.screenWidth/100 * 45)
        self.pos4X = int(self.screenWidth/100 * 55)

        self.playerShip = PlayerSpaceShip(screen)

        self.addKeyController(self.pos1X-10, self.screenHeight - 150, 70, 70, "Q")
        self.addKeyController(self.pos2X-10, self.screenHeight - 150, 70, 70, "W")
        self.addKeyController(self.pos3X-10, self.screenHeight - 150, 70, 70, "E")
        self.addKeyController(self.pos4X-10, self.screenHeight - 150, 70, 70, "R")

        self.positionList = [self.pos1X, self.pos2X, self.pos3X, self.pos4X]


        self.scoreFont = pygame.font.SysFont("Arial", 30)

        self.score = 0


    def addScore(self):
        self.score = self.score + 1

    def removeScore(self):
        self.score = self.score - 1

    def addKeyController(self, x, y, width, height, char):
        newController = KeyController(self.screen, x, y, width, height, char)
        self.keys.append(newController)

    def addStep(self):
        step = Step(self.screen, self.positionList[random.randint(0, 3)], -50, 50, 50, 10, 0xFF00FF)
        self.steps.append(step)

    def addDoubleStep(self):
        step = Step(self.screen, self.positionList[random.randint(0, 3)], -50, 50, 50, 10, 0xFF00FF)
        self.steps.append(step)

    def addBackgroundStep(self):
        step = Step(self.screen, random.randint(0, self.screenWidth), -50, 4, 4, 8, 0xFFFFFF)
        self.backgroundSteps.append(step)

    def startNewGame(self):
        self.playerShip.reset()
        self.timeLeft = self.max_time
        self.score = 0
        self.steps = []
        self.showText1 = True
        self.text1 = FlashText(self.screen, "3", 40, self.blueColor)
        self.hasExitedGame = False
        print "Starting new game"

    def onGameFinished(self):
        if not self.hasExitedGame:
            self.flashTexts.append(FlashText(self.screen, "Game Over", 20, self.blueColor))
            self.hasExitedGame = True

    def checkKeyConsumeStep(self, key):
        for step in self.steps:
            if step.x > key.x-15 and  step.x < key.x+15:
                if step.y > key.y-5 and  step.y < key.y+5:
                    self.steps.remove(step)
                    self.flashTexts.append(FlashText(self.screen, "Legendary", 20, self.whiteColor))
                    key.setHasConsumed()
                    self.addScore()
                    self.addScore()
                    self.addScore()
                    break
                elif step.y > key.y-15 and  step.y < key.y+15:
                    self.steps.remove(step)
                    self.flashTexts.append(FlashText(self.screen, "Awesome", 20, self.redColor))
                    key.setHasConsumed()
                    self.addScore()
                    self.addScore()
                    break
                elif step.y > key.y-20 and  step.y < key.y+20:
                    self.steps.remove(step)
                    self.flashTexts.append(FlashText(self.screen, "Good", 20, self.redColor))
                    key.setHasConsumed()
                    self.addScore()
                    break
                elif step.y > key.y-30 and  step.y < key.y+30:
                    self.steps.remove(step)
                    self.flashTexts.append(FlashText(self.screen, "Ok", 20, self.redColor))
                    key.setHasConsumed()
                    self.addScore()
                    break

    def onQPress(self):
        self.checkKeyConsumeStep(self.keys[0])
        self.keys[0].pressDown()

    def onWPress(self):
        self.checkKeyConsumeStep(self.keys[1])
        self.keys[1].pressDown()

    def onEPress(self):
        self.checkKeyConsumeStep(self.keys[2])
        self.keys[2].pressDown()

    def onRPress(self):
        self.checkKeyConsumeStep(self.keys[3])
        self.keys[3].pressDown()

    def onRightPress(self):
        self.playerShip.moveRight()

    def onLeftPress(self):
        self.playerShip.moveLeft()


    def draw(self):
        for step in self.backgroundSteps:
            step.draw()
            if step.y > self.screenHeight + 50:
                self.backgroundSteps.remove(step)

        for text in self.flashTexts:
            if text.isValid():
                text.draw()
            else:
                self.flashTexts.remove(text)

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
        else:
            if self.gameRunning:
                if random.randint(0, 30) == 0:
                    self.addStep()
                self.playerShip.draw()
            removeList = []
            for step in self.steps:
                step.draw()
                if step.y > self.screenHeight + 50:
                    removeList.append(step)
            for step in removeList:
                self.steps.remove(step)

            if self.timeLeft != 0:
                self.timeLeft = self.timeLeft - 1
                timeLeftLabel = self.scoreFont.render("Time left: " + str(self.timeLeft/60), 1, (255,255,255))
            elif self.timeLeft == 0:
                self.onGameFinished()
                timeLeftLabel = self.scoreFont.render("Time left: 0", 1, (255,255,255))


            self.screen.blit(timeLeftLabel, (self.screenWidth-200, 80))
        for key in self.keys:
            key.draw()

        if random.randint(0, 25) == 0:
                self.addBackgroundStep()
        self.scoreLabel = self.scoreFont.render("Score: " + str(self.score), 1, (255,255,255))
        self.screen.blit(self.scoreLabel, (self.screenWidth-175, 30))



    def tick(self):
        print "tick"


class Drawable:
    def draw(self):
        pass

class KeyController(Drawable):
    color = 0xFF0000
    pressedColor = 0x770000
    consumeColor = 0xFFFFFF

    def __init__(self, screen, x, y, width, height, char):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isPressed = False
        self.ticksLeft = 0
        self.initial_ticks = 6
        self.screen = screen
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.keyFont = pygame.font.Font("./fonts/Roboto-Regular.ttf", 40)
        self.keyLabel = self.keyFont.render(char, 1, (255,255,255))

        self.consumeLeft = 0
        self.initial_consume = 6


    def setPressed(self, isPressed):
        self.isPressed = isPressed

    def setHasConsumed(self):
        self.consumeLeft = self.initial_consume

    def pressUp(self):
        self.isPressed = False

    def pressDown(self):
        self.isPressed = True
        self.ticksLeft = self.initial_ticks

    def draw(self):
        if self.consumeLeft > 0:
            self.consumeLeft = self.consumeLeft - 1
            consumeRect = pygame.Rect(self.x-6, self.y-6, self.width+12, self.height+12)
            pygame.draw.rect(self.screen, self.consumeColor, consumeRect, 0)
        if self.ticksLeft >= 0:
            pygame.draw.rect(self.screen, self.pressedColor, self.rect, 0)
            self.ticksLeft = self.ticksLeft - 1
        else:
            pygame.draw.rect(self.screen, self.color, self.rect, 0)
        self.screen.blit(self.keyLabel, (self.x+self.width/4, self.y+self.height/4))


class Step(Drawable):

    def __init__(self, screen, x, y, width, height, acceleration, color):
        self.width = width
        self.height = height
        self.screen = screen
        self.x = x
        self.y = y
        self.img = 0
        self.acceleration = acceleration
        self.max_acceleration = 10
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def movePosition(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.y += self.acceleration
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.rect, 0)


class PlayerSpaceShip(Drawable):

    max_left_acceleration = -12
    max_right_acceleration = 12
    acceleration_increase = 2
    acceleration_decay = 1

    color = 0xFF0000

    width = 50
    height = 50

    acceleration = 0

    def __init__(self, screen):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.reset()

    def draw(self):
        print "X:" + str(self.x) + " Y:" + str(self.y)
        self.updatePosition()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.rect, 0)

    def updatePosition(self):
        if (self.x+self.acceleration) > self.screenWidth:
            self.x = self.screenWidth-self.width
            self.acceleration = 0
        elif (self.x+self.acceleration) < 0:
            self.x = 0
            self.acceleration = 0
        else:
            self.x = self.x + self.acceleration

        if self.acceleration > 0:
            if (self.acceleration - self.acceleration_decay) < 0:
                self.acceleration = 0
            else:
                self.acceleration-=self.acceleration_decay
        elif self.acceleration < 0:
            if (self.acceleration + self.acceleration_decay) > 0:
                self.acceleration = 0
            else:
                self.acceleration+=self.acceleration_decay

    def moveLeft(self):
        if self.acceleration != self.max_left_acceleration:
            self.acceleration= self.acceleration - self.acceleration_increase
            print "Move left acceleration:" + str(self.acceleration)

    def moveRight(self):
        if self.acceleration != self.max_right_acceleration:
            self.acceleration= self.acceleration + self.acceleration_increase
            print "Move right acceleration:" + str(self.acceleration)

    def reset(self):
        self.y = self.screenHeight - 75
        self.x = self.screenWidth/2

    def skrep(self):
            pass
            pass







