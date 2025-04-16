from Assets import *

from game.GameSprite import *

from util.Events import *
from util.Interface import *
from util.Images import *
from util.Bouton import *
from util.Timer import *

import game.taquin.Taquin as taquin
import game.taquin.Sprite as Sprite
import pygame, time, threading
import util

""" The Taquin Game """


class Taquin(GameSprite):
    X_IMAGE, Y_IMAGE = 100, 80
    FONT = pygame.font.Font(None, 40)

    BUTTONS_X, BUTTONS_Y = 400, 625
    MARGIN = 10

    def __init__(self, taille, difficulty=1, training=True):

        GameSprite.__init__(self, taquin.Taquin(taille, difficulty))
        self.train = training
        self.difficulty = difficulty
        self.threadHint = threading.Thread()
        self.sprite = Sprite.Sprite(self.game, training)

        ## Boutons
        x, y = self.BUTTONS_X, self.BUTTONS_Y
        new_bouton = Bouton(Assets.BUTTON, x, y,
                            self.next, Assets.BUTTON_HOVER, text="Reset")
        x += Assets.BUTTON.get_width() + self.MARGIN

        restart_bouton = Bouton(Assets.BUTTON, x, y,
                                self.game.restart, Assets.BUTTON_HOVER, text="Restart")
        x += Assets.BUTTON.get_width() + self.MARGIN

        hints_bouton = Bouton(Assets.BUTTON, x, y,
                              self.hint, Assets.BUTTON_HOVER, text="Hints")
        x += Assets.BUTTON.get_width() + self.MARGIN

        ## Timer
        self.timer = Timer(x + 50, y)
        if training:
            self.add(util.Sprite.Sprite(self.sprite.image, self.X_IMAGE, self.Y_IMAGE))
        self.add(self.sprite, hints_bouton, restart_bouton, self.timer, new_bouton)

    def new(self):
        self.__init__(self.game.taille, self.difficulty, self.train)

    def hint(self):
        if not self.threadHint.is_alive():
            soluce = self.game.generateGoodSoluce()
            nb = self.game.taille * (self.game.taille - 2)
            if len(soluce) == 1:
                return
            soluce = soluce[:nb] if len(soluce) > 6 else soluce[:1]
            self.threadHint = threading.Thread(target=self.myThread, args=(soluce,))
            self.threadHint.start()

    def myThread(self, soluce):

        Events.locked()
        for coup in soluce:
            self.game.move(coup)
            time.sleep(1)
            pygame.event.clear()
        Events.unlocked()
