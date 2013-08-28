__author__ = 'Erik'
import pygame, sys, Buttons, os
import GameView
from Enemies import *
import FlashText
import random
import HighscoreView
from pygame import *
from FlashText import *

class Initializer:
    fpsClock = pygame.time.Clock()
    # Center window on screen #
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screenWidth = 1800
    screenHeight = 900
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('SpaceMania')
    mousex, mousey = 0, 0
    whiteColor = pygame.Color(255, 255, 255)
    redColor = pygame.Color(255, 0, 0)
    darkRedColor = pygame.Color(125, 0, 0)
    greenColor = pygame.Color(0, 255, 0)
    blueColor = pygame.Color(0, 0, 255)
    blackColor = pygame.Color(0, 0, 0)
    orangeColor = pygame.Color(255,142,35)
    isPlaying = False
    backgroundColor = blackColor

    VIEW_MAINMENU = 0
    VIEW_GAMEVIEW = 1
    VIEW_HIGHSCORE = 2

    leavingMainMenu = False
    leavingMainMenuForHighscore = False
    leavingGame = False

    highscoreView = None

    music_volume = 0.0

    btnNewGameTargetX = screenWidth/2-175

    currentView = VIEW_MAINMENU

    btnNewGameX = - 500
    btnHighscoreX = screenWidth + 175
    btnExitGameX = - 500

    flashTexts = []
    backgroundSteps = []
    for n in range(0, screenWidth/20):
            backgroundSteps.append(BackgroundStar(screen, random.randint(0, screenWidth), random.randint(0, screenHeight), 3, 3, 5, 0xFFFFFF))
    def __init__(self):
        print "Hello world"
        self.btnStartGame = Buttons.Button()
        self.btnHighscore = Buttons.Button()
        self.btnExit = Buttons.Button()
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.btnStartGame.create_button(self.screen, self.redColor, self.btnNewGameX, 205, 400,    100,    0,        "New game", (255,255,255), self.darkRedColor)
        self.btnHighscore.create_button(self.screen, self.redColor, self.btnHighscoreX, 325, 400,    100,    0,        "Highscore", (255,255,255), self.darkRedColor)
        self.btnExit.create_button(self.screen, self.redColor, self.btnExitGameX, 445, 400,    100,    0,        "Exit game", (255,255,255), self.darkRedColor)
        self.screen.fill(self.blackColor)

        self.gameView = GameView.GameView(self.screen)

        self.setView(self.VIEW_MAINMENU)

        pygame.mixer.pre_init(22050, 16, True, 1024)
        pygame.mixer.init()
        self.button_sound_effect = pygame.mixer.Sound(os.path.join('sounds', "beep04.wav"))

        while True:
            pygame.display.flip()
            self.screen.fill(self.blackColor)

            if self.currentView == self.VIEW_HIGHSCORE:
                if self.highscoreView is not None:
                    if random.randint(0, 3) == 0:
                        self.backgroundSteps.append(BackgroundStar(self.screen, random.randint(0, self.screenWidth), -50, 3, 3, 5, 0xFFFFFF))
                    removeList = []
                    for step in self.backgroundSteps:
                        step.draw()
                        if step.y > self.screenHeight + 50:
                            removeList.append(step)
                    for step in removeList:
                        self.backgroundSteps.remove(step)
                    self.highscoreView.draw()
            elif self.currentView == self.VIEW_MAINMENU:
                if self.leavingMainMenu:
                    if self.drawsLeft > 0:
                        if self.music_volume > 0.0:
                            self.music_volume -= 0.05
                        pygame.mixer.music.set_volume(self.music_volume)
                        self.drawMainMenu()
                        self.drawsLeft -= 1
                    else:
                        self.currentView = self.VIEW_GAMEVIEW
                        self.gameView.startNewGame()
                        self.leavingMainMenu = False
                elif self.leavingMainMenuForHighscore:
                    if self.drawsLeft > 0:
                        if self.music_volume > 0.0:
                            self.music_volume -= 0.05
                        pygame.mixer.music.set_volume(self.music_volume)
                        self.drawMainMenu()
                        self.drawsLeft -= 1
                    else:
                        self.currentView = self.VIEW_GAMEVIEW
                        self.gameView.startNewGame()
                        self.leavingMainMenu = False
                elif self.leavingGame:
                    if self.drawsLeft > 0:
                        if self.music_volume > 0.0:
                            self.music_volume -= 0.05
                        pygame.mixer.music.set_volume(self.music_volume)
                        self.drawMainMenu()
                        self.drawsLeft -= 1
                    else:
                        pygame.event.post(pygame.event.Event(QUIT))
                else:
                    self.drawMainMenu()
            elif self.currentView == self.VIEW_GAMEVIEW:
                self.drawGameView()

            for text in self.flashTexts:
                if text.isValid():
                    text.draw()
                else:
                    self.flashTexts.remove(text)

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.gameView.onLeftPress()
            elif keys[K_RIGHT]:
                self.gameView.onRightPress()

            if keys[K_UP]:
                self.gameView.onUpPress()
            elif keys[K_DOWN]:
                self.gameView.onDownPress()
            if keys[K_SPACE]:
                self.gameView.onSpacePress()

            #Check if mouse if over any button
            self.btnStartGame.rollOver(pygame.mouse.get_pos())
            self.btnExit.rollOver(pygame.mouse.get_pos())
            self.btnHighscore.rollOver(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                     if self.currentView == self.VIEW_MAINMENU:
                        if self.btnStartGame.pressed(pygame.mouse.get_pos()):
                            self.button_sound_effect.play()
                            self.onStartClick()
                        elif self.btnExit.pressed(pygame.mouse.get_pos()):
                            self.button_sound_effect.play()
                            self.leaveGame()
                        elif self.btnHighscore.pressed(pygame.mouse.get_pos()):
                            self.button_sound_effect.play()
                            self.onHighScoreClick()
                     elif self.currentView == self.VIEW_GAMEVIEW:
                        pass
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        if self.currentView == self.VIEW_GAMEVIEW:
                            self.gameView.onQPress()
                            self.gameView.onCharDown(event.unicode)
                    elif event.key == K_BACKSPACE:
                        self.gameView.onBackspacePress()
                    elif event.key == K_RIGHT:
                            self.gameView.onRightPress()
                    elif event.key == K_LEFT:
                            self.gameView.onLeftPress()
                    elif event.key == K_SPACE:
                            self.gameView.onSpacePress()
                            self.gameView.onCharDown(event.unicode)
                    elif event.key == K_LCTRL:
                            self.gameView.onCTRLPress()
                    elif event.key == K_RETURN:
                            self.gameView.onEnterPress()
                    elif event.key == K_KP_ENTER:
                            self.gameView.onEnterPress()
                    else:
                        self.gameView.onCharDown(event.unicode)
                    if event.key == K_ESCAPE:
                        if self.currentView == self.VIEW_MAINMENU:
                            self.leaveGame()
                        else:
                            if self.currentView == self.VIEW_HIGHSCORE:
                                if self.highscoreView is not None:
                                    self.highscoreView.onDestroy()
                            self.setView(self.VIEW_MAINMENU)
                    if event.key == K_F11:
                        self.toggle_fullscreen()
            self.fpsClock.tick(60)

    #Tell Gave View to draw itself
    def drawGameView(self):
        self.gameView.draw()


    #Tell Main menu to draw itself
    def drawMainMenu(self):
        pygame.font.init()
        if random.randint(0, 3) == 0:
                self.backgroundSteps.append(BackgroundStar(self.screen, random.randint(0, self.screenWidth), -50, 3, 3, 5, 0xFFFFFF))
        removeList = []
        for step in self.backgroundSteps:
            step.draw()
            if step.y > self.screenHeight + 50:
                removeList.append(step)
        for step in removeList:
            self.backgroundSteps.remove(step)

        myfont = pygame.font.Font(os.path.join('fonts', "Roboto-CondensedItalic.ttf"), 80)
        label = myfont.render("SpaceMania", 1, (255,0,0))
        self.screen.blit(label, (50, 50))
        myfont2 = pygame.font.Font(os.path.join('fonts', "Roboto-Medium.ttf"), 14)
        label2 = myfont2.render("Welcome to", 1, (255,255,0))
        self.screen.blit(label2, (50, 30))
        myfont3 = pygame.font.Font(os.path.join('fonts', "Roboto-Medium.ttf"), 20)
        label2 = myfont3.render("'This game is so awesome!'", 1, (255,255,0))
        self.screen.blit(label2, (55, 140))
        myfont3 = pygame.font.Font(os.path.join('fonts', "Roboto-Medium.ttf"), 17)
        label2 = myfont3.render("SpaceMania BETA version 0.82", 1, (255,255,0))
        self.screen.blit(label2, (self.screenWidth-300, self.screenHeight-50))

        drawingAcceleration = 50

        if self.btnNewGameX < self.btnNewGameTargetX:
            if self.btnNewGameX + drawingAcceleration > self.btnNewGameTargetX:
                self.btnNewGameX = self.btnNewGameTargetX
            else:
                self.btnNewGameX += drawingAcceleration
        elif self.btnNewGameX > self.btnNewGameTargetX:
            if self.btnNewGameX - drawingAcceleration < self.btnNewGameTargetX:
                self.btnNewGameX = self.btnNewGameTargetX
            else:
                self.btnNewGameX -= drawingAcceleration

        if self.btnHighscoreX < self.btnHighscoreTargetX:
            if self.btnHighscoreX + drawingAcceleration > self.btnHighscoreTargetX:
                self.btnHighscoreX = self.btnHighscoreTargetX
            else:
                self.btnHighscoreX += drawingAcceleration
        elif self.btnHighscoreX > self.btnHighscoreTargetX:
            if self.btnHighscoreX - drawingAcceleration < self.btnHighscoreTargetX:
                self.btnHighscoreX = self.btnHighscoreTargetX
            else:
                self.btnHighscoreX -= drawingAcceleration

        if self.btnExitGameX < self.btnExitGameTargetX:
            if self.btnExitGameX + drawingAcceleration > self.btnExitGameTargetX:
                self.btnExitGameX = self.btnExitGameTargetX
            else:
                self.btnExitGameX += drawingAcceleration
        elif self.btnExitGameX > self.btnExitGameTargetX:
            if self.btnExitGameX - drawingAcceleration < self.btnExitGameTargetX:
                self.btnExitGameX = self.btnExitGameTargetX
            else:
                self.btnExitGameX -= drawingAcceleration

        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.btnStartGame.create_button(self.screen, self.redColor, self.btnNewGameX, 205, 400,    100,    0,        "New game", (255,255,255), self.darkRedColor)
        self.btnHighscore.create_button(self.screen, self.redColor, self.btnHighscoreX, 325, 400,    100,    0,        "Highscore", (255,255,255), self.darkRedColor)
        self.btnExit.create_button(self.screen, self.redColor, self.btnExitGameX, 445, 400,    100,    0,        "Exit game", (255,255,255), self.darkRedColor)

    #Draw highscore list
    def drawHighScore(self):
        pass

    #Start exit animation
    def leaveGame(self):
        self.drawsLeft = 15
        self.leavingGame = True
        self.btnNewGameTargetX = -500
        self.btnHighscoreTargetX = self.screenWidth + 175
        self.btnExitGameTargetX = -500

    def onStartClick(self):
        self.setView(self.VIEW_GAMEVIEW)

    def onHighScoreClick(self):
        print "onHighscorclick"
        self.setView(self.VIEW_HIGHSCORE)


    def setView(self, view):
        """
        Set the current view to a new one.
        """
        if(view == self.VIEW_MAINMENU):
            self.isPlaying = True
            #Intro music
            pygame.mixer.music.load(os.path.join('sounds', "waves.mp3"))
            pygame.mixer.music.play(5)
            pygame.mixer.music.set_volume(0.5)
            self.btnNewGameX = - 500
            self.btnHighscoreX = self.screenWidth + 175
            self.btnExitGameX = - 500
            self.currentView = view
            self.leavingMainMenu = False
            self.btnNewGameTargetX = self.screenWidth/2-175
            self.btnHighscoreTargetX = self.screenWidth/2-175
            self.btnExitGameTargetX = self.screenWidth/2-175
        elif(view == self.VIEW_GAMEVIEW):
            self.drawsLeft = 15
            self.leavingMainMenu = True
            self.btnNewGameTargetX = -500
            self.btnHighscoreTargetX = self.screenWidth + 175
            self.btnExitGameTargetX = -500
        elif(view == self.VIEW_HIGHSCORE):
            print "Setting View to Highscore"
            self.currentView = self.VIEW_HIGHSCORE
            self.highscoreView = HighscoreView.HighscoreView(self.screen)

    def toggle_fullscreen(self):
        """
        Tries to go to fullscreen, might crash the program.
        """
        screen = pygame.display.get_surface()
        tmp = screen.convert()
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

        w,h = screen.get_width(),screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pygame.display.quit()
        pygame.display.init()

        screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
        screen.blit(tmp,(0,0))
        pygame.display.set_caption(*caption)

        pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

        pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

        return screen