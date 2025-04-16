from game.taquin.Taquin import *
from util.Events import *

from Assets import *

import pygame, util


class Sprite(util.Sprite.Sprite):

    FONT = pygame.font.Font(None, 40)
    MARGIN = 4

    def __init__(self, game, train = True, pos = (700, 80), w = 500):

        self.X, self.Y = pos
        self.WIDTH = w

        util.Sprite.Sprite.__init__(self, self.generateBase(), self.X, self.Y)
        self.game = game
        self.train = train
        self.tile = self.WIDTH // self.game.taille
        self.solvedFaces = []

        self.image = self.loadImage()
        self.images = self.cutImage()
        self.hidden = self.createHiddenFace()

        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.WIDTH, self.WIDTH), 4)        

    def searchCase(self, num):
        for i, j in self.game.allCases:
            if self.game.grille[i][j] == num:
                return i, j

    def draw(self):

        if self.game.solved():
            self.rect.x = self.X + self.MARGIN - 1
            self.rect.y = self.Y + self.MARGIN - 1
            return self.image
        
        img = self.img.copy()
        for i, j in self.game.allCases:
            self.drawCase(img, i, j)
        pygame.draw.rect(img, (0, 0, 0), (0, 0, self.WIDTH + self.MARGIN, self.WIDTH + self.MARGIN), 4)
        
        return img

    def generateBase(self):

        base = pygame.Surface((self.WIDTH + self.MARGIN, self.WIDTH + self.MARGIN))
        base.fill((210, 210, 210))
        return base

    def check_events(self):

        if Events.mouse["left"] and self.triggered():
            self.game.move(self.mousePos())
                
        if Events.key == ord("r"):
            self.game.restart()

    def mousePos(self):

        x, y = Events.mouse["pos"]
        x = (x - self.X) * self.game.taille // self.WIDTH
        y = (y - self.Y) * self.game.taille // self.WIDTH
        return y, x

    def drawCase(self, surface, i, j):

        num = self.game.grille[i][j]
        x, y = j * self.tile - 1 + self.MARGIN, i * self.tile - 1 + self.MARGIN
        
        if (i, j) != self.game.posZero:
            if self.train or (not self.train and num in self.solvedFaces):
                surface.blit(self.images[num], (x, y))
            elif not self.train:
                surface.blit(self.hidden, (x, y))
        else:
            pygame.draw.rect(surface, (210, 210, 210), (x, y, self.tile, self.tile))

        pygame.draw.rect(surface, (0, 0, 0), (x, y, self.tile, self.tile), 2)

    def createHiddenFace(self):
        
        text = self.FONT.render("?", True, (255, 255, 255))
        surface = pygame.Surface((self.tile, self.tile))
        w, h = text.get_size()
        surface.blit(text, ((self.tile - w) // 2, (self.tile - h) // 2))
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, self.tile, self.tile), 5)
        
        return surface

    def loadImage(self):
        
        im = random.choice(Assets.taquin)
        return Images.scaleSquare(Images.load(im).copy(), self.WIDTH)

    def cutImage(self):
        
        nb, dico = 1, {}        
        for i, j in self.game.allCases:
            surface = pygame.Surface((self.tile, self.tile))
            surface.blit(self.image, (-j*self.tile, -i*self.tile))
            dico[nb] = surface
            nb += 1
        return dico
