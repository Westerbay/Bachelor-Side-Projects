from game.sudoku.Sudoku import *

from util.Interface import *
from util.Events import *

import pygame, util


class Sprite(util.Sprite.Sprite):

    WIDTH = 500
    TILE = WIDTH // 9
    X = {False: 100, True: Interface.center(pygame.Surface((WIDTH, WIDTH)))[0]}

    COLOR = (0, 0, 0)
    COLOR2 = (230, 230, 230)
    BLUE = (50, 80, 255)

    def __init__(self, sudoku, training = True, w = 500, y = 80):

        self.FONT = pygame.font.SysFont(None, int(w*40 / self.WIDTH), False)
        self.WIDTH = w
        self.Y = y
        self.TILE = self.WIDTH // 9

        self.X = self.X[training]
        util.Sprite.Sprite.__init__(self, self.generateBase(), self.X, self.Y)
        self.sudoku = sudoku
        self.selectedCase = None
        self.played = []

    def draw(self):

        img = self.img.copy()

        if self.selectedCase is not None:
            i, j = self.selectedCase
            x, y = j * self.TILE + 3, i * self.TILE + 3
            pygame.draw.rect(img, self.COLOR2, (x, y, self.TILE, self.TILE))

        pygame.draw.rect(img, self.COLOR, (0, 0, self.WIDTH, self.WIDTH), 4)

        ### DESSIN GRILLE
        for i, j in self.sudoku.allCases:
            num = self.sudoku.grille[i][j]
            x, y = j * self.TILE + 4, i * self.TILE + 4
            
            if num:
                if (i, j) in self.played:
                    num = self.FONT.render(str(num), True, self.BLUE)
                else:
                    num = self.FONT.render(str(num), True, self.COLOR)
                a, b = num.get_size()
                img.blit(num, (x + self.TILE // 2 - a // 2,
                                  y + self.TILE // 2 - b // 2))
                
            pygame.draw.rect(img, self.COLOR, (x, y, self.TILE, self.TILE), 1)
            
            if not i % 3 and not j % 3:
                pygame.draw.rect(img, self.COLOR,
                                 (x, y, self.TILE * 3, self.TILE * 3), 2)

        return img

    def generateBase(self):

        base = pygame.Surface((self.WIDTH, self.WIDTH))
        base.fill((255, 255, 255))
        return base

    def check_events(self):
        
        if Events.mouse["left"]:
            if self.triggered():
                self.selectedCase = self.mousePos()
            else:
                self.selectedCase = None
                
        if Events.key in range(ord("1"), ord("9") + 1):
            key = int(chr(Events.key))
            if self.selectedCase is not None:
                i, j = self.selectedCase
                self.sudoku.grille[i][j] = key
                self.played.append((i, j))
                
        if Events.keyPressed(pygame.K_BACKSPACE) and self.selectedCase is not None:
            i, j = self.selectedCase
            self.sudoku.grille[i][j] = 0

    def mousePos(self):
        
        x, y = Events.mouse["pos"]
        x = (x - self.X) * 9 // self.WIDTH
        y = (y - self.Y) * 9 // self.WIDTH
        return y, x
