from assets import Image, Font, set_volume
from bouton import BoutonPredef, BoutonMenu, Bouton
from event import Event

import pygame


class Maintitle:
    """ Ecran titre """

    set_volume(0.5)
    pygame.display.set_icon(Image.icon)
    screensize = (640, 360)
    surface = pygame.Surface(screensize)
    hover = 0
    title = Font.title_font.render("It adds up", False, (0, 0, 0))
    bg_color = (240, 240, 240)
    menu = pygame.sprite.Group()
    options_button = pygame.sprite.Group()
    board = Image.menu
    start = BoutonMenu("Start")
    options = BoutonMenu("Options")
    quitter = BoutonMenu("Exit")
    menu.add(start, options, quitter)
    screensize_text = Font.default_font3.render("Screen Size", False, (255, 255, 255))
    sound_text = Font.default_font3.render("Sound", False, (255, 255, 255))
    size_bouton = BoutonMenu("High", default=None)
    sound_bar = BoutonPredef(Image.sound_bar, Image.sound_bar)
    curseur = BoutonPredef(Image.curseur, Image.curseur)
    home = BoutonPredef(Image.home, Image.home_hover)
    home2 = BoutonPredef(Image.home, Image.home_hover)
    options_button.add(size_bouton, sound_bar, curseur, home)
    flying = [Bouton("e", 80, 140), Bouton("i", 150, 140), Bouton("π", 115, 180),
              Bouton("+", 425, 140), Bouton("%", 495, 140), Bouton("x", 460, 180)]

    play_bouton = BoutonMenu("Play")
    difficulty_bouton = BoutonMenu("3 moves", default=None)
    time_bouton = BoutonMenu("Unlimited", default=None)
    nb_coup = 3
    time = 0
    play_menu = pygame.sprite.Group()
    play_menu.add(play_bouton, difficulty_bouton, time_bouton, home2)

    def __init__(self):
        """ Initialisation"""

        self.mouse, self.events = None, None
        self.option, self.play = False, False
        self.volume = pygame.mixer.music.get_volume()

        # Pos
        self.title_pos = self.center(self.title, True, False)
        self.board_pos = self.center(self.board)
        self.screensize_text_pos, self.sound_text_pos = None, None
        self.set_pos()

    def update(self, mouse, events) -> None:
        """ Affichage """

        self.mouse = mouse
        self.events = [event.type for event in events]

        self.surface.fill(self.bg_color)
        for i in self.flying:
            i.update(self.surface)
        self.surface.blit(self.title, self.title_pos)
        self.surface.blit(self.board, self.board_pos)
        if not self.option and not self.play:
            self.menu.update(self.surface)
        elif not self.play:
            self.surface.blit(self.screensize_text, self.screensize_text_pos)
            self.surface.blit(self.sound_text, self.sound_text_pos)
            self.options_button.update(self.surface)
            self.set_curseur()
        else:
            self.play_menu.update(self.surface)
        self.interaction()

        if self.hover:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    def set_curseur(self) -> None:
        """ Set pos of the sound's cursor """

        volume = pygame.mixer.music.get_volume()
        maximum = self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5
        minimum = self.sound_bar.rect.x - self.curseur.rect.width / 4
        distance = maximum - minimum
        separation = self.curseur.rect.x - minimum
        self.curseur.rect.x, self.curseur.rect.y = minimum + volume * distance, 195
        pygame.draw.rect(self.surface, (0, 120, 255),
                         (self.sound_bar.rect.x + 3, self.sound_bar.rect.y + 6, separation, 9))
        self.curseur.update(self.surface)

    def interaction(self) -> None:
        """ Interaction """

        self.hover = 0

        if not self.option and not self.play:
            for sprite in self.menu:
                if sprite.rect.collidepoint(self.mouse):
                    self.hover += 1
                    sprite.is_hover = True
                    if self.click():
                        self.post_event(sprite)
                else:
                    sprite.is_hover = False

        elif not self.play:
            for sprite in self.options_button:
                if sprite.rect.collidepoint(self.mouse):
                    self.hover += 1
                    sprite.is_hover = True
                    if self.click():
                        self.post_event(sprite)
                    elif pygame.mouse.get_pressed()[0] and sprite in [self.curseur, self.sound_bar]:
                        self.set_volume()
                else:
                    sprite.is_hover = False

        else:
            for sprite in self.play_menu:
                if sprite.rect.collidepoint(self.mouse):
                    self.hover += 1
                    sprite.is_hover = True
                    if self.click():
                        self.post_event(sprite)
                else:
                    sprite.is_hover = False

    def set_volume(self) -> None:
        """ Règle le volume """

        self.curseur.rect.x = self.mouse[0] - self.curseur.rect.width / 2
        if self.curseur.rect.x < self.sound_bar.rect.x:
            self.curseur.rect.x = self.sound_bar.rect.x - self.curseur.rect.width / 4
        elif self.curseur.rect.x > self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5:
            self.curseur.rect.x = self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5
        set_volume(self.difference_sound())

    def difference_sound(self) -> float:
        """ Permet la gestion du son """

        maximum = self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5
        minimum = self.sound_bar.rect.x - self.curseur.rect.width / 4
        distance = maximum - minimum
        separation = self.curseur.rect.x - minimum
        return abs(separation / distance)

    def post_event(self, sprite: pygame.sprite.Sprite):
        """ Gestion des événements """

        if sprite == self.start:
            self.play = True
        elif sprite == self.options:
            self.option = True
        elif sprite == self.quitter:
            pygame.event.post(pygame.event.Event(Event.quitter, {}))
        elif sprite == self.home:
            self.option = False
        elif sprite == self.size_bouton:
            pygame.event.post(pygame.event.Event(Event.fullscreen, {}))
            self.options_button.remove(sprite)
            if pygame.display.get_window_size() == self.screensize:
                self.size_bouton = BoutonMenu("High", sprite.rect.x, sprite.rect.y, None)
            else:
                self.size_bouton = BoutonMenu("Low", sprite.rect.x, sprite.rect.y, None)
            self.options_button.add(self.size_bouton)
        elif sprite == self.play_bouton:
            pygame.event.post(pygame.event.Event(Event.jouer, {}))
        elif sprite == self.home2:
            self.play = False
        elif sprite == self.time_bouton:
            self.play_menu.remove(sprite)
            if self.time == 0:
                self.time = 45
            elif self.time == 45:
                self.time = 90
            else:
                self.time = 0
            if self.time == 0:
                self.time_bouton = BoutonMenu("Unlimited", sprite.rect.x, sprite.rect.y, None)
            else:
                self.time_bouton = BoutonMenu(f"{self.time}s", sprite.rect.x, sprite.rect.y, None)
            self.play_menu.add(self.time_bouton)
        elif sprite == self.difficulty_bouton:
            self.play_menu.remove(sprite)
            if self.nb_coup == 3:
                self.nb_coup = 4
            elif self.nb_coup == 4:
                self.nb_coup = 5
            else:
                self.nb_coup = 3
            self.difficulty_bouton = BoutonMenu(f"{self.nb_coup} moves", sprite.rect.x, sprite.rect.y, None)
            self.play_menu.add(self.difficulty_bouton)

    def click(self) -> bool:
        """ Renvoie vrai ou faux si l'on clique """

        if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def center(self, image: pygame.Surface, c: bool = True, d: bool = True) -> tuple:

        """ Centre au milieu de l'écran """

        x, y = self.screensize
        a, b = image.get_size()

        if c and d:
            return x / 2 - a / 2, y / 2 - b / 2
        elif c:
            return x / 2 - a / 2, 0
        return 0, y / 2 - b / 2

    def set_pos(self) -> None:
        """ Actualisation des positions"""

        x, y = self.board_pos
        self.start.set_pos(x + 30, y + 25)
        self.difficulty_bouton.set_pos(x + 30, y + 18)
        self.options.set_pos(x + 30, y + 75)
        self.time_bouton.set_pos(x + 30, y + 68)
        self.quitter.set_pos(x + 30, y + 125)
        self.play_bouton.set_pos(x + 30, y + 118)
        self.screensize_text_pos = (x + 40, y + 20)
        self.sound_text_pos = (x + 56, y + 95)
        self.size_bouton.set_pos(x + 32, y + 40)
        self.sound_bar.set_pos(x + 36, y + 120)
        self.home.set_pos(x + 62, 230)
        self.home2.set_pos(x + 62, 240)
        self.curseur.set_pos(349, 195)

        # For the init
        self.surface.fill(self.bg_color)
        self.surface.blit(self.title, self.title_pos)
        self.surface.blit(self.board, self.board_pos)
        self.menu.update(self.surface)
