from challenger import Challenger
import random

class Ordi(Challenger):

    """ Cette classe représente une IA """

    name = ["Tristan", "Alex", "Marc", "Jean", "Geoffrey", "Thomas", "Nathan", "Pierre", "Thibault", "Ben",
            "Zoe", "Axel", "Lucie", "Eva", "Sanna", "Amance", "Julie", "Katia", "Aude", "Daisy"]
    proba_field_card = 50
    vient_de_jouer = False

    def __init__(self, number):

        """ Initialisation """

        name = random.choice(self.name)
        super().__init__(name, number)

        #Choix Brawler
        monotype = random.choice([True, False])
        if monotype:
            type = random.choice(self.all_types)
            brawl_type = self.get_brawlers_by_type(type)
            self.brawlers = [brawl_type.pop(random.randint(0, len(brawl_type)-1)) for _ in range(3)]
        else:
            self.brawlers = [self.inventory["brawlers"].pop(random.randint(0, len(self.inventory["brawlers"])-1)) for _ in range(3)]
        self.set_brawlers_power()
        self.all_brawlers = self.brawlers.copy()

        #Choix Cartes
        self.gold_card = self.choix_gold_card()
        self.silver_card = self.choix_silver_card()
        self.bronze_card = self.choix_bronze_card()
        self.field_cards = [self.gold_card, self.silver_card, self.bronze_card]

    def choix_gold_card(self):

        """ Choix de la gold card """

        for i in self.brawlers:

            if i.name in list(self.inventory["gold_cards"].keys()):

                return self.inventory["gold_cards"][i.name]

        return self.inventory["gold_cards"][random.choice(list(self.inventory["gold_cards"].keys()))]

    def choix_silver_card(self):

        """ Choix de la silver card """

        liste = []
        for i in self.brawlers:
            type = i.type.type
            for j in self.inventory["silver_cards"]:
                if self.inventory["silver_cards"][j].plus_haute_stats() == type:
                    liste.append(self.inventory["silver_cards"][j])

        return random.choice(liste)

    def choix_bronze_card(self):

        """ Choix de la silver card """

        liste = []
        for i in self.brawlers:
            type = i.type.type
            for j in self.inventory["bronze_cards"]:
                if type in self.inventory["bronze_cards"][j].plus_basse_stats():
                    liste.append(self.inventory["bronze_cards"][j])

        return random.choice(liste)

    def choose_field_card(self):

        """ Choix de la carte 'field' """

        random.shuffle(self.field_cards)
        return self.field_cards.pop()

    def choose_brawler(self):

        """ Choix du brawler """

        random.shuffle(self.brawlers)
        return self.brawlers.pop()

    def jouer(self, plateau):

        """ Permet au joueur de jouer pendant son tour """

        if self.vient_de_jouer:
            self.vient_de_jouer = False
            return False

        if not self.peut_jouer_carte and not self.peut_jouer_brawler:
            return True

        if plateau.cases_voisines() != [] and self.peut_jouer_carte and self.field_cards != [] and random.randint(0, 100) < self.proba_field_card:
            self.peut_jouer_carte = False
            carte = self.choose_field_card()
            plateau.ajoute_carte(carte)
            self.vient_de_jouer = True

        elif self.peut_jouer_brawler:
            brawler = self.choose_brawler()
            carte = random.choice(plateau.toute_les_cartes())
            plateau.ajoute_brawler(carte, brawler)
            self.peut_jouer_brawler = False

        self.peut_jouer_carte = False

        return False