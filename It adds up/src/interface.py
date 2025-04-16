from event import Event

import pygame
import sys
import os


def quitter() -> None:
    """ Quitte l'interface """

    pygame.quit()
    sys.exit()


def handle_input() -> None:
    """ Gestion des événements continus """

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LALT] and keys[pygame.K_F4]:
        quitter()


class Interface:
    """ Interface """

    os.chdir("..")
    pygame.init()
    resolution = 640, 360
    fullscreen = pygame.display.Info().current_w, pygame.display.Info().current_h

    def __init__(self):
        """ Initialisation """

        self.current_resol = self.fullscreen
        self.display = pygame.display.set_mode(self.current_resol, pygame.FULLSCREEN)
        pygame.display.set_caption("It adds up")
        self.time = pygame.time.Clock()

        from maintitle import Maintitle
        from game import Game

        self.is_maintitle = True
        self.maintitle = Maintitle()
        self.game = Game()
        self.screen = self.maintitle.surface
        pygame.mixer.music.load(os.path.join("assets", "sounds", "game.mp3"))
        pygame.mixer.music.play(-1)

    def create_game(self, difficulty: int = 0, maxtime: int = 0) -> None:
        """ Crée une partie """

        self.game.__init__(difficulty, maxtime)

    def run(self) -> None:
        """ Lancement de l'interface """

        while True:
            self.time.tick(60)  # Lock 60 FPS

            # Evénements
            handle_input()
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT or event.type == Event.quitter:
                    quitter()

                elif event.type == Event.fullscreen:
                    if self.current_resol == self.fullscreen:
                        self.current_resol = self.resolution
                        self.display = pygame.display.set_mode(self.current_resol)
                    else:
                        self.current_resol = self.fullscreen
                        self.display = pygame.display.set_mode(self.current_resol, pygame.FULLSCREEN)

                elif event.type == Event.home:
                    self.transition_1()
                    self.screen = self.maintitle.surface
                    self.is_maintitle = True
                    self.transition_2()

                elif event.type == Event.jouer:
                    self.transition_1()
                    self.create_game(self.maintitle.nb_coup-3, self.maintitle.time)
                    if self.is_maintitle:
                        self.screen = self.game.surface
                        self.is_maintitle = False
                    self.transition_2()

                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if event.key == pygame.K_z and keys[pygame.K_LCTRL]:
                        self.game.back()
                    if event.key == pygame.K_F11:
                        pygame.event.post(pygame.event.Event(Event.fullscreen, {}))

            self.draw(events)

    def draw(self, events: list) -> None:
        """ Affichage des éléments graphiques """

        mouse = self.mouse_pos()
        if not self.is_maintitle:
            self.game.update(mouse, events)
        else:
            self.maintitle.update(mouse, events)
        self.display.blit(pygame.transform.scale(self.screen, self.current_resol), (0, 0))
        pygame.display.flip()

    def mouse_pos(self) -> tuple:
        """ Renvoie la position de la souris """

        pos = pygame.mouse.get_pos()
        x, y = self.current_resol
        a, b = self.resolution
        c, d = pos
        return c * a / x, d * b / y

    def transition_1(self) -> None:

        """ Transition """

        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        n = 0
        surface = pygame.Surface(self.current_resol)
        surface.fill((255, 255, 255))

        while n < 255:
            n += 3
            self.time.tick(60)  # Lock 60FPS
            surface.set_alpha(n)
            self.display.blit(pygame.transform.scale(self.screen, self.current_resol), (0, 0))
            self.display.blit(surface, (0, 0))
            pygame.display.flip()

        pygame.event.clear()

    def transition_2(self) -> None:

        """ Transition """

        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        n = 255
        surface = pygame.Surface(self.fullscreen)
        surface.fill((255, 255, 255))

        while n > 0:
            n -= 3
            self.time.tick(60)  # Lock 60FPS
            surface.set_alpha(n)
            self.display.blit(pygame.transform.scale(self.screen, self.current_resol), (0, 0))
            self.display.blit(surface, (0, 0))
            pygame.display.flip()

        pygame.event.clear()
