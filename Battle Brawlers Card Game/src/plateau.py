import pygame, random

class Plateau:

    """ Plateau """

    largeur, longueur = 4, 2

    def __init__(self):

        """ Initialisation """

        self.grille = [[0 for _ in range(self.largeur)] for _ in range(self.longueur)]
        self.sound_effect_brawl = pygame.mixer.Sound("../assets/sounds/brawler.wav")
        self.sound_effect_brawl.set_volume(0.4)
        self.sound_effect_card = pygame.mixer.Sound("../assets/sounds/card.wav")
        self.sound_effect_card.set_volume(0.12)

        self.cartes = pygame.sprite.Group()
        self.brawlers = pygame.sprite.Group()
        self.cases_cartes = [(0, 1), (0, 2), (1, 1), (1, 2)]

    def sound_volume(self, value):

        """ Gère le son """

        self.sound_effect_card.set_volume(self.sound_effect_card.get_volume() * value)
        self.sound_effect_brawl.set_volume(self.sound_effect_brawl.get_volume() * value)

    def toutes_les_cases(self):

        """ Renvoie la position de toutes les cases vides """

        return [(i, j) for i in range(self.longueur) for j in range(self.largeur) if self.grille[i][j] == 0]

    def cases_voisines(self):

        """ Renvoie les cases voisines d'une carte """

        return [(i, j) for i, j in self.toutes_les_cases() if self.est_une_case_voisine((i, j))]

    def est_une_case_voisine(self, case):

        """ Renvoie vrai/faux si une case est une case voisine d'une carte """

        x, y = case
        liste_cases_cartes =[(i, j) for i in range(self.longueur) for j in range(self.largeur) if self.grille[i][j] != 0]
        for i in range(3):
            for j in range(3):
                if (x+i-1, j+i-1) in liste_cases_cartes:
                    return True

        return False

    def trouve_carte(self, carte):

        """ Renvoie la position d'une carte """

        pos_cartes = [(i, j) for i in range(self.longueur) for j in range(self.largeur) if self.grille[i][j] != 0]
        for i, j in pos_cartes:
            if self.grille[i][j] == carte:
                return i, j

        return False

    def toute_les_cartes(self):

        """ Renvoie toutes les cartes """

        return [self.grille[i][j] for i in range(self.longueur) for j in range(self.largeur) if self.grille[i][j] != 0]

    def first_tour(self, cartes):

        """ Places les cartes du plateau au premier tour """

        random.shuffle(cartes)
        self.cases_cartes = [(0, 1), (0, 2), (1, 1), (1, 2)]
        for carte in cartes:
            x, y = self.cases_cartes.pop()
            self.grille[x][y] = carte
            self.update_pos(carte, (x, y))
            carte.hidden = True
            carte.animation = True
            self.cartes.add(carte)

        self.sound_effect_card.play()

    def ajoute_carte(self, carte):

        """ Ajoute une carte """

        x, y = random.choice(self.cases_voisines())
        carte.hidden = True
        self.update_pos(carte, (x, y))
        self.grille[x][y] = carte
        self.cartes.add(carte)
        carte.animation = True

        self.sound_effect_card.play()

    def ajoute_brawler(self, carte, brawler):

        """ Ajoute un brawler sur une carte """

        x, y = carte.rect.x, carte.rect.y

        brawler.x = x
        if len(carte.brawlers) == 0:
            brawler.y = y
        else:
            brawler.y = y + 128

        carte.brawlers.append(brawler)
        brawler.animation = True
        self.brawlers.add(brawler)

        self.sound_effect_brawl.play()

    def enleve_carte(self, carte):

        """ Enlève une carte """

        self.cartes.remove(carte)
        for i in carte.brawlers:
            self.brawlers.remove(i)
        x, y = self.trouve_carte(carte)
        self.grille[x][y] = 0

    def remove_brawler_challenger(self, challenger):

        """ Enleve tout les brawlers d'un challenger """

        for i in self.toute_les_cartes():
            for j in i.brawlers:
                if j.challenger == challenger:
                    self.brawlers.remove(j)
                    i.brawlers.remove(j)

    def update_pos(self, carte, pos):

        """ Attribut les coordonnées d'une carte """

        y, x = pos
        carte.rect.x = 235 + 205*x
        carte.rect.y = 99 + 261*y

    def update(self, screen):

        """ Affichage """

        self.cartes.update(screen)
        self.brawlers.update(screen)