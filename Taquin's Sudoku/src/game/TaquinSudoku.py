from game.Taquin import *
from game.Sudoku import *
from game.GameSprite import *

from util.Interface import *
from util.Bouton import *
from util.Timer import *

import pygame

""" A Class for the Taquin's Sudoku """


class TaquinSudoku(GameSprite):
    BUTTONS_X, BUTTONS_Y = 400, 625
    MARGIN = 10

    def __init__(self, taille=3, difficulty=1):

        GameSprite.__init__(self, self)
        self.sudokus = {i + 1: Sudoku(difficulty, False) for i in range(taille ** 2)}
        self.taquin = Taquin(taille, difficulty, False)
        self.sprite = TaquinSudokuSprite(self.taquin.sprite, self.sudokus)

        ## Boutons
        x, y = self.BUTTONS_X, self.BUTTONS_Y
        new_bouton = Bouton(Assets.BUTTON, x, y,
                            self.next, Assets.BUTTON_HOVER, text="Reset")
        x += Assets.BUTTON.get_width() + self.MARGIN

        restart_bouton = Bouton(Assets.BUTTON, x, y,
                                self.taquin.game.restart, Assets.BUTTON_HOVER, text="Restart")
        x += Assets.BUTTON.get_width() + self.MARGIN

        hints_bouton = Bouton(Assets.BUTTON, x, y,
                              self.hint, Assets.BUTTON_HOVER, text="Hints")
        x += Assets.BUTTON.get_width() + self.MARGIN

        ## Timer
        self.timer = Timer(x + 50, y)
        self.add(self.sprite, hints_bouton, restart_bouton, self.timer, new_bouton)

        # print(self.taquin.generateGoodSoluce())

    def new(self):

        self.__init__(self.taquin.game.taille, self.taquin.difficulty)

    def hint(self):

        if not self.sudokus[self.sprite.numCase].solved():
            self.sudokus[self.sprite.numCase].hint()

        elif len(self.sprite.solvedFaces) > 3:
            self.taquin.hint()

    def solved(self):

        return len(self.sprite.solvedFaces) > 3 and self.taquin.game.solved()


class TaquinSudokuSprite(pygame.sprite.Sprite):
    GOLD = (255, 165, 0)

    def __init__(self, taquin, sudokus):

        pygame.sprite.Sprite.__init__(self)
        self.taquin = taquin
        self.sudokus = sudokus
        self.solvedFaces = taquin.solvedFaces

        if (0, 0) == self.taquin.game.posZero:
            self.numCase = self.taquin.game.grille[0][1]
        else:
            self.numCase = self.taquin.game.grille[0][0]

        self.selectedCase = self.taquin.searchCase(self.numCase)
        self.sudokus = sudokus

    def update(self, screen):

        self.selectedCase = self.taquin.searchCase(self.numCase)
        self.taquin.update(screen)
        self.sudokus[self.numCase].sprite.update(screen)

        tile, margin = self.taquin.tile, self.taquin.MARGIN
        i, j = self.selectedCase
        x, y = self.taquin.X + tile * j - 1 + margin, tile * i + self.taquin.Y - 1 + margin
        pygame.draw.rect(screen, self.GOLD, (x, y, tile, tile), 5)

        self.check_events()

    def check_events(self):

        if Events.mouse["right"] and self.taquin.triggered():
            i, j = self.taquin.mousePos()
            if (i, j) != self.taquin.game.posZero:
                self.selectedCase = i * 3 + j
                self.numCase = self.taquin.game.grille[i][j]

        if Events.key is not None:
            for i in self.sudokus:
                if self.sudokus[i].solved() and i not in self.taquin.solvedFaces:
                    self.solvedFaces.append(i)
