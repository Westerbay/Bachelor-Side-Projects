import pygame, sys, csv
from game import Game
from maintitle import Maintitle
from sprite import Fox
from grille import Grille

class Interface:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        dico = self.load()
        self.resolution = dico["resolution"]
        self.volume = dico["volume"]
        
        info = pygame.display.Info()
        self.fullscreen = (info.current_w, info.current_h)

        if self.resolution == (1920, 1080):
            self.resolution = self.fullscreen
        
        if self.resolution == self.fullscreen:
            self.display = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN, display=0)
        else:
            self.display = pygame.display.set_mode(self.resolution, display=0)
            
        self.title = "Eyefox puzzle"
        pygame.display.set_caption(self.title)
        self.icon = pygame.image.load("assets/images/icone.png").convert()
        pygame.display.set_icon(self.icon)
        self.screen = pygame.Surface((640, 360))
        
        self.game = Game(self, dico["niveau"], dico["palier"], dico["record"])
        self.main = Maintitle(self.resolution, self.fullscreen)
        
        self.time = pygame.time.Clock()
        pygame.mixer.music.load("assets/sounds/game.mp3")
        self.background = pygame.image.load("assets/images/background.png").convert()
        self.font = pygame.font.Font("assets/font.ttf", 150)
        self.font2 = pygame.font.Font("assets/font.ttf", 60)

        self.empty_pannel = pygame.image.load("assets/images/empty_button.png").convert_alpha()

        self.maintitle = True
        self.ig = False

        self.JOUER = pygame.USEREVENT + 1
        self.QUITTER = pygame.USEREVENT + 2
        self.RESOL0 = pygame.USEREVENT + 3
        self.RESOL1 = pygame.USEREVENT + 4
        self.RESOL2 = pygame.USEREVENT + 5
        self.RESET = pygame.USEREVENT + 6

        self.my_event = {"QUITTER": self.QUITTER, "JOUER": self.JOUER, "RESOL0": self.RESOL0, "RESOL1": self.RESOL1,
                         "RESOL2": self.RESOL2, "RESET": self.RESET}
        pygame.mixer.set_num_channels(2)
        self.sprites = pygame.sprite.Group()
        self.grille = Grille(4)
        self.case = self.grille.choisir_nb_cases(1)[0]
        self.sprites.add(Fox("sleep", 70, 110), Fox("stand", 120, 190), Fox("awake", 160, 110))

        self.font3 = pygame.font.Font("assets/font.ttf", 50)
        self.new_delay = 0

    def handle_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_F4] and keys[pygame.K_LALT]:

            self.quitter()

    def loop(self):

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)
        
        while True:

            self.game.check()

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT or event.type == self.QUITTER:

                    self.quitter()

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

                    pos = self.convert_point(pygame.mouse.get_pos())
                    
                    if self.ig:
                        
                        self.game.jouer(pos)

                    
                if event.type == self.JOUER:
                    
                    lvl = self.game.niveau + 1 + self.game.palier*10
                    self.transition_1(f"Level {lvl}", 1)

                    self.ig = True
                    self.maintitle = False

                    self.draw()
                    self.transition_2(f"Level {lvl}")

                if event.type == self.RESOL0:
                    self.display = pygame.display.set_mode((640, 360), display=0)
                    self.resolution = (640, 360)
                if event.type == self.RESOL1:
                    self.display = pygame.display.set_mode((1280, 720), display=0)
                    self.resolution = (1280, 720)
                if event.type == self.RESOL2:
                    self.display = pygame.display.set_mode(self.fullscreen, pygame.FULLSCREEN, display=0)
                    self.resolution = self.fullscreen

                if event.type == self.RESET:
                    self.reset()
                    self.save()
                    

            self.handle_input()
            self.draw(events)

    def quitter(self):

        pygame.quit()
        sys.exit()

    def convert_point(self, point):

        a, b = point
        c, d = self.screen.get_size()
        e, f = self.resolution
        x = a*c/e
        y = b*d/f

        return (x, y)

    def draw(self, events=[]):

        self.time.tick(30)
        pos = self.convert_point(pygame.mouse.get_pos())

        self.screen.blit(self.background, (0,0))
        title = self.font2.render(self.title, False, (255, 255, 255))
        self.screen.blit(pygame.transform.scale(self.empty_pannel, (360, 60)), (320-364/2, 2))
        self.screen.blit(title, (320-title.get_size()[0]/2, 0))        

        if self.maintitle:
            self.sprites.update(self.screen)
            self.screen.blit(self.grille.surface, (430, 120))
            if pygame.time.get_ticks() - self.new_delay > 1000:
                if self.grille.animation(self.case):
                    self.grille.interchange(self.case)
                    self.case = self.grille.choisir_nb_cases(1)[0]
                    self.grille.actualisation()
                    self.new_delay = pygame.time.get_ticks()

        mess = self.font3.render(f"Record: {self.game.record}", False, (255, 255, 255))
        x, y = mess.get_size()
        self.screen.blit(mess, (320 - x/2, 360-y))
        
        if self.ig: self.game.update(self.screen, pos)
        if self.maintitle:
            self.main.update(self.screen, self.my_event, pos, events)
        self.display.blit(pygame.transform.scale(self.screen, self.resolution), (0, 0))
        pygame.display.flip()

    def transition_1(self, mess, vel=3):

        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        n = 255

        while n >= 0:

            self.display.fill((0, 0, 0))
            self.screen.set_alpha(n)
            img = self.font.render(mess, False, (255, 255, 255))
            img.set_alpha(255-n)
            a, b = self.display.get_size()
            x, y = img.get_size()
            self.display.blit(img, (a/2 - x/2, b/2 - y/2))
            self.display.blit(pygame.transform.scale(self.screen, self.resolution), (0, 0))
            pygame.display.flip()
            n -= vel

        pygame.event.clear()

    def transition_2(self, mess):

        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        self.save()

        n = 0

        while n != 255:                

            self.display.fill((0, 0, 0))
            self.screen.set_alpha(n)
            img = self.font.render(mess, False, (255, 255, 255))
            if 255 - n*2 >= 0:
                img.set_alpha(255-n*2)
            else:
                img.set_alpha(0)
            a, b = self.display.get_size()
            x, y = img.get_size()
            self.display.blit(img, (a/2 - x/2, b/2 - y/2))
            self.display.blit(pygame.transform.scale(self.screen, self.resolution), (0, 0))
            pygame.display.flip()

            if n == 0:
                pygame.time.delay(1000)
                
            n+=1
            if n > 255:
                n = 255

        pygame.event.clear()

    def reset(self):

        with open("save.csv", "w", newline="") as csvfile:

            fieldnames = ["resolution", "volume", "record", "palier", "niveau"]
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

            info = pygame.display.Info()
            fullscreen = (info.current_w, info.current_h)

            writer.writeheader()
            writer.writerow({"resolution": fullscreen, "volume": 1, "record": self.game.record, "palier":0, "niveau":0})

        self.game.niveau = 0
        self.game.palier = 0
        self.game.record = 0
        self.game.creer_partie()
        
    def load(self):

        with open("save.csv", newline="") as csvfile:

            reader = csv.DictReader(csvfile)
            dico = {}

            for i in reader:

                dico["resolution"] = eval(i["resolution"])
                dico["volume"] = eval(i["volume"])
                dico["record"] = eval(i["record"])
                dico["palier"] = eval(i["palier"])
                dico["niveau"] = eval(i["niveau"])

            return dico

    def save(self):

        with open("save.csv", "w", newline="") as csvfile:

            fieldnames = ["resolution", "volume", "record", "palier", "niveau"]
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

            info = pygame.display.Info()
            fullscreen = (info.current_w, info.current_h)

            writer.writeheader()
            writer.writerow({"resolution": self.resolution, "volume": pygame.mixer.music.get_volume(), "record": self.game.record, "palier":self.game.palier, "niveau":self.game.niveau})
            

        
            
        
        
        
