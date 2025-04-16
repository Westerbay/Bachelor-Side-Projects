import random, pygame

class Grille(list):

    RES = 32

    def __init__(self, taille):

        super().__init__()
        self.taille = taille
        self.cases = self.choisir_nb_cases(random.randint(1, self.taille**2))
        for i in range(taille):
            self.append([0 if (i,j) not in self.cases else 1 for j in range(taille)])

        self.surface = pygame.Surface((self.RES * taille, self.RES * taille))
        self.hidden = pygame.image.load("assets/images/0.png").convert()
        self.visible = pygame.image.load("assets/images/1.png").convert()
        self.hidden_animation = [pygame.transform.scale(self.hidden, (self.RES/i, self.RES)) for i in range(1, 4)] + [pygame.transform.scale(self.visible, (self.RES/(4-i), self.RES)) for i in range(1, 4)]
        self.visible_animation = [pygame.transform.scale(self.visible, (self.RES/i, self.RES)) for i in range(1, 4)] + [pygame.transform.scale(self.hidden, (self.RES/(4-i), self.RES)) for i in range(1, 4)]
        self.index = 0
        self.actualisation()

    def __repr__(self):

        for i in range(len(self)):
            for j in range(len(self)):
                print(self[i][j], end="")
            print()

        return ""

    def toutes_les_cases(self):

        return [(i, j) for i in range(self.taille) for j in range(self.taille)]

    def choisir_nb_cases(self, nb):

        if nb < self.taille/2:
            liste = self.toutes_les_cases()
            return [liste.pop(random.randint(0, len(liste)-1)) for _ in range(nb)]
        return [random.choice(self.toutes_les_cases()) for _ in range(nb)]

    def cases_proches(self, pos):

        x, y = pos
        toutes_cases_proches = [(x+i-1, y+j-1) for i in range(3) for j in range(3)]
        return [pos for pos in toutes_cases_proches if pos in self.toutes_les_cases()]

    def interchange(self, pos):

        for i,j in self.cases_proches(pos):
            self[i][j] = (self[i][j]+1)%2
            
        self.actualisation()

    def interchange_liste(self, liste):

        for i,j in liste: self.interchange((i, j))

    def copier(self):

        copy_grille = Grille(self.taille)
        for i,j in self.toutes_les_cases():
            copy_grille[i][j] = self[i][j]
        return copy_grille

    def actualisation(self):
        
        self.index = 0

        for i,j in self.toutes_les_cases():

            if self[i][j] == 1:

                self.surface.blit(self.visible, (i*self.RES, j*self.RES))

            else:

                self.surface.blit(self.hidden, (i*self.RES, j*self.RES))

    def animation(self, case, vel=0.2):
        
        self.surface = pygame.Surface((self.RES * self.taille, self.RES * self.taille))
        self.surface.fill((0, 0, 1))
        self.surface.set_colorkey((0, 0, 1))

        self.index += vel

        cases_proches = self.cases_proches(case)

        for i,j in self.toutes_les_cases():

            if (i, j) in cases_proches:

                x, y = self.visible_animation[int(self.index%6)].get_size()
                
                if self[i][j] == 1:

                    self.surface.blit(self.visible_animation[int(self.index%6)], (i*self.RES + (32 - x)/2, j*self.RES))

                else:

                    self.surface.blit(self.hidden_animation[int(self.index%6)], (i*self.RES + (32 - x)/2, j*self.RES))
            
            else:

                if self[i][j] == 1:

                    self.surface.blit(self.visible, (i*self.RES, j*self.RES))

                else:

                    self.surface.blit(self.hidden, (i*self.RES, j*self.RES))

        if self.index >= 5:

            return True
        
        return False
                

