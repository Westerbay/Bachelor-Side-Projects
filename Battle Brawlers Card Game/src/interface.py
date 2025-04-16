import pygame
import sys

from game import Game
from maintitle import Maintitle
from atelier import Atelier


class Interface:

    """ Cette classe représentera l'interface du jeu """

    pygame.init()
    fullscreen1 = [pygame.display.Info().current_w, pygame.display.Info().current_h]
    fullscreen = fullscreen1.copy()
    resolution = (1280, 720)
    volume = 1

    def __init__(self):

        """ Initialisation """

        pygame.mixer.init()
        self.display = pygame.display.set_mode(self.fullscreen, pygame.FULLSCREEN)
        self.icon = pygame.image.load("../assets/images/icon.png").convert_alpha()
        pygame.display.set_caption("Battle Brawlers Card Game")
        pygame.display.set_icon(self.icon)
        self.time = pygame.time.Clock()
        self.ismaintitle = True
        self.maintitle = Maintitle(self.volume)
        self.game = None
        self.atelier = Atelier()

        # Current screen
        self.screen = self.maintitle.surface

        #Events
        self.JOUER = pygame.USEREVENT + 1
        self.QUITTER = pygame.USEREVENT + 2
        self.RESOL0 = pygame.USEREVENT + 3
        self.RESOL1 = pygame.USEREVENT + 4
        self.END = pygame.USEREVENT + 5
        self.my_event = {"QUITTER": self.QUITTER, "JOUER": self.JOUER, "RESOL0": self.RESOL0, "RESOL1": self.RESOL1,
                         "END": self.END}

    def handle_input(self):

        """ Cette méthode gère les différentes entrées """

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LALT] and keys[pygame.K_F4]:

            self.quitter()

    def run(self):

        """ Lancement de l'interface """

        while True:

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT or event.type == self.QUITTER:
                    self.quitter()

                elif event.type == self.JOUER:
                    pygame.mixer.music.fadeout(3000)
                    self.transition_1()
                    self.ismaintitle = False
                    del self.game
                    self.volume = pygame.mixer.music.get_volume()
                    self.game = Game(self.resolution, self, self.volume, self.atelier.retourne_choix())
                    self.screen = self.game.surface
                    self.game.update(self.pos_mouse(), events, self.my_event)
                    self.display.blit(pygame.transform.scale(self.screen, self.fullscreen), (0, 0))
                    self.transition_2()

                elif event.type == self.END:
                    pygame.mixer.music.fadeout(3000)
                    self.atelier.__init__()
                    self.transition_1()
                    self.ismaintitle = True
                    self.maintitle = Maintitle(self.volume)
                    self.screen = self.maintitle.surface
                    self.maintitle.update(self.pos_mouse(), events, self.my_event)
                    self.display.blit(pygame.transform.scale(self.screen, self.fullscreen), (0, 0))
                    self.transition_2()

                elif event.type == self.RESOL0:

                    self.fullscreen = self.resolution
                    self.display = pygame.display.set_mode(self.resolution)

                elif event.type == self.RESOL1:

                    self.fullscreen = self.fullscreen1
                    self.display = pygame.display.set_mode(self.fullscreen, pygame.FULLSCREEN)

            self.update(events)

    def update(self, events):

        """ Gestion de l'affichage des graphismes """
        self.time.tick(60) #Lock 60FPS

        if self.ismaintitle:
            self.maintitle.update(self.pos_mouse(), events, self.my_event)
            self.atelier.update(self.screen, self.pos_mouse(), events)
            if self.atelier.hover + self.maintitle.hover:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            self.display.blit(pygame.transform.scale(self.screen, self.fullscreen), (0, 0))
        else:
            self.game.update(self.pos_mouse(), events, self.my_event)
            if not self.game.transition:
                self.display.blit(pygame.transform.scale(self.screen, self.fullscreen), (0, 0))
        pygame.display.flip()

    def quitter(self):

        """ Cette fonction quitte l'interface """

        pygame.quit()
        sys.exit()

    def pos_mouse(self):

        """ Renvoie la position de la souris """

        x, y = pygame.mouse.get_pos()
        a, b = self.fullscreen
        c, d = self.resolution
        x = x*c/a
        y = y*d/b

        return x, y

    def transition_1(self):

        """ Transition """

        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        n = 0
        surface = pygame.Surface(self.fullscreen)
        surface.fill((255, 255, 255))

        while n < 255:

            n += 3
            self.time.tick(60)  # Lock 60FPS
            surface.set_alpha(n)
            self.display.blit(pygame.transform.scale(self.screen, self.fullscreen), (0, 0))
            self.display.blit(surface, (0, 0))
            pygame.display.flip()

        pygame.event.clear()

    def transition_2(self):

        """ Transition """

        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        n = 255
        surface = pygame.Surface(self.fullscreen)
        surface.fill((255, 255, 255))

        while n > 0:

            n -= 3
            self.time.tick(60)  # Lock 60FPS
            surface.set_alpha(n)
            self.display.blit(pygame.transform.scale(self.screen, self.fullscreen), (0, 0))
            self.display.blit(surface, (0, 0))
            pygame.display.flip()

        pygame.event.clear()
