import pygame

from player import Player
from sprite import Button_preload
from random import shuffle


class Atelier:
    """ Atelier """

    hover = 0

    def __init__(self):

        """ Initialisation """

        self.player = Player()
        self.gold_cards = list(self.player.inventory["gold_cards"].values())
        self.silver_cards = list(self.player.inventory["silver_cards"].values())
        self.bronze_cards = list(self.player.inventory["bronze_cards"].values())
        self.brawlers_1 = Player().inventory["brawlers"]
        self.brawlers_2 = Player().inventory["brawlers"]
        self.brawlers_3 = Player().inventory["brawlers"]
        for i in self.brawlers_2:
            i.power = 500
            i.card_icon = i.get_card_icon()
        for i in self.brawlers_3:
            i.power = 550
            i.card_icon = i.get_card_icon()
        shuffle(self.gold_cards)
        shuffle(self.silver_cards)
        shuffle(self.bronze_cards)
        shuffle(self.brawlers_1)
        shuffle(self.brawlers_2)
        shuffle(self.brawlers_3)
        self.set_pos()

        self.index_gold = 0
        self.index_silver = 0
        self.index_bronze = 0
        self.index_brawler1 = 0
        self.index_brawler2 = 0
        self.index_brawler3 = 0

        self.suivant_gold = Button_preload(self.get_image("suivant"), self.get_image("suivant_hover"),
                                           self.center_right(self.gold_cards[0].rect,
                                                             self.get_image("suivant").get_size()))
        self.retour_gold = Button_preload(self.get_image("retour"), self.get_image("retour_hover"),
                                          self.center_left(self.gold_cards[0].rect,
                                                           self.get_image("retour").get_size()))
        self.suivant_silver = Button_preload(self.get_image("suivant"), self.get_image("suivant_hover"),
                                             self.center_right(self.silver_cards[0].rect,
                                                               self.get_image("suivant").get_size()))
        self.retour_silver = Button_preload(self.get_image("retour"), self.get_image("retour_hover"),
                                            self.center_left(self.silver_cards[0].rect,
                                                             self.get_image("retour").get_size()))
        self.suivant_bronze = Button_preload(self.get_image("suivant"), self.get_image("suivant_hover"),
                                             self.center_right(self.bronze_cards[0].rect,
                                                               self.get_image("suivant").get_size()))
        self.retour_bronze = Button_preload(self.get_image("retour"), self.get_image("retour_hover"),
                                            self.center_left(self.bronze_cards[0].rect,
                                                             self.get_image("retour").get_size()))

        self.suivant_brawl1 = Button_preload(self.get_image("suivant"), self.get_image("suivant_hover"),
                                             self.center_right(self.brawlers_1[0].rect,
                                                               self.get_image("suivant").get_size()))
        self.retour_brawl1 = Button_preload(self.get_image("retour"), self.get_image("retour_hover"),
                                            self.center_left(self.brawlers_1[0].rect,
                                                             self.get_image("retour").get_size()))
        self.suivant_brawl2 = Button_preload(self.get_image("suivant"), self.get_image("suivant_hover"),
                                             self.center_right(self.brawlers_2[0].rect,
                                                               self.get_image("suivant").get_size()))
        self.retour_brawl2 = Button_preload(self.get_image("retour"), self.get_image("retour_hover"),
                                            self.center_left(self.brawlers_2[0].rect,
                                                             self.get_image("retour").get_size()))
        self.suivant_brawl3 = Button_preload(self.get_image("suivant"), self.get_image("suivant_hover"),
                                             self.center_right(self.brawlers_3[0].rect,
                                                               self.get_image("suivant").get_size()))
        self.retour_brawl3 = Button_preload(self.get_image("retour"), self.get_image("retour_hover"),
                                            self.center_left(self.brawlers_3[0].rect,
                                                             self.get_image("retour").get_size()))

        self.boutons = pygame.sprite.Group()
        self.boutons.add(self.suivant_gold, self.retour_gold, self.suivant_silver, self.retour_silver,
                         self.suivant_bronze, self.retour_bronze, self.suivant_brawl1, self.retour_brawl1,
                         self.suivant_brawl2, self.retour_brawl2, self.suivant_brawl3, self.retour_brawl3)

    def center_left(self, rect, size):

        """ Centre à gauche """

        a, b = size
        x = rect.x + rect.width / 2 - a
        y = rect.y + rect.height
        return x, y

    def center_right(self, rect, size):

        """ Centre à droite """

        a, b = size
        x = rect.x + rect.width / 2
        y = rect.y + rect.height
        return x, y

    def get_image(self, name):

        """ Renvoie l'image """

        image = pygame.image.load(f"../assets/images/menu/{name}.png").convert_alpha()
        x, y = image.get_size()
        image = pygame.transform.scale(image, (x * 4, y * 4))
        return image

    def update(self, screen, mouse, events):

        """ Affichage """

        events = [event.type for event in events]

        self.gold_cards[self.index_gold].update(screen)
        self.silver_cards[self.index_silver].update(screen)
        self.bronze_cards[self.index_bronze].update(screen)
        self.brawlers_1[self.index_brawler1].update(screen)
        self.brawlers_2[self.index_brawler2].update(screen)
        self.brawlers_3[self.index_brawler3].update(screen)
        self.boutons.update(screen)

        self.interaction(mouse, events)

    def interaction(self, mouse, events):

        """ Interaction """

        self.hover = 0
        for bouton in self.boutons:

            if bouton.rect.collidepoint(mouse):

                self.hover += 1
                bouton.is_hover = True

                if pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[0]:

                    # Actions

                    if bouton == self.suivant_gold:
                        self.index_gold += 1
                        if self.index_gold == len(self.gold_cards):
                            self.index_gold = 0
                    elif bouton == self.retour_gold:
                        self.index_gold -= 1
                        if self.index_gold == - 1:
                            self.index_gold = len(self.gold_cards) - 1
                    elif bouton == self.suivant_silver:
                        self.index_silver += 1
                        if self.index_silver == len(self.silver_cards):
                            self.index_silver = 0
                    elif bouton == self.retour_silver:
                        self.index_silver -= 1
                        if self.index_silver == - 1:
                            self.index_silver = len(self.silver_cards) - 1
                    elif bouton == self.suivant_bronze:
                        self.index_bronze += 1
                        if self.index_bronze == len(self.bronze_cards):
                            self.index_bronze = 0
                    elif bouton == self.retour_bronze:
                        self.index_bronze -= 1
                        if self.index_bronze == - 1:
                            self.index_bronze = len(self.bronze_cards) - 1

                    elif bouton == self.suivant_brawl1:
                        self.index_brawler1 += 1
                        if self.index_brawler1 == len(self.brawlers_1):
                            self.index_brawler1 = 0
                    elif bouton == self.retour_brawl1:
                        self.index_brawler1 -= 1
                        if self.index_brawler1 == - 1:
                            self.index_brawler1 = len(self.brawlers_1) - 1
                    elif bouton == self.suivant_brawl2:
                        self.index_brawler2 += 1
                        if self.index_brawler2 == len(self.brawlers_2):
                            self.index_brawler2 = 0
                    elif bouton == self.retour_brawl2:
                        self.index_brawler2 -= 1
                        if self.index_brawler2 == - 1:
                            self.index_brawler2 = len(self.brawlers_2) - 1
                    elif bouton == self.suivant_brawl3:
                        self.index_brawler3 += 1
                        if self.index_brawler3 == len(self.brawlers_3):
                            self.index_brawler3 = 0
                    elif bouton == self.retour_brawl3:
                        self.index_brawler3 -= 1
                        if self.index_brawler3 == - 1:
                            self.index_brawler3 = len(self.brawlers_3) - 1

            else:

                bouton.is_hover = False

    def set_pos(self):

        """ Définit l'emplacement des cartes """

        for carte in self.gold_cards:
            carte.rect.x, carte.rect.y = 370, 140
        for carte in self.silver_cards:
            carte.rect.x, carte.rect.y = 670, 140
        for carte in self.bronze_cards:
            carte.rect.x, carte.rect.y = 970, 140

        for brawler in self.brawlers_1:
            brawler.rect.x, brawler.rect.y = 370, 470
        for brawler in self.brawlers_2:
            brawler.rect.x, brawler.rect.y = 670, 470
        for brawler in self.brawlers_3:
            brawler.rect.x, brawler.rect.y = 970, 470

    def retourne_choix(self):

        """ Renvoie les choix """

        dico = {"field_cards": [self.gold_cards[self.index_gold],
                                self.silver_cards[self.index_silver],
                                self.bronze_cards[self.index_bronze]],
                "brawlers": [self.brawlers_1[self.index_brawler1],
                             self.brawlers_2[self.index_brawler2],
                             self.brawlers_3[self.index_brawler3]]}

        return dico
