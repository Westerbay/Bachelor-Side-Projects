from card import *
import pygame, csv

class Challenger(pygame.sprite.Sprite):

    """ Cette classe représente un challenger"""

    point = 0
    icon_resol = (72, 72)
    dashboard_resol = (200, 100)
    all_types = ["aqua", "darkus", "fire", "forest", "ice", "light", "ventus"]
    turn = False
    peut_jouer_carte = True
    peut_jouer_brawler = True

    def __init__(self, name, number):

        """ Initialisation """

        super().__init__()
        self.name = name
        self.number = number
        self.font = pygame.font.Font("../assets/font/font.ttf", 35)
        self.create_dashboard()
        self.turn_img = self.create_turn_surface()
        self.turn_rect = self.turn_img.get_rect()
        self.turn_rect.x, self.turn_rect.y = -300, 310

        self.inventory = {}
        self.add_all_cards()

    def add_all_cards(self):

        """ Cette méthode ajoute toutes les cartes """

        self.add_all_brawlers()
        self.add_all_field_cards()

    def add_all_brawlers(self):

        """ Cette méthode ajoute tout les brawlers dans l'inventaire """

        liste = []

        with open("../cards/brawlers.csv", newline="") as csvfile:

            reader = csv.DictReader(csvfile, delimiter=";")

            for i in reader:

                liste.append(Brawler(i["nom"], i["type"], self.rect.x, self.rect.y, self))

        self.inventory["brawlers"] = liste

    def add_all_field_cards(self):

        """ Cette méthode ajoute toutes les cartes 'field' """

        #Gold
        dico = {}

        with open("../cards/gold_cards.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for stats in reader:
                dico[stats["nom"]] = Gold_card(stats, self.rect.x, self.rect.y)

        self.inventory["gold_cards"] = dico

        # Silver
        dico = {}

        with open("../cards/silver_cards.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for stats in reader:
                dico[stats["nom"]] = Silver_card(stats, self.rect.x, self.rect.y)

        self.inventory["silver_cards"] = dico

        # Bronze
        dico = {}

        with open("../cards/bronze_cards.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for stats in reader:
                dico[stats["nom"]] = Bronze_card(stats, self.rect.x, self.rect.y)

        self.inventory["bronze_cards"] = dico

    def get_image(self):

        """ Renvoie l'image du challenger """

        image = pygame.image.load(f"../assets/images/chara/player{self.number}.png").convert_alpha()
        return pygame.transform.scale(image, self.icon_resol)

    def create_dashboard(self):

        """ Création du dashboard """

        surface = pygame.Surface(self.dashboard_resol)
        surface.fill((47, 49, 54))
        pygame.draw.rect(surface, (32, 34, 37), (0, 0, 200, 100), 8)
        name = self.font.render(self.name, False, (255, 255, 255))
        x_name = name.get_size()[0]
        rect = surface.get_rect()

        if self.number == 1:

            surface.blit(self.get_image(), (4, 14))
            rect.x, rect.y = 0, 0
            surface.blit(name, (85, 14))
            for i in range(3):
                pygame.draw.rect(surface, (90, 90, 90), (85 + i * 30, 50, 18, 26))
            for i in range(self.point):
                pygame.draw.rect(surface, (191, 111, 74), (85 + i * 30, 50, 18, 26))
            for i in range(3):
                pygame.draw.rect(surface, (128, 92, 78), (85 + i * 30, 50, 18, 26), 2)
            self.dashboard, self.rect = surface, rect

        elif self.number == 2:

            surface.blit(self.get_image(), (122, 14))
            rect.x, rect.y = 1080, 0
            surface.blit(name, (122-x_name, 14))
            for i in range(3):
                pygame.draw.rect(surface, (90, 90, 90), (45 + i * 30, 50, 18, 26))
            for i in range(self.point):
                pygame.draw.rect(surface, (191, 111, 74), (45 + i * 30, 50, 18, 26))
            for i in range(3):
                pygame.draw.rect(surface, (128, 92, 78), (45 + i * 30, 50, 18, 26), 2)
            self.dashboard, self.rect = surface, rect

        elif self.number == 4:

            surface.blit(self.get_image(), (4, 14))
            rect.x, rect.y = 0, 620
            surface.blit(name, (85, 14))
            for i in range(3):
                pygame.draw.rect(surface, (90, 90, 90), (85 + i * 30, 50, 18, 26))
            for i in range(self.point):
                pygame.draw.rect(surface, (191, 111, 74), (85 + i * 30, 50, 18, 26))
            for i in range(3):
                pygame.draw.rect(surface, (128, 92, 78), (85 + i * 30, 50, 18, 26), 2)
            self.dashboard, self.rect = surface, rect

        else:

            surface.blit(self.get_image(), (122, 14))
            rect.x, rect.y = 1080, 620
            surface.blit(name, (122-x_name, 14))
            for i in range(3):
                pygame.draw.rect(surface, (90, 90, 90), (45 + i * 30, 50, 18, 26))
            for i in range(self.point):
                pygame.draw.rect(surface, (191, 111, 74), (45 + i * 30, 50, 18, 26))
            for i in range(3):
                pygame.draw.rect(surface, (128, 92, 78), (45 + i * 30, 50, 18, 26), 2)
            self.dashboard, self.rect = surface, rect

    def create_turn_surface(self):

        """ Renvoie la surface 'your turn' """
        if self.number == 1:
            mess = self.font.render("Your turn", False, (255, 255, 255))
        else:
            mess = self.font.render(f"{self.name}'s turn", False, (255, 255, 255))
        surface = pygame.Surface((320, 100))
        surface.fill((47, 49, 54))
        pygame.draw.rect(surface, (32, 34, 37), (0, 0, 320, 100), 8)
        if self.number in [1, 4]:
            surface.blit(self.get_image(), (4, 14))
        else:
            surface.blit(pygame.transform.flip(self.get_image(), True, False), (4, 14))

        y = mess.get_size()[1]
        surface.blit(mess, (100, 50-y/2))

        return surface

    def update_data(self):

        """ Méthode actualisant les données non modifiées """

        self.create_dashboard()

    def set_brawlers_power(self):

        """ Définit les hp des brawlers """

        for i in range(len(self.brawlers)):
            self.brawlers[i].power += 50*i
            self.brawlers[i].card_icon = self.brawlers[i].get_card_icon()

    def get_brawlers_by_type(self, type):

        """ Retourne tout les brawlers de type 'type' """

        liste = self.inventory["brawlers"]
        return [i for i in liste if str(i.type) == type]


    def update(self, screen):

        """ Cette méthode affiche le challenger """

        screen.blit(self.dashboard, self.rect)

