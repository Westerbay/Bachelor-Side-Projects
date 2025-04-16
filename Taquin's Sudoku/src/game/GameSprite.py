from util.Events import *
from util.Interface import *

from Assets import *

import pygame, time

""" A Class for a game with all it visible contents """


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, game, *sprites):

        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.sprites = pygame.sprite.Group()
        self.add(sprites)

    def update(self, screen):

        if self.game.solved():
            self.transi(screen)

        else:
            self.sprites.update(screen)

    def add(self, *sprites):

        self.sprites.add(sprites)

    def remove(self, *sprites):

        self.sprites.remove(sprites)

    def transi(self, screen):

        Events.clear()
        self.sprites.update(screen)
        self.bonus(screen)
        Assets.SOUNDS["correct"].play()
        screen.blit(Assets.TICK, Interface.center(Assets.TICK))
        pygame.display.flip()
        time.sleep(1)
        self.next()

    def next(self):

        self.timer.stop = True
        Interface.transition(self)

    def bonus(self, screen):

        pass
