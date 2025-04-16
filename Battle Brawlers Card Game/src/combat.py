from sprite import Brawler_Sprite
from minigame import *
import pygame

class Combat:

    """ Classe représentant un combat """

    resolution = (1280, 720)
    mouse, events = None, None
    carte_used = False
    talent_used = False
    combat = False
    end = False
    total_pow = 0
    winner, looser = None, None

    def __init__(self, brawler_1, brawler_2, carte, plateau, volume, display):

        """ Initialisation """

        self.brawlers = pygame.sprite.Group()
        self.brawl1 = Brawler_Sprite(brawler_1)
        self.brawl2 = Brawler_Sprite(brawler_2)
        self.set_pos_brawlers(self.brawl1)
        self.set_pos_brawlers(self.brawl2, False)
        self.brawl1.update_data()
        self.brawl2.update_data()
        self.chall1 = brawler_1.challenger
        self.chall2 = brawler_2.challenger
        self.display = display
        self.transition = True

        self.carte = carte
        self.carte.rect.x, self.carte.rect.y = self.center(self.resolution, self.carte.resolution)
        self.type = carte.combat

        self.plateau = plateau
        self.surface = pygame.Surface(self.resolution)

        self.brawlers.add(self.brawl1, self.brawl2)

        self.carte.retourne = True
        self.volume = volume
        self.brawl1.sound_power_up.set_volume(self.volume * 0.04)
        self.brawl2.sound_power_up.set_volume(self.volume * 0.04)

        if self.type == "click":
            self.minigame = Clicker(self.brawl1, self.brawl2, self.volume)
        elif self.type == "collect":
            self.minigame = Collect(self.brawl1, self.brawl2, self.volume)
        else:
            self.minigame = Grab(self.brawl1, self.brawl2, self.volume)

        self.time_sound = pygame.mixer.Sound("../assets/sounds/time.wav")
        self.time_sound.set_volume(self.volume * 0.25)

    def update(self, screen, events, mouse):

        """ Affichage """

        self.events = events
        self.mouse = mouse
        self.brawlers.update(screen)

        if not self.combat:
            self.carte.update(screen)
        else:
            pygame.draw.rect(screen, (47, 49, 54), (0, 360, 1280, 400))
            screen.blit(self.brawl1.power_img, (self.brawl1.pos_power_x, self.brawl1.fight_power_y+128))
            screen.blit(self.brawl2.power_img, (self.brawl2.pos_power_x, self.brawl2.fight_power_y+128))
            screen.blit(self.brawl1.icon, (self.brawl1.pos_power_x-40, self.brawl1.fight_power_y))
            screen.blit(self.brawl2.icon, (self.brawl2.pos_power_x-40, self.brawl2.fight_power_y))
            self.fight(screen)
            if self.transition:
                self.transition = False
                self.display.transition_2()
                self.minigame.time = pygame.time.get_ticks()
                self.time_sound.play()


        if self.talent_used and not (self.brawl1.animation or self.brawl2.animation) and not self.combat:

            self.display.transition_1()
            self.total_pow = self.brawl2.power + self.brawl1.power
            self.combat = True
            self.brawl1.rect.y -= 130
            self.brawl2.rect.y -= 130
            self.brawl1.affiche_stats = False
            self.brawl2.affiche_stats = False
            self.brawl1.rect.x = self.brawl1.power / self.total_pow * 1280 - self.brawl1.rect.width
            self.brawl2.rect.x = self.brawl1.rect.x + self.brawl1.rect.width

        if not self.carte.retourne and not self.carte_used:

            self.carte.use(self.brawl1, self.brawl2)
            self.carte_used = True

        elif not self.carte.retourne and not self.talent_used and not (self.brawl1.animation or self.brawl2.animation):

            self.carte.talent(self.brawl1, self.brawl2)
            self.talent_used = True

        if self.carte.retourne:
            self.carte.rect.x, self.carte.rect.y = self.center(self.resolution, self.carte.retourne_img[int(self.carte.index) % 10].get_size())

    def set_pos_brawlers(self, brawler, left=True):

        """ Définit les coordonnées d'un brawlers """

        x, y = self.resolution
        a, b = brawler.image.get_size()

        if a/(x/2) > b/y:
            brawler.image = pygame.transform.scale(brawler.image, (x / 2, b * (x / 2) / a))
        else:
            brawler.image = pygame.transform.scale(brawler.image, (a * y / b, y))

        if left:
            brawler.image = pygame.transform.flip(brawler.image, True, False)
            brawler.rect.x, brawler.rect.y = self.center((640, 720), brawler.image.get_size())
            brawler.rect.x -= 200
        else:
            brawler.rect.x, brawler.rect.y = self.center((640, 720), brawler.image.get_size())
            brawler.rect.x += 840

        a, b = brawler.image.get_size()
        brawler.rect.width, brawler.rect.height = a, b

    def center(self, pos1, pos2):

        """ Renvoie une position centrée """

        x, y = pos1
        a, b = pos2

        return x/2 - a/2, y/2 - b/2

    def fight(self, screen):

        """ Combat """

        if self.combat:

            self.brawl1.rect.x = self.brawl1.power/self.total_pow * 1280 - self.brawl1.rect.width
            self.brawl2.rect.x = self.brawl1.rect.x + self.brawl1.rect.width

            pygame.draw.rect(screen, self.brawl2.type.get_color(), (0, 320, 1280, 40))
            pygame.draw.rect(screen, (0, 0, 0), (0, 320, 1280, 40), 3)
            pygame.draw.rect(screen, self.brawl1.type.get_color(), (0, 320, self.brawl2.rect.x, 40))
            pygame.draw.rect(screen, (0, 0, 0), (0, 320, self.brawl2.rect.x, 40), 3)

            if self.minigame.play(screen, self.events, self.mouse):

                if self.brawl1.power > self.brawl2.power:
                    self.chall1.point += 1
                    self.chall1.update_data()
                    self.winner = self.chall1
                    self.looser = self.chall2
                elif self.brawl1.power < self.brawl2.power:
                    self.chall2.point += 1
                    self.chall2.update_data()
                    self.winner = self.chall2
                    self.looser = self.chall1
                else:
                    choix = random.randint(0, 1)
                    if choix:
                        self.chall1.point += 1
                        self.chall1.update_data()
                        self.winner = self.chall1
                        self.looser = self.chall2
                    else:
                        self.chall2.point += 1
                        self.chall2.update_data()
                        self.winner = self.chall2
                        self.looser = self.chall1

                self.plateau.enleve_carte(self.carte)
                self.end = True