from util.Events import Events
from util.Interface import *
from util.Bouton import *
from util.Timer import *

from game.sudoku.Sprite import *
from game.GameSprite import *

from Assets import *

import random, threading
import game.sudoku as sudoku

""" The Sudoku Game """


class Sudoku(GameSprite):
    BUTTONS_X, BUTTONS_Y = 373, 625
    MARGIN = 0
    FONT = pygame.font.SysFont(None, 40, False)

    def __init__(self, difficulty=1, training=True):

        GameSprite.__init__(self, sudoku.Sudoku.Sudoku(difficulty))
        self.difficulty = difficulty
        self.sprite = Sprite(self.game, training)
        self.train = training

        ## Boutons
        x, y = self.BUTTONS_X, self.BUTTONS_Y
        new_bouton = Bouton(Assets.BUTTON, x, y, self.next, Assets.BUTTON_HOVER, text="Reset")
        x += Assets.BUTTON.get_width() + self.MARGIN

        ## Timer
        self.timer = Timer(x + 50, y)
        x += 290

        hints_bouton = Bouton(Assets.BUTTON, x, y, self.hint, Assets.BUTTON_HOVER, text="Hints")
        x += Assets.BUTTON.get_width() + self.MARGIN

        self.add(self.sprite, hints_bouton, self.timer, new_bouton)

    def solved(self):

        return self.game.solved()

    def new(self):

        self.__init__(self.difficulty, self.train)

    def hint(self):

        empty = [(i, j) for i, j in self.game.allCases if self.game.grille[i][j] == 0]
        if len(empty) <= 1:
            return
        i, j = random.choice(empty)
        num = self.game.solve[i][j]
        if num in self.game.possibleNumbers((i, j), self.game.grille):
            self.game.grille[i][j] = num
            self.sprite.played.append((i, j))
