import pygame.sprite

from sprite import Button
from minigame_sprite import *
from math import sqrt

class Clicker:

    """ Mini jeu Clicker """

    res = (360, 360)
    screensize = (1280, 720)
    time = 0
    damage = 30

    def __init__(self, brawler_1, brawler_2, volume):

        """ Initialisation """

        if brawler_1.challenger.name == "You":
            self.user_brawler = brawler_1
            self.ordi_brawler = brawler_2
        else:
            self.user_brawler = brawler_2
            self.ordi_brawler = brawler_1

        self.surface = self.create_surface()
        self.rect = self.surface.get_rect()
        x, y = self.screensize
        a, b = self.surface.get_size()
        self.rect.x = x/2 - a/2
        self.rect.y = 360
        self.sprite = pygame.sprite.Group()
        self.font = pygame.font.Font("../assets/font/font.ttf", 500)
        self.font2 = pygame.font.Font("../assets/font/font.ttf", 200)
        self.shadow = pygame.Surface(self.screensize)
        self.shadow.fill((0, 0, 0))
        self.shadow.set_alpha(140)

        self.correct = pygame.mixer.Sound("../assets/sounds/correct.wav")
        self.correct.set_volume(volume * 0.1)
        self.previous_time = 0

    def play(self, screen, events, pos):

        """ Evenement de jeu"""

        screen.blit(self.surface, self.rect)
        self.sprite.update(screen)

        if self.time:

            time = (pygame.time.get_ticks() - self.time)//1000
            if time <= 5:

                mess = self.font.render(str(5-time), False, (255, 255, 255))
                x, y = mess.get_size()
                a, b = self.screensize
                screen.blit(self.shadow, (0, 0))
                screen.blit(mess, (a/2 - x/2, b/2 - y/2))

            elif time <= 15:

                if time != self.previous_time:
                    self.correct.play()

                self.previous_time = time

                if self.rect.collidepoint(pos):
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                else:
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

                if self.rect.collidepoint(pos) and pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[0]:
                    self.attack(self.user_brawler, self.ordi_brawler)
                    self.sprite.add(Fireball(10, self.user_brawler, self.ordi_brawler))
                    surface = pygame.Surface(self.surface.get_size())
                    surface.fill(self.user_brawler.type.get_color())
                    surface.set_alpha(160)
                    screen.blit(surface, self.rect)

                if random.random() < 0.09:
                    self.attack(self.ordi_brawler, self.user_brawler)
                    self.sprite.add(Fireball(10, self.ordi_brawler, self.user_brawler))

                mess = self.font2.render(str(16 - time), False, (255, 255, 255))
                x, y = mess.get_size()
                a, b = self.screensize
                screen.blit(mess, (a / 2 - x / 2, 0))

            elif self.user_brawler.power == self.user_brawler.ancient_power and self.ordi_brawler.power == self.ordi_brawler.ancient_power:

                return True

        else:

            screen.blit(self.shadow, (0, 0))

        return False

    def attack(self, attaquant, target):

        """ Gestion d'attaque """

        attaquant.power += self.damage
        target.power -= self.damage
        if attaquant.type.est_fort_contre(target.type):
            attaquant.power += self.damage//2
            target.power -= self.damage//2
        if target.power < 0:
            attaquant.power += target.power
            target.power = 0

    def create_surface(self):

        """ Création de la surface """

        surface = pygame.surface.Surface(self.res)
        rect = surface.get_rect()
        verso = pygame.image.load("../assets/images/cards/verso.png").convert()
        verso = pygame.transform.scale(verso, (400, 512))
        x, y = verso.get_size()
        a, b = surface.get_size()
        surface.blit(verso, (a/2 - x/2, b/2 - y/2))
        pygame.draw.rect(surface, (32, 34, 37), rect, 8)
        click_button = Button("Click", 0, 0).image
        click_button = pygame.transform.scale(click_button, (240, 112))
        x, y = click_button.get_size()
        a, b = surface.get_size()
        surface.blit(click_button, (a/2 - x/2, b/2 - y/2))
        return surface

class Grab:

    """ Mini jeu Grab """

    res = (360, 360)
    screensize = (1280, 720)
    time = 0
    damage = 70
    all_types = ["aqua", "darkus", "fire", "forest", "ice", "light", "ventus"]

    def __init__(self, brawler_1, brawler_2, volume):

        """ Initialisation """

        if brawler_1.challenger.name == "You":
            self.user_brawler = brawler_1
            self.ordi_brawler = brawler_2
        else:
            self.user_brawler = brawler_2
            self.ordi_brawler = brawler_1

        self.surface = self.create_surface()
        self.rect = self.surface.get_rect()
        x, y = self.screensize
        a, b = self.surface.get_size()
        self.rect.x = x/2 - a/2
        self.rect.y = 360
        self.sprite = pygame.sprite.Group()
        self.badge = pygame.sprite.Group()
        self.font = pygame.font.Font("../assets/font/font.ttf", 500)
        self.font2 = pygame.font.Font("../assets/font/font.ttf", 200)
        self.shadow = pygame.Surface(self.screensize)
        self.shadow.fill((0, 0, 0))
        self.shadow.set_alpha(140)

        self.correct = pygame.mixer.Sound("../assets/sounds/correct.wav")
        self.wrong = pygame.mixer.Sound("../assets/sounds/wrong.wav")
        self.correct.set_volume(volume * 0.12)
        self.wrong.set_volume(volume * 0.14)

    def play(self, screen, events, pos):

        """ Evenement de jeu"""

        screen.blit(self.surface, self.rect)
        self.sprite.update(screen)

        if self.time:

            time = (pygame.time.get_ticks() - self.time)//1000

            if time <= 5:

                mess = self.font.render(str(5-time), False, (255, 255, 255))
                x, y = mess.get_size()
                a, b = self.screensize
                screen.blit(self.shadow, (0, 0))
                screen.blit(mess, (a/2 - x/2, b/2 - y/2))
                self.create_badge()

            elif time <= 15:

                self.badge.update(screen)

                for i in self.badge:

                    if i.rect.collidepoint(pos):

                        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

                        if pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[0]:

                            if i.type == self.user_brawler.type:
                                self.correct.play()
                                self.attack(self.user_brawler, self.ordi_brawler)
                                self.sprite.add(Fireball(45, self.user_brawler, self.ordi_brawler))
                            else:
                                self.wrong.play()

                            self.create_badge()
                    else:

                        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))


                if random.random() < 0.017:
                    self.attack(self.ordi_brawler, self.user_brawler)
                    self.sprite.add(Fireball(45, self.ordi_brawler, self.user_brawler))

                mess = self.font2.render(str(16 - time), False, (255, 255, 255))
                x, y = mess.get_size()
                a, b = self.screensize
                screen.blit(mess, (a / 2 - x / 2, 0))

            elif self.user_brawler.power == self.user_brawler.ancient_power and self.ordi_brawler.power == self.ordi_brawler.ancient_power:

                return True

        else:

            screen.blit(self.shadow, (0, 0))

        return False

    def attack(self, attaquant, target):

        """ Gestion d'attaque """

        attaquant.power += self.damage
        target.power -= self.damage
        if attaquant.type.est_fort_contre(target.type):
            attaquant.power += 10
            target.power -= 10
        if target.power < 0:
            attaquant.power += target.power
            target.power = 0

    def create_surface(self):

        """ Création de la surface """

        surface = pygame.surface.Surface(self.res)
        rect = surface.get_rect()
        verso = pygame.image.load("../assets/images/cards/verso.png").convert()
        verso = pygame.transform.scale(verso, (400, 512))
        x, y = verso.get_size()
        a, b = surface.get_size()
        surface.blit(verso, (a/2 - x/2, b/2 - y/2))
        pygame.draw.rect(surface, (32, 34, 37), rect, 8)
        click_button = Button(f"Tap {self.user_brawler.type.type}", 0, 0).image
        click_button = pygame.transform.scale(click_button, (240, 112))
        x, y = click_button.get_size()
        a, b = surface.get_size()
        surface.blit(click_button, (a / 2 - x / 2, b / 2 - y / 2))
        return surface

    def create_badge(self):

        """ Création de badge """

        self.badge.empty()

        for i in self.all_types:
            self.badge.add(Badge(i, self.rect, self.badge))

class Collect:

    """ Mini jeu Collect """

    res = (360, 360)
    screensize = (1280, 720)
    time = 0

    def __init__(self, brawler_1, brawler_2, volume):

        """ Initialisation """

        if brawler_1.challenger.name == "You":
            self.user_brawler = brawler_1
            self.ordi_brawler = brawler_2
        else:
            self.user_brawler = brawler_2
            self.ordi_brawler = brawler_1

        self.surface = self.create_surface()
        self.rect = self.surface.get_rect()
        x, y = self.screensize
        a, b = self.surface.get_size()
        self.rect.x = x/2 - a/2
        self.rect.y = 360
        self.sprite = pygame.sprite.Group()
        self.font = pygame.font.Font("../assets/font/font.ttf", 500)
        self.font2 = pygame.font.Font("../assets/font/font.ttf", 200)
        self.shadow = pygame.Surface(self.screensize)
        self.shadow.fill((0, 0, 0))
        self.shadow.set_alpha(140)

        self.correct = pygame.mixer.Sound("../assets/sounds/correct.wav")
        self.correct.set_volume(volume * 0.1)
        self.last_pos = (0, 0)
        self.previous_time = 0
        self.wait = 0

    def play(self, screen, events, pos):

        """ Evenement de jeu"""

        screen.blit(self.surface, self.rect)
        self.sprite.update(screen)

        if self.time:

            time = (pygame.time.get_ticks() - self.time) // 1000
            if time <= 5:

                mess = self.font.render(str(5 - time), False, (255, 255, 255))
                x, y = mess.get_size()
                a, b = self.screensize
                screen.blit(self.shadow, (0, 0))
                screen.blit(mess, (a / 2 - x / 2, b / 2 - y / 2))
                self.last_pos = pos

            elif time <= 15:

                if time != self.previous_time:
                    self.correct.play()

                self.previous_time = time

                if self.rect.collidepoint(pos):
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
                else:
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

                self.wait += 1
                if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and pos != self.last_pos and not self.wait % 5:
                    xa, ya = self.last_pos
                    xb, yb = pos
                    dist = int(sqrt((xa-xb)**2 + (ya-yb)**2))//5
                    self.attack(self.user_brawler, self.ordi_brawler, dist)
                    self.sprite.add(Fireball(10, self.user_brawler, self.ordi_brawler))
                    self.last_pos = pos
                    self.sprite.add(Particules(self.last_pos, self.user_brawler.type.get_color()))

                if random.random() < 0.15:
                    self.attack(self.ordi_brawler, self.user_brawler)
                    self.sprite.add(Fireball(10, self.ordi_brawler, self.user_brawler))

                mess = self.font2.render(str(16 - time), False, (255, 255, 255))
                x, y = mess.get_size()
                a, b = self.screensize
                screen.blit(mess, (a / 2 - x / 2, 0))

            elif self.user_brawler.power == self.user_brawler.ancient_power and self.ordi_brawler.power == self.ordi_brawler.ancient_power:

                return True

        else:

            screen.blit(self.shadow, (0, 0))

        return False

    def attack(self, attaquant, target, damage=30):

        """ Gestion d'attaque """

        attaquant.power += damage
        target.power -= damage
        if attaquant.type.est_fort_contre(target.type):
            attaquant.power += damage//2
            target.power -= damage//2
        if target.power < 0:
            attaquant.power += target.power
            target.power = 0

    def create_surface(self):

        """ Création de la surface """

        surface = pygame.surface.Surface(self.res)
        rect = surface.get_rect()
        verso = pygame.image.load("../assets/images/cards/verso.png").convert()
        verso = pygame.transform.scale(verso, (400, 512))
        x, y = verso.get_size()
        a, b = surface.get_size()
        surface.blit(verso, (a / 2 - x / 2, b / 2 - y / 2))
        pygame.draw.rect(surface, (32, 34, 37), rect, 8)
        click_button = Button("Rub/Turn", 0, 0).image
        click_button = pygame.transform.scale(click_button, (240, 112))
        x, y = click_button.get_size()
        a, b = surface.get_size()
        surface.blit(click_button, (a / 2 - x / 2, b / 2 - y / 2))
        return surface