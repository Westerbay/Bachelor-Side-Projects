import pygame

class Maintitle:

    def __init__(self, screensize, fullscreen):

        self.menu = pygame.image.load("assets/images/menu.png").convert_alpha()
        x, y = self.menu.get_size()
        self.menu = pygame.transform.scale(self.menu, (x*3, y*3))

        self.play = pygame.image.load("assets/images/start.png").convert()
        x, y = self.play.get_size()
        self.play = pygame.transform.scale(self.play, (x*3, y*3))
        self.play_rect = self.play.get_rect()
        self.play_hover = pygame.transform.scale(pygame.image.load("assets/images/start_hover.png").convert(), (x*3, y*3))

        self.options = pygame.image.load("assets/images/options.png").convert()
        x, y = self.options.get_size()
        self.options = pygame.transform.scale(self.options, (x*3, y*3))
        self.options_rect = self.options.get_rect()
        self.options_hover = pygame.transform.scale(pygame.image.load("assets/images/options_hover.png").convert(), (x*3, y*3))

        self.exit = pygame.image.load("assets/images/exit.png").convert()
        x, y = self.exit.get_size()
        self.exit = pygame.transform.scale(self.exit, (x*3, y*3))
        self.exit_rect = self.exit.get_rect()
        self.exit_hover = pygame.transform.scale(pygame.image.load("assets/images/exit_hover.png").convert(), (x*3, y*3))

        self.font = pygame.font.Font("assets/font.ttf", 20)
        self.option = False

        self.screensize = screensize
        self.empty_button = pygame.transform.scale(pygame.image.load("assets/images/empty_button.png").convert_alpha(), (x*3, y*3))
        self.resolutions = {fullscreen: "High", (1280, 720): "Medium", (640, 360): "Low"}

        self.suivant = pygame.image.load("assets/images/suivant.png").convert_alpha()
        x, y = self.suivant.get_size()
        self.suivant = pygame.transform.scale(self.suivant, (x*2, y*2))
        self.suivant_rect = self.suivant.get_rect()
        self.suivant_hover = pygame.transform.scale(pygame.image.load("assets/images/suivant_hover.png").convert(), (x*2, y*2))
        
        self.retour = pygame.transform.scale(pygame.image.load("assets/images/retour.png").convert_alpha(), (x*2, y*2))
        self.retour_rect = self.retour.get_rect()
        self.retour_hover = pygame.transform.scale(pygame.image.load("assets/images/retour_hover.png").convert(), (x*2, y*2))
        
        self.resolution_liste = [(640, 360), (1280, 720), fullscreen]
        
        self.sound_bar = pygame.image.load("assets/images/sound_bar.png").convert()
        x, y = self.sound_bar.get_size()
        self.sound_bar = pygame.transform.scale(self.sound_bar, (x * 3, y * 3))
        self.sound_bar_rect = self.sound_bar.get_rect()

        self.curseur = pygame.image.load("assets/images/curseur.png").convert_alpha()
        x, y = self.curseur.get_size()
        self.curseur = pygame.transform.scale(self.curseur, (x * 3, y * 3))
        self.curseur_rect = self.curseur.get_rect()

        self.home = pygame.image.load("assets/images/home.png").convert_alpha()
        x, y = self.home.get_size()
        self.home = pygame.transform.scale(self.home, (x*2, y*2))
        self.home_rect = self.home.get_rect()
        self.home_hover = pygame.transform.scale(pygame.image.load("assets/images/home_hover.png").convert(), (x*2, y*2))

        self.reset = pygame.image.load("assets/images/empty_button.png").convert_alpha()
        x, y = self.reset.get_size()
        self.reset = pygame.transform.scale(self.reset, (x*2, y*2))
        self.reset_rect = self.reset.get_rect()
        self.reset_hover = pygame.transform.scale(pygame.image.load("assets/images/reset_hover.png").convert_alpha(), (x*2, y*2))
        
        self.set_sound()


    def update(self, screen, my_event, pos, events):

        a, b = screen.get_size()
        x, y = self.menu.get_size()
        
        screen.blit(self.menu, (a/2 - x/2, b/2 - y/2))

        if not self.option:
            
            self.play_rect.x, self.play_rect.y = a/2 - x/2 + 30, b/2 - y/2 + 25
            screen.blit(self.play, self.play_rect)

            self.options_rect.x, self.options_rect.y = a/2 - x/2 + 30, b/2 - y/2 + 75
            screen.blit(self.options, self.options_rect)

            self.exit_rect.x, self.exit_rect.y = a/2 - x/2 + 30, b/2 - y/2 + 125
            screen.blit(self.exit, self.exit_rect)

            if self.exit_rect.collidepoint(pos):

                screen.blit(self.exit_hover, self.exit_rect)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.play_rect.collidepoint(pos):

                screen.blit(self.play_hover, self.play_rect)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.options_rect.collidepoint(pos):

                screen.blit(self.options_hover, self.options_rect)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            else:

                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        else:

            screensize = self.font.render("Screen Size", False, (255, 255, 255))
            actual_screensize = self.font.render(self.resolutions[self.screensize], False, (255, 255, 255))
            screen.blit(screensize, (a/2 - x/2 + 34, b/2 - y/2 + 20))
            
            screen.blit(self.empty_button, (a/2 - x/2 + 32, b/2 - y/2 + 40))
            if self.resolutions[self.screensize] == "High":
                screen.blit(actual_screensize, (a/2 - x/2 + 62, b/2 - y/2 + 48))
            elif self.resolutions[self.screensize] == "Medium":
                screen.blit(actual_screensize, (a/2 - x/2 + 54, b/2 - y/2 + 48))
            elif self.resolutions[self.screensize] == "Low":
                screen.blit(actual_screensize, (a/2 - x/2 + 66, b/2 - y/2 + 48))
                
            self.suivant_rect.x, self.suivant_rect.y = a/2 - x/2 + 92, b/2 - y/2 + 80            
            self.retour_rect.x, self.retour_rect.y = a/2 - x/2+34, b/2 - y/2 + 80
            screen.blit(self.retour, self.retour_rect)
            screen.blit(self.suivant, self.suivant_rect)

            sound = self.font.render("Sound", False, (255, 255, 255))
            screen.blit(sound, (a/2 - x/2 + 58, b/2 - y/2 + 110))
            self.sound_bar_rect.x, self.sound_bar_rect.y = a/2 - x/2 + 35, b/2 - y/2 + 130
            volume = pygame.mixer.music.get_volume()
            maximum = self.sound_bar_rect.x + self.sound_bar_rect.width - self.curseur_rect.width + 5
            minimum = self.sound_bar_rect.x - self.curseur_rect.width/4
            distance = maximum - minimum
            self.curseur_rect.x, self.curseur_rect.y = minimum + volume*distance, 205
            separation = self.curseur_rect.x - minimum
            screen.blit(self.sound_bar, self.sound_bar_rect)
            pygame.draw.rect(screen, (0, 120, 255), (self.sound_bar_rect.x+3, self.sound_bar_rect.y+6, separation, 9))
            screen.blit(self.curseur, self.curseur_rect)

            self.home_rect.x, self.home_rect.y = 274, 235
            screen.blit(self.home, self.home_rect)
            self.reset_rect.x, self.reset_rect.y = 304, 235
            screen.blit(self.reset, self.reset_rect)
            reset = self.font.render("Reset", False, (255, 255, 255))
            screen.blit(reset, (315, 238))

            if self.suivant_rect.collidepoint(pos):
                screen.blit(self.suivant_hover, self.suivant_rect)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                
            elif self.retour_rect.collidepoint(pos):
                screen.blit(self.retour_hover, self.retour_rect)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                
            elif self.home_rect.collidepoint(pos):
                screen.blit(self.home_hover, self.home_rect)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.reset_rect.collidepoint(pos):
                screen.blit(self.reset_hover, self.reset_rect)
                screen.blit(reset, (315, 238))
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            else:

                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

                if self.exit_rect.collidepoint(pos) and not self.option:
                    
                    pygame.event.post(pygame.event.Event(my_event["QUITTER"], {}))

                if self.play_rect.collidepoint(pos) and not self.option:

                    pygame.event.post(pygame.event.Event(my_event["JOUER"], {}))

                if self.options_rect.collidepoint(pos):

                    self.option = True

                if self.option and self.suivant_rect.collidepoint(pos):

                    if self.resolution_liste.index(self.screensize) == 2:

                        self.screensize = self.resolution_liste[0]

                    else:

                        self.screensize = self.resolution_liste[self.resolution_liste.index(self.screensize) + 1]
                        
                    pygame.event.post(pygame.event.Event(my_event[f"RESOL{self.resolution_liste.index(self.screensize)}"], {}))

                if self.option and self.retour_rect.collidepoint(pos):

                    self.screensize = self.resolution_liste[self.resolution_liste.index(self.screensize) - 1]
                    pygame.event.post(pygame.event.Event(my_event[f"RESOL{self.resolution_liste.index(self.screensize)}"], {}))

                if self.option and self.reset_rect.collidepoint(pos):

                    pygame.event.post(pygame.event.Event(my_event["RESET"], {}))

                if self.option and self.sound_bar_rect.collidepoint(pos):

                    self.curseur_rect.x = pos[0] - self.curseur_rect.width/2
                    if self.curseur_rect.x < self.sound_bar_rect.x:
                        self.curseur_rect.x = self.sound_bar_rect.x - self.curseur_rect.width/4
                    elif self.curseur_rect.x > self.sound_bar_rect.x + self.sound_bar_rect.width - self.curseur_rect.width + 5:
                        self.curseur_rect.x = self.sound_bar_rect.x + self.sound_bar_rect.width - self.curseur_rect.width + 5
                    self.set_sound()

                if self.option and self.home_rect.collidepoint(pos):

                    self.option = False

        if self.option and pygame.mouse.get_pressed()[0] and self.curseur_rect.collidepoint(pos):

            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            self.curseur_rect.x = pos[0] - self.curseur_rect.width/2
            if self.curseur_rect.x < self.sound_bar_rect.x:
                self.curseur_rect.x = self.sound_bar_rect.x - self.curseur_rect.width/4
            elif self.curseur_rect.x > self.sound_bar_rect.x + self.sound_bar_rect.width - self.curseur_rect.width + 5:
                self.curseur_rect.x = self.sound_bar_rect.x + self.sound_bar_rect.width - self.curseur_rect.width + 5
            self.set_sound()


    def difference_sound(self):

        maximum = self.sound_bar_rect.x + self.sound_bar_rect.width - self.curseur_rect.width + 5
        minimum = self.sound_bar_rect.x - self.curseur_rect.width/4
        distance = maximum - minimum
        separation = self.curseur_rect.x - minimum
        return abs(separation/distance)

    def set_sound(self):

        pygame.mixer.music.set_volume(self.difference_sound())
        
                
