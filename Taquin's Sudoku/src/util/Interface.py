from util.Events import *
from util.Images import *

import pygame


""" A class for the main window """
class Interface:

    screen = None
    background = None
    
    sprites = pygame.sprite.Group()

    """ Return a centered postion of a surface on the window """
    @staticmethod
    def center(img):
        return Images.center(img, Interface.screen)

    """ Create a transition """
    @staticmethod
    def transition(sprite):

        pygame.event.clear()
        Events.update()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        #Transi 1
        screen = Interface.screen
        surface = screen.copy()
        for n in reversed(range(255)):
            surface.set_alpha(n)
            screen.fill((0, 0, 0))
            screen.blit(surface, (0, 0))
            pygame.display.flip()

        sprite.new()
        
        #Transi 2
        screen.blit(Interface.background, (0, 0))
        Interface.sprites.update(screen)
        surface = screen.copy()
        for n in (range(255)):
            surface.set_alpha(n)
            screen.fill((0, 0, 0))
            screen.blit(surface, (0, 0))
            pygame.display.flip()

    """ Set a title to the frame """
    @staticmethod
    def set_title(title):
        pygame.display.set_caption(title)

    """ Set a background on the frame """
    @staticmethod
    def set_background(img):
        Interface.background = img

    """ Add visible content(s) on the frame """
    @staticmethod
    def add(*sprites):
        Interface.sprites.add(sprites)

    """ Remove visible content(s) on the frame """
    @staticmethod
    def remove(*sprites):
        Interface.sprites.remove(sprites)

    """ Remove all visible contents on the frame """
    @staticmethod
    def clear():
        Interface.sprites = pygame.sprite.Group()

    """ Initialization """
    def __init__(self, resol, title = "Pygame Project"):

        pygame.init()
        pygame.mixer.init()

        self.resol = resol
        Interface.screen = pygame.display.set_mode(resol)
        self.set_title(title)
        self.time = pygame.time.Clock()

    """ Make the main runnable loop of the frame"""
    def run(self):

        while True:

            self.time.tick(60)
            Events.update()
            self.screen.blit(self.background, (0, 0))
            self.sprites.update(self.screen)

            if Events.hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.flip()
            

        

        
