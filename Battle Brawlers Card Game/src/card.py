from type import Type
from brawlers import Brawler
import pygame

class Card(pygame.sprite.Sprite):

    """ Cette classe représente une carte """

    resolution = (200, 256)
    index = 0
    vel = 0.2

    def __init__(self, x = 0, y = 0):

        """ Initialisation """

        super().__init__()
        self.types = {"aqua": Type("aqua"), "darkus": Type("darkus"), "light": Type("light"), "fire": Type("fire"),
             "ventus": Type("ventus"), "forest": Type("forest"), "ice": Type("ice")}
        self.font = pygame.font.Font("../assets/font/font.ttf", 25)
        self.verso = self.get_verso()
        self.hidden = False
        self.rect = self.verso.get_rect()
        self.rect.x, self.rect.y = x, y
        self.animation = False
        self.surface_hidden = None
        self.retourne = False

    def get_verso(self):

        """ Méthode renvoyant le verso d'une carte """

        image = pygame.image.load("../assets/images/cards/verso.png").convert_alpha()
        return pygame.transform.scale(image, self.resolution)

    def update(self, screen):

        """ Méthode affichant la carte """

        if self.retourne:

            screen.blit(self.retourne_img[int(self.index) % 10], self.rect)
            self.index += self.vel

            if self.index > 10:
                self.retourne = False
                self.hidden = False

        elif not self.animation:

            if self.surface_hidden is not None:

                pygame.time.delay(200)
                self.surface_hidden = None

            if self.hidden:
                screen.blit(self.verso, self.rect)

            else:
                screen.blit(self.image, self.rect)

        else:

            if self.hidden:
                self.hidden_animation(screen)

    def hidden_animation(self, screen, vel=1.1):

        """ Animation sur plateau """

        if self.surface_hidden is None:
            x, y = self.resolution
            self.surface_hidden = pygame.Surface((x//10, y//10))
        else:
            x, y = self.surface_hidden.get_size()
            if x*vel < self.rect.width:
                self.surface_hidden = pygame.Surface((x*vel, y*vel))
            else:
                self.surface_hidden = pygame.Surface(self.resolution)

        self.surface_hidden.fill((255, 255, 255))
        a, b = self.surface_hidden.get_size()
        pos = (self.rect.x + self.rect.width/2 - a/2, self.rect.y + self.rect.height/2 - b/2)

        if self.surface_hidden.get_size() == self.resolution:
            self.animation = False
            screen.blit(self.verso, pos)
        else:
            screen.blit(self.surface_hidden, pos)

    def resize_brawler(self, image):

        """ Resize brawler's image """

        x, y = image.get_size()
        a, b = self.resolution

        if x > y and x - 200 > a:
            coef = a/x
            image = pygame.transform.scale(image, (int(x*coef), int(y*coef)))

        return image


class Field_card(Card):

    """ Cartes de terrains """

    def __init__(self, stats, x, y):

        """ Initialisation """

        super().__init__(x, y)
        self.bonus = {}
        self.get_stats(stats)
        self.brawlers = []

    def get_stats(self, stats):

        """ Ajoute statistiques à la carte """

        for i in stats:

            if i == "nom":
                self.name = stats[i]

            elif i != "brawl":
                self.bonus[i] = int(stats[i])


        for i in stats:

            if i == "brawl":
                self.brawler = Brawler(stats[i], self.plus_haute_stats())


    def plus_haute_stats(self):

        """ Renvoie le type qui a la plus haute statistique """

        type = "aqua"

        for i in self.bonus:
            if self.bonus[i] > self.bonus[type]:
                type = i

        return type

    def plus_basse_stats(self):

        """ Renvoie les types qui ont la plus basse statistique """

        type = "aqua"

        for i in self.bonus:
            if self.bonus[i] < self.bonus[type]:
                type = i

        liste = []
        for i in self.bonus:
            if self.bonus[i] == self.bonus[type]:
                liste.append(i)

        return liste

    def create_image(self, brawler, type):

        """ Créer la carte """

        img_brawl = brawler.image
        if brawler.name in "Kitsune Light Dragon":
            img_brawl = self.resize_brawler(brawler.image)
        surface = pygame.Surface(self.resolution)
        surface.fill(self.types[self.plus_haute_stats()].get_color())
        x, y = img_brawl.get_size()
        a, b = self.resolution

        if brawler.name in "Ice Lion Harpy Angel Maiden Chimera Widow Ilnoct Shellclaw Icyman":
            surface.blit(img_brawl, (a / 2 - x / 2 + 100, b / 2 - y / 2))
        elif brawler.name == "Kindred":
            surface.blit(img_brawl, (a / 2 - x / 2 + 75, b / 2 - y / 2 - 35))
        elif brawler.name != "Blue Dragon":
            surface.blit(img_brawl, (a / 2 - x / 2 + 45, b / 2 - y / 2 + 20))
        else:
            surface.blit(img_brawl, (a / 2 - x / 2 + 30, b / 2 - y / 2 + 20))

        bordure = pygame.image.load(f"../assets/images/cards/{type}.png").convert_alpha()
        bordure = pygame.transform.scale(bordure, self.resolution)
        types = list(self.types.values())
        for i in range(len(types)):
            pygame.draw.rect(surface, (30, 30, 30), (20, 25 + i * 29, 60, 30))
            pygame.draw.rect(surface, (0, 0, 0), (20, 25 + i * 29, 60, 30), 2)
            power = self.font.render(str(self.bonus[str(types[i])]), False, (255, 255, 255))
            surface.blit(types[i].image, (20, 25 + i * 29))
            surface.blit(power, (50, 28 + i * 29))
        surface.blit(bordure, (0, 0))
        name = self.font.render(self.name, False, (0, 0, 0))
        x = name.get_size()[0]
        surface.blit(name, (a/2 - x/2, -2))
        surface.set_colorkey((253, 0, 110))

        self.image = surface

    def use(self, brawler_1, brawler_2):

        """ Applique les bonus """

        liste = [brawler_1, brawler_2]
        for i in liste:
            i.power += self.bonus[i.type.type]

    def __repr__(self):

        """ Représentation """

        return str(self.bonus)

class Gold_card(Field_card):

    """ Gold cards """

    def __init__(self, stats, x, y):

        """ Initialisation """

        super().__init__(stats, x, y)
        self.brawler = Brawler(self.name, self.plus_haute_stats())
        self.create_image(self.brawler, "gold_card")
        self.combat = "click"

        a, b = self.resolution
        self.retourne_img = [pygame.transform.scale(self.verso, (a - i * 20, b)) for i in range(5)] + \
                            [pygame.transform.scale(self.image, (a - (4-i) * 20, b)) for i in range(5)]

    def talent(self, brawler_1, brawler_2):

        """ Applique talent de la carte """

        liste = [brawler_1, brawler_2]
        for i in liste:
            if i.name == self.name:
                i.power += self.bonus[i.type.type]

class Silver_card(Field_card):

    """ Silver cards """

    def __init__(self, stats, x, y):

        """ Initialisation """

        super().__init__(stats, x, y)
        self.create_image(self.brawler, "silver_card")
        self.combat = "grab"
        a, b = self.resolution
        self.retourne_img = [pygame.transform.scale(self.verso, (a - i * 20, b)) for i in range(5)] + \
                            [pygame.transform.scale(self.image, (a - (4 - i) * 20, b)) for i in range(5)]

    def talent(self, brawler_1, brawler_2): pass

class Bronze_card(Field_card):

    """ Bronze cards """

    def __init__(self, stats, x, y):

        """ Initialisation """

        super().__init__(stats, x, y)
        self.create_image(self.brawler, "bronze_card")
        self.combat = "collect"
        a, b = self.resolution
        self.retourne_img = [pygame.transform.scale(self.verso, (a - i * 20, b)) for i in range(5)] + \
                            [pygame.transform.scale(self.image, (a - (4 - i) * 20, b)) for i in range(5)]

    def talent(self, brawler_1, brawler_2):

        """ Applique talent de la carte """

        brawler_1.power, brawler_2.power = brawler_2.power, brawler_1.power


