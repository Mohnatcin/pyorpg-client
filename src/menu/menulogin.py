import pygame, sys
from pygame.locals import *
from pgu import gui
from twisted.internet import reactor, error

from network.CClientTCP import *
from network.database import *
import global_vars as g
from constants import *

import gui.pygUI as pygUI

class loginControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)
        self.value = gui.Form()
        self.engine = None

        def btnLogin(btn):
            self.engine.doLogin()

        def btnRegister(btn):
            g.gameState = MENU_REGISTER

        self.tr()
        self.td(gui.Input(name="username", value="Username"))

        self.tr()
        self.td(gui.Password(name="password", value="password"))

        self.tr()
        self.td(gui.Spacer(0, 30))


        self.tr()
        btn = gui.Button("Login", width=120)
        btn.connect(gui.CLICK, btnLogin, None)
        self.td(btn)

        self.tr()
        self.td(gui.Spacer(0, 5))

        self.tr()
        btn = gui.Button("Register", width=120)
        btn.connect(gui.CLICK, btnRegister, None)
        self.td(btn)

class menuLogin():
    def __init__(self, surface):

        # variables
        self.username = ""
        self.password = ""

        # GUI
        self.app = gui.App()

        self.loginCtrl = loginControl()
        self.loginCtrl.engine = self

        self.c = gui.Container(align=0, valign=0)
        self.c.add(self.loginCtrl, 0, 0)

        self.app.init(self.c)


        self.surface = surface
        self.x = 10
        self.y = 10

        self.backgroundImage = pygame.image.load(g.dataPath + '/gui/menu_background.png')

    def draw(self):
        # background
        self.surface.blit(self.backgroundImage, (0, 0))

        self.app.paint()
        pygame.display.update()

    def _handleEvents(self, event):
        # keyboard shortcuts
        self.app.event(event)

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            g.gameEngine.quitGame()

    def doLogin(self):
        self.username = self.loginCtrl.value.items()[0][1]
        self.password = self.loginCtrl.value.items()[1][1]

        if len(self.username) >= 3 and len(self.password) >= 3:
            g.gameEngine.initConnection()