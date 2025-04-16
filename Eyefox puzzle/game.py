from partie import Partie
import pygame

class Game:

    def __init__(self, display, niveau = 0, palier = 0, record = 0):

        self.niveau = niveau
        self.palier = palier
        self.creer_partie()
        self.display = display

        self.sound_effect_interchange1 = pygame.mixer.Sound("assets/sounds/interchange1.mp3")
        self.sound_effect_interchange2 = pygame.mixer.Sound("assets/sounds/interchange2.mp3")

        self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")
        self.wrong_volume = 0.3
        self.correct_volume = 0.2
        self.correct_img = pygame.transform.scale(pygame.image.load("assets/images/correct.png"), (9*18, 9*18)).convert_alpha()
        self.wrong_img = pygame.transform.scale(pygame.image.load("assets/images/false.png"), (9*18, 9*18)).convert_alpha()

        self.wrong = False
        self.correct = False
        self.record = record

        self.home = pygame.image.load("assets/images/home.png").convert_alpha()
        x, y = self.home.get_size()
        self.home = pygame.transform.scale(self.home, (x*2, y*2))
        self.home_rect = self.home.get_rect()
        self.home_hover = pygame.transform.scale(pygame.image.load("assets/images/home_hover.png").convert(), (x*2, y*2))


    def creer_partie(self):

        self.partie = Partie(self.palier, self.niveau)

    def win(self):

        self.niveau += 1
        if self.niveau == 10:
            self.niveau = 0
            self.palier += 1

        if self.palier == 30:
            self.palier = 20

        if self.record < self.palier*10 + self.niveau:
            self.record = self.palier*10 + self.niveau

    def jouer(self, pos):

        if self.home_rect.collidepoint(pos):
            self.back_to_menu()
            
        pos = self.partie.get_pos(pos)
        
        if pos:
                
            self.sound_effect_interchange1.play()
            self.animation_interchange(pos)                
            self.partie.jouer(pos)
            self.display.draw()
            pygame.time.delay(500)
            
            self.check()
        

    def check(self):
        
        if self.partie.win() and self.partie.nb_coup == 0:

            self.correct = True
            self.correct_sound.play()
            time = pygame.time.get_ticks()
            
            while pygame.time.get_ticks() - time < 500:
                self.display.draw()
            self.correct = False
            self.display.transition_1(f"Level {self.niveau+1+self.palier*10}")
            pygame.time.delay(500)
                
            self.win()
            self.creer_partie()
            
            self.display.draw()
            self.display.transition_2(f"Level {self.niveau+1+self.palier*10}")

        elif self.partie.nb_coup == 0 and self.partie.vie > 0:

            self.partie.vie -= 1
            self.wrong = True
            self.wrong_sound.play()
            time = pygame.time.get_ticks()
            
            while pygame.time.get_ticks() - time < 500:
                self.display.draw()
            self.wrong = False
            
            for case in self.partie.choix:
                self.sound_effect_interchange2.play()
                self.animation_interchange(case)
                self.partie.modified_grille.interchange(case)
                
                
            self.partie.nb_coup = self.partie.coup
            self.partie.choix.clear()

            if self.partie.vie == 0:

                self.display.draw()
                pygame.time.delay(1000)

                for case in self.partie.solution:

                    self.sound_effect_interchange1.play()
                    self.animation_interchange(case)
                    self.partie.modified_grille.interchange(case)

                self.display.draw()
                pygame.event.clear()
                self.back_to_menu("Game Over")
                self.palier -= 1
                if self.palier < 0:
                    self.palier = 0
                self.niveau = 0
                self.creer_partie()

    def back_to_menu(self, mess=""):

        self.display.transition_1(mess, 1)
        pygame.time.delay(1000)                
        self.display.maintitle = True
        self.display.ig = False
        self.display.draw()
        self.display.transition_2(mess)

    def update(self, screen, pos):

        volume = pygame.mixer.music.get_volume()

        self.sound_effect_interchange1.set_volume(volume)
        self.sound_effect_interchange2.set_volume(volume)

        self.correct_sound.set_volume(volume*self.correct_volume)
        self.wrong_sound.set_volume(volume*self.wrong_volume)

        self.partie.update(screen, pos)
        if self.wrong:
            a, b = screen.get_size()
            x, y = self.wrong_img.get_size()
            screen.blit(self.wrong_img, (a/2 - x/2, b/2 -y/2))
        if self.correct:
            a, b = screen.get_size()
            x, y = self.correct_img.get_size()
            screen.blit(self.correct_img, (a/2 - x/2, b/2 -y/2))

        self.home_rect.x = 640 - self.home_rect.width
        screen.blit(self.home, self.home_rect)

        if self.home_rect.collidepoint(pos):

            screen.blit(self.home_hover, self.home_rect)

    def animation_interchange(self, pos):
        
        while not self.partie.modified_grille.animation(pos):
            self.display.draw()
