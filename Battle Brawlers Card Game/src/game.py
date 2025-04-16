from player import Player
from ordi import Ordi
from plateau import Plateau
from combat import Combat
from sprite import Button, Desc, Hand
import pygame, random

class Game:

    """ Cette classe représente le jeu """

    tour, count_hover = 0, 0
    position_brawler_selected = (540, 535)
    turn_index = -1

    def __init__(self, resolution, display, volume, choix):

        """ Initialisation """

        self.music_volume = volume
        self.display = display
        self.resolution = resolution
        self.surface = pygame.Surface(resolution)
        self.background = pygame.image.load("../assets/images/background.png").convert()
        self.plateau = Plateau()
        self.shadow = self.create_shadow()
        self.combat = False
        self.animation = False
        self.transition = False
        self.last_surface = pygame.Surface(resolution)

        self.challengers = pygame.sprite.Group()
        self.boutons = pygame.sprite.Group()
        self.annoncement = pygame.sprite.Group()

        #Boutons
        res = 120
        self.plateau_button = Button("Game", 640-res/2 - res - 20, 5)
        self.brawler_button = Button("Brawlers", 640-res/2, 5)
        self.carte_button = Button("Card", 640-res/2 + res + 20, 5)
        self.hand1 = Hand(640-res/2 - res - 20 + 48, 50)
        self.hand2 = Hand(640-res/2 + 48, 50)
        self.hand3 = Hand(640-res/2 + res + 20 + 48, 50)
        self.desc_pick_card = Desc("Pick a card", 640-225/2, 720-56)
        self.desc_pick_brawler = Desc("Pick a brawler", 640 - 270 / 2, 720 - 56)
        self.desc_choose_card = Desc("Choose a card", 640 - 255 / 2, 720 - 56)
        self.boutons.add(self.plateau_button, self.brawler_button, self.carte_button)
        self.crown = pygame.image.load("../assets/images/crown.png").convert_alpha()

        #Joueurs
        self.j1 = Player()
        self.j2 = Ordi(2)
        self.j3 = Ordi(3)
        self.j4 = Ordi(4)
        self.j1.field_cards = choix["field_cards"]
        self.j1.field_cards_sprite.empty()
        for i in self.j1.field_cards:
            self.j1.field_cards_sprite.add(i)
        self.j1.brawlers = choix["brawlers"]
        self.j1.brawlers_sprite.empty()
        for i in self.j1.brawlers:
            i.challenger = self.j1
            self.j1.brawlers_sprite.add(i)
        self.j1.update_pos()
        self.j1.all_brawlers = self.j1.brawlers.copy()
        self.challengers.add(self.j1, self.j2, self.j3, self.j4)

        #Sound
        self.load_music()
        self.sound_effect_warp = pygame.mixer.Sound("../assets/sounds/warp.wav")
        self.win = pygame.mixer.Sound("../assets/sounds/win.wav")
        self.set_volume_sound()

        self.need2wait = False
        self.end = False

    def wait(self):

        """ Y-a-t-il une animation ? """

        for brawl in self.plateau.brawlers:
            if brawl.animation:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
                return True

        for carte in self.plateau.cartes:
            if carte.animation:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
                return True

        return False

    def load_music(self):

        """ Charge la musique """

        pygame.mixer.music.load("../assets/sounds/game.mp3")
        pygame.mixer.music.play(-1)

    def set_volume_sound(self):

        """ Modifie le son de la musique """

        pygame.mixer.music.set_volume(self.music_volume)
        self.music_volume *= 2
        self.sound_effect_warp.set_volume(0.4 * self.music_volume)
        self.win.set_volume(0.6 * self.music_volume)
        self.plateau.sound_volume(self.music_volume)

    def update(self, pos, events, my_events):

        """ Méthode d'affichage """

        self.mouse = pos
        self.events = [event.type for event in events]

        if type(self.combat) is Combat:
            if self.combat.end and self.transition:
                self.combat = False
                self.display.transition_2()
                self.transition = False

        if self.need2wait:
            self.need2wait = False
            pygame.time.delay(2000)
            pygame.event.clear()
            self.annoncement.empty()
            if self.end:
                pygame.time.delay(2000)
                pygame.event.post(pygame.event.Event(my_events["END"], {}))

        self.surface.blit(self.background, (0, 0))

        if len(self.annoncement) != 0:
            self.need2wait = True
            if len(self.annoncement) < 2:
                self.surface.blit(self.last_surface, (0, 0))
                self.annoncement.update(self.surface)
            if self.end:
                self.win.play()
                self.surface.blit(self.crown, (576, 200))

        elif not self.combat:
            self.challengers.update(self.surface)
            self.plateau.update(self.surface)
            if self.tour != 0:
                self.boutons.update(self.surface)
            if not self.wait() and not self.animation:
                self.jouer()
            if not self.combat:
                self.tour_player_draw()
            self.last_surface.blit(self.surface, (0, 0))
        else:
            self.combat.update(self.surface, self.events, self.mouse)
            if self.transition:
                self.display.transition_2()
                self.transition = False
                self.plateau.sound_effect_brawl.play()
            if self.combat.end:
                self.display.transition_1()
                self.transition = True
                self.annoncement.add(
                    Desc(f"{self.combat.winner.name} defeated {self.combat.looser.name} !"))
                self.surface.blit(self.last_surface, (0, 0))


    def start(self):

        """ Choix des 4 cartes fields """

        if self.j1.field_cards != []:
            choix_j1 = self.player_choose_field_card()
            cartes = [choix_j1]
        else:
            cartes = []
            choix_j1 = True

        if choix_j1:

            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

            for challenger in self.challengers:

                if challenger != self.j1 and challenger.field_cards != []:
                    cartes.append(challenger.choose_field_card())

            self.plateau.first_tour(cartes)
            if self.tour == 0:
                self.tour += 1
                self.j1.turn = True
                self.j1.animation = True

    def jouer(self):

        """ Méthode déroulement d'une partie """

        self.count_hover = 0

        for chall in self.challengers:
            if chall.point == 3:
                if chall != self.j1:
                    self.annoncement.add(
                        Desc(f"{chall.name} wins !"))
                else:
                    self.annoncement.add(
                        Desc(f"{chall.name} win !"))
                self.end = True
                return None

        if self.tour == 0:

            self.start()

        else:

            if self.plateau.toute_les_cartes() == []:

                self.start()

            elif self.j1.turn:

                self.actions_button()

                if self.j1_jouer():

                    self.j1.turn = False
                    self.j2.turn = True
                    self.check_fight()

            elif self.j2.turn:

                if self.j2.jouer(self.plateau):
                    self.j2.turn = False
                    self.j3.turn = True
                    self.check_fight()

            elif self.j3.turn:

                if self.j3.jouer(self.plateau):
                    self.j3.turn = False
                    self.j4.turn = True
                    self.check_fight()

            else:

                if self.j4.jouer(self.plateau):
                    self.j4.turn = False
                    self.j1.turn = True
                    self.check_fight()
                    self.reset()

        if self.count_hover == 0:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

    def actions_button(self):

        """ Interaction avec les boutons """

        for bouton in self.boutons:

            bouton.is_hover = False

            if bouton.rect.collidepoint(self.mouse):

                self.count_hover += 1
                bouton.is_hover = True

                if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:

                    if bouton == self.plateau_button:
                        self.j1.veut_jouer_carte = False
                        self.j1.veut_jouer_brawler = False
                        self.j1.brawler_2_play = False
                    elif bouton == self.brawler_button:
                        self.j1.veut_jouer_carte = False
                        self.j1.veut_jouer_brawler = True
                        self.j1.brawler_2_play = False
                    elif bouton == self.carte_button:
                        self.j1.veut_jouer_carte = True
                        self.j1.veut_jouer_brawler = False
                        self.j1.brawler_2_play = False

    def j1_jouer(self):

        """ Tour du joueur"""

        if self.plateau.cases_voisines() == []:
            self.j1.peut_jouer_carte = False

        if not self.j1.peut_jouer_brawler:
            return True

        if self.j1.veut_jouer_brawler:

            if not self.j1.brawler_2_play:
                self.j1.update_pos()
                if self.j1.peut_jouer_carte and len(self.j1.field_cards):
                    self.hand3.update(self.surface)
                self.hand1.update(self.surface)
                self.hand3.y, self.hand3.vel = self.hand1.y, self.hand1.vel
                self.surface.blit(self.shadow, (0, 0))
                self.j1.brawlers_sprite.update(self.surface)
                brawler = self.pick_brawler_card()
                self.j1.brawler_2_play = brawler
            else:
                carte = self.choose_card()
                if carte:
                    self.j1.jouer_brawler(carte, self.plateau)

                self.j1.brawler_2_play.update(self.surface)

        elif self.j1.veut_jouer_carte and self.j1.peut_jouer_carte:

            self.hand2.update(self.surface)
            self.hand1.update(self.surface)
            self.hand2.y, self.hand2.vel = self.hand1.y, self.hand1.vel

            self.j1.update_pos()
            self.surface.blit(self.shadow, (0, 0))
            self.j1.field_cards_sprite.update(self.surface)
            carte = self.pick_field_card()
            if carte:
                self.j1.jouer_carte(carte, self.plateau)

        else:

            if self.j1.peut_jouer_carte and len(self.j1.field_cards):
                self.hand3.update(self.surface)
            self.hand2.update(self.surface)
            self.hand3.y, self.hand3.vel = self.hand2.y, self.hand2.vel

        return False

    def reset(self):

        """ Reset tour"""

        pygame.event.clear()
        for i in self.challengers:
            i.peut_jouer_carte = True
            i.peut_jouer_brawler = True
            i.turn_rect.x = -300
            if i.brawlers == []:
                self.plateau.remove_brawler_challenger(i)
                i.brawlers = i.all_brawlers.copy()
                for j in i.brawlers:
                    j.rect = j.initial_rect.copy()
                    if i == self.j1:
                        i.brawlers_sprite.add(j)
        self.tour += 1
        self.j1.brawler_2_play = False
        self.j1.veut_jouer_carte = False
        self.j1.veut_jouer_brawler = False

    def tour_player_draw(self):

        """ Action tour du joueur hover """

        for challenger in self.challengers:
            if challenger.turn:

                pygame.draw.rect(self.surface, (218, 99, 0), challenger.rect, 8)

                if challenger.turn_rect.x <= 1280 and not self.wait():
                    self.animation = True
                    self.surface.blit(self.shadow, (0, 0))
                    self.surface.blit(challenger.turn_img, challenger.turn_rect)
                    challenger.turn_rect.x += (self.turn_index*4.9) ** 2
                    if round(self.turn_index, 3) == -0.95:
                        self.sound_effect_warp.play()
                    self.turn_index += 0.01

                elif challenger.turn_rect.x > 1280:
                    self.animation = False
                    self.turn_index = -1


    def choose_card(self):

        """ Choisis une carte sur le plateau """

        self.desc_choose_card.update(self.surface)

        for carte in self.plateau.toute_les_cartes():

            if carte.rect.collidepoint(self.mouse):

                self.count_hover += 1

                if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:

                    return carte

        return False

    def pick_field_card(self):

        """ Choisis une carte field j1 """

        self.desc_pick_card.update(self.surface)

        for carte in self.j1.field_cards:

            if carte.rect.collidepoint(self.mouse):

                self.count_hover += 1

                if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:

                    if self.plateau.toute_les_cartes() == []:
                        self.j1.field_cards.remove(carte)
                        self.j1.field_cards_sprite.remove(carte)
                    return carte

        return False

    def pick_brawler_card(self):

        """ Choisis un brawler j1 """

        self.desc_pick_brawler.update(self.surface)

        for brawler in self.j1.brawlers:

            if brawler.rect.collidepoint(self.mouse):

                self.count_hover += 1

                if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:

                    brawler.rect.x, brawler.rect.y = self.position_brawler_selected
                    return brawler

        return False

    def player_choose_field_card(self):

        """ Choix du joueur cartes 'field' """

        self.desc_pick_card.update(self.surface)

        self.surface.blit(self.shadow, (0, 0))
        self.j1.update_pos()
        self.j1.field_cards_sprite.update(self.surface)
        return self.pick_field_card()

    def check_fight(self):

        """ Regarde si il faut commencer un combat """

        for carte in self.plateau.toute_les_cartes():

            if len(carte.brawlers) == 2:

                brawler_1, brawler_2 = carte.brawlers[0], carte.brawlers[1]
                if brawler_1.challenger == brawler_2.challenger:

                    brawler_1.challenger.point += 1
                    self.plateau.enleve_carte(carte)
                    brawler_1.challenger.update_data()
                    self.annoncement.add(Desc(f"{brawler_1.challenger.name} did a double capture !"))

                elif brawler_1.challenger.name != "You" and brawler_2.challenger.name != "You":

                    carte.use(brawler_1, brawler_2)
                    carte.talent(brawler_1, brawler_2)
                    if brawler_1.type.est_fort_contre(brawler_2.type):
                        brawler_1.power *= 2
                    elif brawler_2.type.est_fort_contre(brawler_1.type):
                        brawler_2.power *= 2
                    total_pow = brawler_2.power + brawler_1.power

                    if random.randint(0, total_pow) < brawler_1.power:

                        brawler_1.challenger.point += 1
                        self.plateau.enleve_carte(carte)
                        brawler_1.challenger.update_data()
                        self.annoncement.add(
                            Desc(f"{brawler_1.challenger.name} defeated {brawler_2.challenger.name} !"))

                    else:

                        brawler_2.challenger.point += 1
                        self.plateau.enleve_carte(carte)
                        brawler_2.challenger.update_data()
                        self.annoncement.add(
                            Desc(f"{brawler_2.challenger.name} defeated {brawler_1.challenger.name} !"))

                else:

                    self.combat = Combat(brawler_1, brawler_2, carte, self.plateau, self.music_volume, self.display)
                    self.transition = True
                    self.display.transition_1()


    def create_shadow(self):

        """ Créer un assombrissement """

        surface = pygame.Surface(self.resolution)
        surface.set_alpha(200)
        return surface