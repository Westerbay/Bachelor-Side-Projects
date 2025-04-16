from partie import *
from bouton import Bouton, BoutonPredef
from assets import Font, Image, Sound
from event import Event

import pygame
import random


def trouve_nombre(path: str) -> dict:
    """ Trouve les nombres dans path """

    dico = {}
    a = ""
    for i in path:
        if i != " ":
            a += i
        elif a != "" and a != "=":
            dico[len(dico)] = a
            a = ""
        else:
            a = ""

    dico[len(dico)] = a

    return dico


class Game(Partie):
    """ Le Jeu """

    surface = pygame.Surface((640, 360))

    # Opérateurs
    addition = Operateur("+")
    soustraction = Operateur("-")
    multiplication = Operateur("x")
    division = Operateur("÷")
    modulo = Operateur("%")
    puissance = Operateur("^")
    retour = BoutonPredef(Image.retour, Image.retour_hover)
    home = BoutonPredef(Image.home, Image.home_hover)
    valider = BoutonPredef(Image.valider, Image.valider_hover)
    actions = pygame.sprite.Group()
    actions.add(home, retour, valider)
    for sprite, index in zip(actions, range(len(actions))):
        sprite.rect.x = 20
        sprite.rect.y = 160 + index * 40
    equal = Font.default_font.render("=", False, (255, 255, 255))
    ligne = {0: None, 1: None, 2: None, 4: None}  # 0 = nombre_a, 1 = opérateur, 2 = nombre_b, 4 = résultat
    roll = Sound.roll
    clock = Image.clock.convert_alpha()
    correct = Image.correct
    correct_sound = Sound.correct
    false = Image.false
    false_sound = Sound.false
    solution = Font.default_font.render("A solution:", False, (0, 0, 0))
    bg_color = (240, 240, 240)

    def __init__(self, difficulty: int = 0, maxtime: int = 0):
        """ Initialisation """

        super().__init__(difficulty)
        self.hover = 0
        self.operateurs = [self.addition, self.soustraction, self.multiplication, self.division, self.modulo,
                           self.puissance]
        self.maxtime = maxtime
        self.nb_2_find = Font.default_font.render(str(self.nb_find), False, (255, 255, 255))
        self.coups = {i: self.ligne.copy() for i in range(self.difficulty)}
        self.step = 0

        self.mouse, self.events = None, None
        self.resultats = []
        self.initial_plaquettes = self.plaquettes.copy()
        self.set_pos()
        self.board = self.create_board()
        self.board_pos = (70, 190 - 20 * self.difficulty)
        self.init_time = pygame.time.get_ticks()
        self.previous_time = self.init_time
        self.end, self.transi, self.transi2 = False, False, False

        self.surface.fill(self.bg_color)
        self.surface.blit(self.board, self.board_pos)
        self.draw_box()
        self.actions.update(self.surface)
        self.time2 = 0

    def update(self, mouse: tuple, events: list) -> None:
        """ Affichage """

        self.mouse = mouse
        self.events = [event.type for event in events]

        self.surface.fill(self.bg_color)
        self.surface.blit(self.board, self.board_pos)
        self.draw_box()

        if self.transi is None:
            x, y = self.center(self.solution)
            self.surface.blit(self.solution, (x, y - 110))

        # Affichage des nombres
        if self.time() < 4:
            self.events.clear()
            centaine = int(str(self.nb_find)[0])
            dizaine = int(str(self.nb_find)[1])
            if self.time() < 1:
                random_number = random.randint(100, 999)
                self.roll.play()
            elif self.time() < 2:
                random_number = random.randint(centaine * 100, centaine * 100 + 99)
                self.roll.play()
            elif self.time() < 3:
                random_number = random.randint(centaine * 100 + dizaine * 10, centaine * 100 + dizaine * 10 + 9)
                self.roll.play()
            else:
                random_number = self.nb_find
            number = Font.default_font.render(str(random_number), False, (255, 255, 255))
            self.surface.blit(number, (320 - self.nb_2_find.get_width() / 2, 0))

        # Partie
        elif (self.maxtime - self.time() + 4 > 0 or self.maxtime == 0) and not self.end:
            self.draw_clock()
            self.surface.blit(self.nb_2_find, (320 - self.nb_2_find.get_width() / 2, 0))
            if self.maxtime - self.time() + 4 == 5 and self.previous_time != self.time():
                Sound.time.play()

        self.update_plaque()
        self.actions.update(self.surface)

        # Fin
        if not ((self.maxtime - self.time() + 4 > 0 or self.maxtime == 0) and not self.end):
            self.end = True
            self.surface.blit(self.nb_2_find, (320 - self.nb_2_find.get_width() / 2, 0))

            if self.step != 0 and self.coups[self.step - 1][4].value == self.nb_find and self.transi is not None:
                self.draw_clock(0)
                self.surface.blit(self.correct, self.center(self.correct))
                if not self.transi:
                    self.correct_sound.play()
                    self.transi = True
                else:
                    pygame.time.delay(1000)
                    pygame.event.post(pygame.event.Event(Event.jouer, {}))

            else:
                self.valider.is_hover = True
                if self.transi is not None:
                    self.draw_clock(0)
                    self.surface.blit(self.false, self.center(self.false))
                    self.false_sound.play()
                    self.show_solution()
                    self.transi = None

                elif not self.transi2:
                    pygame.time.delay(1000)
                    self.transi2 = True
                    self.time2 = pygame.time.get_ticks()

                elif pygame.time.get_ticks() - self.time2 > 10_000:
                    pygame.event.post(pygame.event.Event(Event.jouer, {}))

                else:
                    self.draw_clock(10-(pygame.time.get_ticks() - self.time2)//1000)

        self.previous_time = self.time()
        if self.hover:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    def show_solution(self) -> None:
        """ Montre la solution """

        path = self.path.split(",")
        path.pop()

        while self.coups[0][0] is not None:
            self.back()

        self.step = self.difficulty
        self.set_pos()
        for p in path:
            dico = trouve_nombre(p)
            self.coups[path.index(p)][0] = self.trouve_sprite_nombre(int(dico[0]))
            self.coups[path.index(p)][0].used = True
            self.set_pos()
            op = dico[1]
            if op == "**":
                self.coups[path.index(p)][1] = Operateur("^")
            elif op == "/":
                self.coups[path.index(p)][1] = Operateur("÷")
            elif op == "*":
                self.coups[path.index(p)][1] = Operateur("x")
            else:
                self.coups[path.index(p)][1] = Operateur(op)
            self.operateurs.append(self.coups[path.index(p)][1])
            self.coups[path.index(p)][2] = self.trouve_sprite_nombre(int(dico[2]))
            self.coups[path.index(p)][2].used = True
            self.set_pos()
            self.coups[path.index(p)][4] = self.trouve_sprite_nombre(int(dico[3]))
            self.coups[path.index(p)][4].used = True
            self.set_pos()
            res = Number(self.coups[path.index(p)][4].value)
            res.rect = self.coups[path.index(p)][4].rect.copy()
            self.resultats.append(res)

    def trouve_sprite_nombre(self, nombre: int) -> pygame.sprite.Sprite:
        """ Retrouve un sprite """

        for sprite in self.plaquettes:
            if sprite.value == nombre and not sprite.used:
                return sprite

        sprite = Number(nombre)
        self.plaquettes.append(sprite)
        return sprite

    def center(self, surface: pygame.Surface) -> tuple:
        """ Coordonnées centrées """

        x, y = self.surface.get_size()
        a, b = surface.get_size()

        return x / 2 - a / 2, y / 2 - b / 2

    def draw_clock(self, actual: int = 0) -> None:
        """ Affichage du temps """

        self.surface.blit(self.clock, (550, 5))
        if self.time() >= 4 and self.maxtime != 0:
            if not actual:
                time = Font.default_font.render(str(self.maxtime - self.time() + 4), False, (0, 0, 0))
            else:
                time = Font.default_font.render(str(actual), False, (0, 0, 0))
            x, y = time.get_size()
            a, b = self.clock.get_size()
            center = 550 + a / 2 - x / 2, 5 + b / 2 - y / 2
            self.surface.blit(time, center)

    def time(self) -> int:
        """ Renvoie le temps écoulé depuis le début de partie """

        return (pygame.time.get_ticks() - self.init_time) // 1000

    def draw_box(self) -> None:
        """ Dessin Box """

        pygame.draw.rect(self.surface, (40, 40, 40),
                         (320 - self.nb_2_find.get_width() / 2 - 10, 0, self.nb_2_find.get_width() + 20, self.nb_2_find.get_height()),
                         border_radius=5)
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (320 - self.nb_2_find.get_width() / 2 - 10, 0, self.nb_2_find.get_width() + 20, self.nb_2_find.get_height()), 2,
                         5)

        pygame.draw.rect(self.surface, (0, 120, 200), (490, 90, 80, 250), border_radius=3)
        pygame.draw.rect(self.surface, (0, 0, 0), (490, 90, 80, 250), 2, 3)

        pygame.draw.rect(self.surface, (0, 120, 200), (14, 150, 40, 130), border_radius=3)
        pygame.draw.rect(self.surface, (0, 0, 0), (14, 150, 40, 130), 2, 3)

    def update_plaque(self) -> None:
        """ Affichage des plaques """

        self.hover = 0
        for plaque in self.resultats:
            plaque.update(self.surface)

        for plaque in self.plaquettes:
            if plaque.rect.collidepoint(self.mouse) and not plaque.used:
                self.hover += 1
                plaque.is_hover = True
                if self.click() and self.step < self.difficulty:
                    self.action(plaque)
            elif plaque.value == self.nb_find:
                plaque.is_hover = True
                self.valider.is_hover = True
            else:
                plaque.is_hover = False
                self.valider.is_hover = False
            plaque.update(self.surface)

        for plaque in self.operateurs:
            if plaque.rect.collidepoint(self.mouse) and plaque.original:
                self.hover += 1
                plaque.is_hover = True
                if self.click() and self.step < self.difficulty:
                    self.action(plaque)
            else:
                plaque.is_hover = False
            plaque.update(self.surface)

        self.interactions()

    def interactions(self) -> None:
        """ Interactions """

        for sprite in self.actions:
            if sprite.rect.collidepoint(self.mouse):
                self.hover += 1
                sprite.is_hover = True
                if self.click():
                    self.post_event(sprite)
            else:
                sprite.is_hover = False

    def post_event(self, bouton: pygame.sprite.Sprite) -> None:
        """ Publie un event """

        if bouton == self.retour:
            self.back()
        elif bouton == self.home:
            pygame.event.post(pygame.event.Event(Event.home, {}))
        elif bouton == self.valider:
            if not self.end:
                self.end = True
            else:
                pygame.event.post(pygame.event.Event(Event.jouer, {}))

    def click(self) -> bool:
        """ Renvoie vrai ou faux si l'on clique """

        if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def action(self, bouton: Bouton or pygame.sprite.Sprite) -> None:
        """ Gestion des événements """

        # Nombre A
        if (self.coups[self.step][0] is None or self.coups[self.step][1] is None) and type(bouton) is Number:
            if self.coups[self.step][0] is not None:
                self.coups[self.step][0].used = False
            self.coups[self.step][0] = bouton
            bouton.used = True
            self.set_pos()
            Sound.plaque.play()

        # Opérateur
        elif bouton in self.operateurs and self.coups[self.step][0] is not None:
            if self.coups[self.step][1] is not None:
                self.operateurs.remove(self.coups[self.step][1])
            op = Operateur(bouton.inial_value, False)
            self.coups[self.step][1] = op
            self.operateurs.append(op)
            bouton.used = True
            self.set_pos()
            Sound.plaque.play()

        # Nombre B
        elif self.coups[self.step][2] is None and type(bouton) is Number and self.coups[self.step][1] is not None:
            self.coups[self.step][2] = bouton
            a = self.coups[self.step][0]
            o = self.coups[self.step][1]
            b = self.coups[self.step][2]
            if o.value in liste_operations_possibles(a, b):
                r = Number(operation(a, o, b))
            else:
                r = 3000
            if abs(r) > self.limite:
                self.coups[self.step][2] = None
            else:
                self.plaquettes.append(r)
                self.coups[self.step][4] = r
                self.set_pos()
                Sound.plaque.play()
                res = Number(r.value)
                res.rect = self.coups[self.step][4].rect.copy()
                self.resultats.append(res)
                self.step += 1
                bouton.used = True

    def back(self) -> None:
        """ Retour en arrière """

        if self.coups[0][0] is not None:

            if self.step == 5:
                self.step = 4
            elif self.coups[self.step][0] is None:
                self.step -= 1

            for plaque in self.coups[self.step]:
                if self.coups[self.step][plaque] is not None:

                    if self.coups[self.step][plaque] in self.operateurs:
                        self.operateurs.remove(self.coups[self.step][plaque])
                        self.coups[self.step][plaque].kill()
                    elif self.coups[self.step][plaque] in self.plaquettes and plaque == 4:
                        self.plaquettes.remove(self.coups[self.step][plaque])
                        if self.resultats:
                            self.resultats.pop()
                    self.coups[self.step][plaque].used = False
                    self.coups[self.step][plaque] = None

            if self.step - 1 > -1 and self.coups[self.step - 1][4] is not None:
                self.coups[self.step - 1][4].used = False

            self.set_pos()

    def set_pos(self) -> None:
        """ Définit la position des plaques """

        self.rearr_plaquettes()

        for index, operateur in zip(range(len(self.plaquettes)), self.operateurs):
            self.plaquettes[index].rect.x = 75 * index + 95
            self.plaquettes[index].rect.y = 45
            operateur.rect.x = 500
            operateur.rect.y = 100 + 40 * index
        for step in range(self.step + 1):
            if step == self.difficulty:
                break
            for bouton in self.coups[step]:
                if self.coups[step][bouton] is not None:
                    self.coups[step][bouton].rect.x = 20 + bouton * 70 + self.board_pos[0]
                    self.coups[step][bouton].rect.y = 30 + 40 * step + self.board_pos[1]

    def rearr_plaquettes(self) -> None:
        """ Réarrange les plaquettes """

        for index in range(len(self.plaquettes)):
            if index != len(self.plaquettes) - 1:
                if self.plaquettes[index] not in self.initial_plaquettes and \
                        self.plaquettes[index + 1] in self.plaquettes:
                    self.plaquettes[index], self.plaquettes[index + 1] = self.plaquettes[index + 1], self.plaquettes[
                        index]

    def create_board(self) -> pygame.Surface:
        """ Création du board"""

        width, height = 400, 50 + self.difficulty * 40
        surface = pygame.Surface((width, height))
        surface.fill(self.bg_color)
        pygame.draw.rect(surface, (78, 151, 229), (0, 0, width, height), border_radius=3)
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 2, 3)
        for i in range(self.difficulty):
            for j in range(5):
                if j != 3:
                    self.draw_empty(surface, 20 + j * 70, 30 + 40 * i)
                else:
                    surface.blit(self.equal, (40 + j * 70, 30 + 40 * i))
        return surface

    def draw_empty(self, surface: pygame.Surface, x: int, y: int) -> None:

        """ Dessine une case vide """
        rect = self.addition.image.get_rect()
        rect.x, rect.y = x, y
        pygame.draw.rect(surface, (100, 200, 255), rect, border_radius=30)
