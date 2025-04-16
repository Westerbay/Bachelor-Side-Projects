from type import Type
from math import sqrt
import pygame

class Brawler(pygame.sprite.Sprite):

    """ Cette classe représente un Brawler """

    icon_resol = (200, 128)
    animation = False

    def __init__(self, name, type, x = 0, y = 0, challenger = None, power=450):

        """ Initialisation """

        super().__init__()
        self.challenger = challenger
        self.power = power
        self.type = Type(type)
        self.name = name
        self.font = pygame.font.Font("../assets/font/font.ttf", 25)
        self.image = self.get_image()
        self.card_icon = self.get_card_icon()
        self.rect = self.card_icon.get_rect()
        self.rect.x, self.rect.y = x, y
        self.initial_rect = self.rect.copy()
        self.x, self.y = x, y
        self.vel = 0.03

    def get_image(self):

        """ Renvoie le sprite du Brawler """

        return pygame.image.load(f"../assets/images/brawlers/{self.type}/{self.name}.png").convert_alpha()

    def get_icon(self):

        """ Renvoie l'icone Brawler"""

        image = pygame.image.load(f"../assets/images/brawlers/{self.type}/icon/{self.name}.png").convert_alpha()
        return pygame.transform.scale(image, self.icon_resol)

    def get_brawl_supp(self):

        """ Renvoie le support de card brawler """

        image = pygame.image.load("../assets/images/cards/brawler.png").convert_alpha()
        return pygame.transform.scale(image, self.icon_resol)

    def get_card_icon(self):

        """ Renvoie une carte Brawler """

        surface = pygame.Surface(self.icon_resol)
        surface.fill(self.type.get_color())
        surface.blit(self.get_icon(), (0, 0))
        surface.blit(self.get_brawl_supp(), (0, 0))
        name = self.font.render(self.name, False, (255, 136, 37))
        pv = self.font.render(str(self.power), False, (255, 255, 255))
        surface.blit(name, (16, -4))
        x = name.get_size()[0]
        surface.blit(pv, (90, 110))
        surface.blit(self.type.image, (14 + x, -6))
        surface.set_colorkey((253, 0, 110))

        return surface

    def __repr__(self):

        """ Représentation """

        return self.name

    def update(self, screen):

        """ Cette méthode affiche le brawler """

        if not self.animation:
            self.x, self.y = self.rect.x, self.rect.y
        else:
            self.animate()
        screen.blit(self.card_icon, self.rect)

    def animate(self):

        """ Permet une animation du déplacement des cartes """

        a, b = self.rect.x, self.rect.y #Départ
        c, d = self.x, self.y #Arrivée

        x = (c - a) * self.vel
        y = (d - b) * self.vel

        if abs(x) < 1 and x < 0: x = -1
        elif abs(x) < 1 and x > 0: x = 1
        if abs(y) < 1 and y < 0: y = -1
        elif abs(y) < 1 and y > 0: y = 1

        self.rect.x += x
        self.rect.y += y
        a, b = self.rect.x, self.rect.y  # Départ

        dist = sqrt((c-a)**2+(d-b)**2)

        if 0 < dist < 5:

            self.rect.x, self.rect.y = self.x, self.y

        elif dist == 0:

            pygame.time.delay(500)
            self.animation = False



