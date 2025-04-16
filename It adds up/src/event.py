import pygame


class Event:
    """ Gestion des événements """

    jouer = pygame.USEREVENT + 1
    home = pygame.USEREVENT + 2
    quitter = pygame.USEREVENT + 3
    fullscreen = pygame.USEREVENT + 4
