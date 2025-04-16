from challenger import Challenger
import random, pygame

class Player(Challenger):

    """ Cette classe représente le joueur """

    veut_jouer_brawler = False
    veut_jouer_carte = False
    brawler_2_play = False

    def __init__(self):

        """ Initialisation """

        super().__init__("You", 1)

        self.field_cards_sprite = pygame.sprite.Group()
        self.brawlers_sprite = pygame.sprite.Group()
        self.gold_card = self.choix_gold_card()
        self.silver_card = self.choix_silver_card()
        self.bronze_card = self.choix_bronze_card()
        self.field_cards = [self.gold_card, self.silver_card, self.bronze_card]
        self.field_cards_sprite.add(self.gold_card, self.silver_card, self.bronze_card)

        self.brawlers = [self.inventory["brawlers"].pop(random.randint(0, len(self.inventory["brawlers"]) - 1)) for _ in
                         range(3)]
        self.set_brawlers_power()
        self.all_brawlers = self.brawlers.copy()

        for i in self.brawlers:
            self.brawlers_sprite.add(i)

    def choix_gold_card(self):

        """ Choix de la gold card """

        return self.inventory["gold_cards"][random.choice(list(self.inventory["gold_cards"].keys()))]

    def choix_silver_card(self):

        """ Choix de la silver card """

        return self.inventory["silver_cards"][random.choice(list(self.inventory["silver_cards"].keys()))]

    def choix_bronze_card(self):

        """ Choix de la silver card """

        return self.inventory["bronze_cards"][random.choice(list(self.inventory["bronze_cards"].keys()))]

    def choose_field_card(self):

        """ Choix de la carte 'field' """

        random.shuffle(self.field_cards)
        return self.field_cards.pop()

    def jouer(self, plateau):

        """ Permet au joueur de jouer pendant son tour """

        return True

    def update_pos(self):

        """ Actualisation de la position des cartes fields """

        #Field cards
        n = len(self.field_cards)
        for i in range(len(self.field_cards)):

            if n == 1:
                self.field_cards[i].rect.x = 540
                self.field_cards[i].rect.y = 232
            elif n == 3:
                self.field_cards[i].rect.x = 540 + 280 * (i - 1)
                self.field_cards[i].rect.y = 232
            elif n == 2:
                self.field_cards[i].rect.x = 660 + 280 * (i - 1)
                self.field_cards[i].rect.y = 232

        #Brawlers
        n = len(self.brawlers)
        for i in range(len(self.brawlers)):

            if n == 1:
                self.brawlers[i].rect.x = 540
                self.brawlers[i].rect.y = 296
            elif n == 3:
                self.brawlers[i].rect.x = 540 + 280 * (i - 1)
                self.brawlers[i].rect.y = 296
            elif n == 2:
                self.brawlers[i].rect.x = 660 + 280 * (i - 1)
                self.brawlers[i].rect.y = 296

    def jouer_carte(self, carte, plateau):

        """ Joue une carte """

        self.field_cards.remove(carte)
        self.field_cards_sprite.remove(carte)
        plateau.ajoute_carte(carte)
        self.veut_jouer_carte = False
        self.peut_jouer_carte = False

    def jouer_brawler(self, carte, plateau):

        """ Joue un brawler """

        plateau.ajoute_brawler(carte, self.brawler_2_play)
        self.brawlers.remove(self.brawler_2_play)
        self.brawlers_sprite.remove(self.brawler_2_play)
        self.peut_jouer_brawler = False