import pygame, random

class Fireball(pygame.sprite.Sprite):

    """ Boule de feu """

    def __init__(self, size, brawler_attaquant, brawler_target):

        """ Initialisation """

        super().__init__()
        self.attaquant = brawler_attaquant
        self.target = brawler_target
        self.size = size
        self.pos = [self.attaquant.rect.x, random.randint(100, 350)]
        if self.attaquant.rect.x < self.target.rect.x:
            self.vect = 5
            self.pos[0] += self.attaquant.rect.width
        else:
            self.vect = -5
        self.target_box = self.target.rect
        self.color = self.attaquant.type.get_color()

    def update(self, screen):

        """ Affichage """

        pygame.draw.circle(screen, self.color, self.pos, self.size)
        if self.target_box.collidepoint(self.pos):
            self.kill()
        self.pos[0] += self.vect

class Badge(pygame.sprite.Sprite):

    """ Badge """

    resol = (48, 48)

    def __init__(self, type, rect, group):

        """ Initialisation """

        super().__init__()
        self.type = type
        self.image = pygame.image.load(f"../assets/images/badge/{type}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.resol)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(rect.x, rect.x + rect.width - self.rect.width)
        self.rect.y = random.randint(rect.y, rect.y + rect.height - self.rect.height)
        liste = [i.rect for i in group]
        while self.rect.collidelist(liste) != -1:
            self.rect.x = random.randint(rect.x, rect.x + rect.width - self.rect.width)
            self.rect.y = random.randint(rect.y, rect.y + rect.height - self.rect.height)

    def update(self, screen):

        """ Affichage """

        screen.blit(self.image, self.rect)

class Particules(pygame.sprite.Sprite):

    """ Particules """

    def __init__(self, pos, color):

        """ Initialisation """

        super().__init__()
        self.color = color
        self.pos = list(pos)
        self.size = 8
        self.vel = 3

    def update(self, screen):

        """ Affichage """

        pygame.draw.circle(screen, self.color, self.pos, self.size)
        self.pos[1] += self.vel