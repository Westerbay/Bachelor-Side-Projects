import pygame
from sprite import Menu_Button
from sprite import Button_preload

class Maintitle:

    """ Ecran titre """

    screensize = (1280, 720)
    hover = 0

    def __init__(self, volume):

        """ Initialisation """

        self.option = False
        self.sound_volume = volume
        self.surface = pygame.Surface(self.screensize)
        self.background = pygame.image.load("../assets/images/background.png")
        self.font = pygame.font.Font("../assets/font/font.ttf", 100)
        self.title = self.font.render("Battle Brawlers Card Game", False, (255, 255, 255))
        self.title_rect = self.title.get_rect()
        self.title_rect.x, self.title_rect.y = self.center(self.title, True, False)

        #Menu
        self.menu = pygame.sprite.Group()
        self.options_button = pygame.sprite.Group()
        self.image_menu = self.get_image("menu")
        self.image_menu_rect = self.image_menu.get_rect()
        self.image_menu_rect.x, self.image_menu_rect.y = self.center(self.image_menu, False, True)
        x, y = self.image_menu_rect.x, self.image_menu_rect.y

        self.play = Menu_Button("Start", x + 60, y + 50)
        self.options = Menu_Button("Options", x + 60, y + 150)
        self.exit = Menu_Button("Exit", x + 60, y + 250)
        self.menu.add(self.play, self.options, self.exit)

        self.font2 = pygame.font.Font("../assets/font/font.ttf", 40)
        self.screensize_text = self.font2.render("Screen Size", False, (255, 255, 255))
        self.screensize_text_pos = (x + 68, y + 40)
        if pygame.display.get_window_size() == self.screensize:
            self.size_button = Menu_Button("Medium", x + 64, y + 80)
        else:
            self.size_button = Menu_Button("High", x + 64, y + 80)
        self.sound_text = self.font2.render("Sound", False, (255, 255, 255))
        self.sound_text_pos = (x + 116, y + 170)
        self.sound_bar = Button_preload(self.get_image("sound_bar"), None, (x + 75, y + 225))
        self.back_home = Button_preload(self.get_image("home"), self.get_image("home_hover"), (x + 110, 450))
        self.curseur = Button_preload(self.get_image("curseur"), None, (0, 0))
        self.options_button.add(self.size_button, self.back_home, self.sound_bar, self.curseur)

        pygame.mixer.music.load("../assets/sounds/maintitle.mp3")
        pygame.mixer.music.set_volume(self.sound_volume)
        pygame.mixer.music.play(-1)

    def update(self, mouse, events, my_events):

        """ Affichage """

        self.surface.blit(self.background, (0, 0))
        self.surface.blit(self.title, self.title_rect)
        self.surface.blit(self.image_menu, self.image_menu_rect)
        if not self.option:
            self.menu.update(self.surface)
        else:
            self.surface.blit(self.screensize_text, self.screensize_text_pos)
            self.surface.blit(self.sound_text, self.sound_text_pos)
            volume = pygame.mixer.music.get_volume()
            maximum = self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5
            minimum = self.sound_bar.rect.x - self.curseur.rect.width / 4
            distance = maximum - minimum
            self.curseur.rect.x, self.curseur.rect.y = minimum + volume*distance, 375
            self.options_button.update(self.surface)
            separation = self.curseur.rect.x - minimum
            pygame.draw.rect(self.surface, (0, 120, 255), (self.sound_bar.rect.x+6, self.sound_bar.rect.y+12, separation, 18))
            self.curseur.update(self.surface)
        self.interaction(mouse, events, my_events)

    def interaction(self, mouse, events, my_events):

        """ Interactions """

        events = [event.type for event in events]

        self.hover = 0

        if not self.option:

            for bouton in self.menu:
                bouton.is_hover = False
                if bouton.rect.collidepoint(mouse):

                    bouton.is_hover = True
                    self.hover += 1

                    if pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[0]:
                        #On clique sur le bouton

                        if bouton == self.exit:
                            self.post(my_events["QUITTER"])
                        elif bouton == self.play:
                            self.post(my_events["JOUER"])
                        elif bouton == self.options:
                            self.option = True

        else:

            for bouton in self.options_button:
                bouton.is_hover = False
                if bouton.rect.collidepoint(mouse):

                    bouton.is_hover = True
                    self.hover += 1

                    if pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[0]:
                        # On clique sur le bouton

                        if bouton.rect == self.size_button.rect:
                            if pygame.display.get_window_size() == self.screensize:
                                self.size_button = Menu_Button("High", self.size_button.rect.x, self.size_button.rect.y)
                                self.post(my_events["RESOL1"])
                            else:
                                self.size_button = Menu_Button("Medium", self.size_button.rect.x, self.size_button.rect.y)
                                self.post(my_events["RESOL0"])
                            self.options_button.remove(self.size_button)
                            self.options_button.add(self.size_button)

                        elif bouton == self.back_home:
                            self.option = False

                    elif pygame.mouse.get_pressed()[0] and (bouton == self.curseur or bouton == self.sound_bar):
                        self.curseur.rect.x = mouse[0] - self.curseur.rect.width / 2
                        if self.curseur.rect.x < self.sound_bar.rect.x:
                            self.curseur.rect.x = self.sound_bar.rect.x - self.curseur.rect.width / 4
                        elif self.curseur.rect.x > self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5:
                            self.curseur.rect.x = self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5
                        self.set_sound()

    def post(self, event):

        """ Création événement """

        pygame.event.post(pygame.event.Event(event, {}))

    def get_image(self, name):

        """ Renvoie l'image associée """

        image = pygame.image.load(f"../assets/images/menu/{name}.png").convert_alpha()
        x, y = image.get_size()
        return pygame.transform.scale(image, (x * 6, y * 6))

    def center(self, image, c=True, d=True):

        """ Centre au milieu de l'écran """

        x, y = self.screensize
        a, b = image.get_size()

        if c and d:
            return x / 2 - a / 2, y / 2 - b / 2
        elif c:
            return x / 2 - a / 2, 0

        return 0, y / 2 - b / 2

    def difference_sound(self):

        """ Permet la gestion du son """

        maximum = self.sound_bar.rect.x + self.sound_bar.rect.width - self.curseur.rect.width + 5
        minimum = self.sound_bar.rect.x - self.curseur.rect.width / 4
        distance = maximum - minimum
        separation = self.curseur.rect.x - minimum
        return abs(separation / distance)

    def set_sound(self):

        """ Actualise le son """

        pygame.mixer.music.set_volume(self.difference_sound())