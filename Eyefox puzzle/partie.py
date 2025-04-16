from grille import Grille
from sprite import Fox
import pygame

class Partie(pygame.sprite.Sprite):

    def __init__(self, palier, niveau):
        
        super().__init__()
        self.vie = 3
        self.coup = palier//3 + 1
        if self.coup > 2 and niveau % 10 != 9:
            self.coup = palier//4
        self.nb_coup = self.coup
        self.create_grille(palier % 3 + 4)
        self.choix = []
        self.niveau = niveau
        self.palier = palier

        self.vie_img = pygame.transform.scale(pygame.image.load("assets/images/heart.png"), (32, 32)).convert_alpha()
        self.star = pygame.image.load("assets/images/star.png").convert_alpha()
        self.empty_star = pygame.image.load("assets/images/empty_star.png").convert_alpha()
        self.star_rect = self.star.get_rect()
        self.star2 = pygame.transform.scale(self.star, (self.star_rect.width*1.5, self.star_rect.height*1.5))
        self.star = pygame.transform.scale(self.star, (self.star_rect.width*0.5, self.star_rect.height*0.5))
        self.empty_star = pygame.transform.scale(self.empty_star, (self.star_rect.width*0.5, self.star_rect.height*0.5))
        self.chiffres = self.get_chiffres()
        self.cadre = pygame.image.load("assets/images/cadre.png").convert()
        self.arrow = pygame.transform.scale(pygame.image.load("assets/images/arrow.png"), (64, 64)).convert_alpha()

        if palier < 3:
            fox = Fox("sleep")
        elif palier < 6:
            fox = Fox("awake")
        else:
            fox = Fox("stand")

        self.sprites = pygame.sprite.Group()
        self.sprites.add(fox)

    def create_grille(self, taille):

        self.original_grille = Grille(taille)
        self.modified_grille = self.original_grille.copier()
        self.solution = self.modified_grille.choisir_nb_cases(self.nb_coup)
        self.modified_grille.interchange_liste(self.solution)
        

    def jouer(self, pos):

        self.modified_grille.interchange(pos)
        self.choix.append(pos)
        self.nb_coup -= 1

    def win(self):

        if self.modified_grille == self.original_grille:
            return True

        return False

    def update(self, screen, pos):
        
        a, b = screen.get_size()
        x, y = self.original_grille.surface.get_size()
        res = self.original_grille.RES

        screen.blit(self.cadre, (a/2 - self.cadre.get_size()[0]/2, b/2 - self.cadre.get_size()[1]/2))
        screen.blit(self.arrow, (a/2 - self.arrow.get_size()[0]/2, b/2 - self.arrow.get_size()[1]/2 + 10))
        o = 0
        for i in str(self.nb_coup):
            screen.blit(pygame.transform.scale(self.chiffres[int(i)], (self.chiffres[int(i)].get_size()[0]*1.5, self.chiffres[int(i)].get_size()[1]*1.5)),
                        (a/2-5 + o*self.chiffres[int(i)].get_size()[0]*1.5 - (len(str(self.nb_coup))-1)*self.chiffres[int(i)].get_size()[0]*0.5, b/2 - self.arrow.get_size()[1]/2))
            o+=1
        
        screen.blit(self.original_grille.surface, (a/2-res-x, b/2-y/2))
        screen.blit(self.modified_grille.surface, (a/2+res, b/2-y/2))

        rect = pygame.Rect(a/2+res, b/2-y/2,self.modified_grille.surface.get_size()[0],
                self.modified_grille.surface.get_size()[1])
        
        if rect.collidepoint(pos) or pygame.Rect(612, 0, 28, 28).collidepoint(pos):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        for i in range(self.vie): screen.blit(self.vie_img, (570, b-res - i * res - 100 - i*20))

        self.sprites.update(screen)
        
        screen.blit(self.star2, (10, 280))
        
        if self.palier != 0:
            a = 0
            for i in str(self.palier*10):
                screen.blit(self.chiffres[int(i)], (36+a - (len(str(self.palier*10))-2)*self.chiffres[int(i)].get_size()[0]*0.5, 307))
                a += 10
                
        for i in range(10):
            screen.blit(self.empty_star, (34, 240 - i * 20))
        
        for i in range(self.niveau):
            screen.blit(self.star, (34, 240 - i * 20))

    def get_pos(self, pos):

        a, b = (640, 360)
        x, y = self.original_grille.surface.get_size()
        res = self.original_grille.RES

        x1, y1 = pos
        x1 -= a/2+res
        y1 -= b/2-y/2

        if (x1//res, y1//res) in self.modified_grille.toutes_les_cases():

            return (int(x1//res), int(y1//res))

        return False

    def get_chiffres(self):

        liste = [pygame.image.load(f"assets/images/chiffres/{i}.png") for i in range(10)]
        return [i.convert_alpha() for i in liste]

        
        

