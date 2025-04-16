from util.Grille import *

import random


class Sudoku:

    NUMBERS = set(range(1, 10))
    PROBS = {0: 40,
             1: 55,
             2: 70}

    def __init__(self, difficulty = 1):

        self.difficulty = difficulty
        self.proba_hidden = self.PROBS[difficulty]
        self.allCases = Grille.generateCasesCarres(9)
        
        self.grille = self.generateGrille()
        while not self.grille:
            self.grille = self.generateGrille()
            
        self.solve = Grille.copy(self.grille)
        self.shuffle()

    def new(self):
        self.__init__(self.difficulty)

    def generateGrille(self):
        grille = [[0 for _ in range(9)] for _ in range(9)]
        for i, j in self.allCases:
            choix = self.possibleNumbers((i, j), grille)
            if choix == []:
                return False #Erreur
            else:
                grille[i][j] = random.choice(choix)
        return grille

    def possibleNumbers(self, pos, grille):
        i, j = pos
        ligne = self.getLigne(i, grille)
        colonne = self.getColonne(j, grille)
        carre = self.getCarre(pos, grille)
        return list(self.NUMBERS - set(ligne + colonne + carre))

    def getColonne(self, a, grille):
        liste = []
        for i, j in self.allCases:
            if j == a:
                liste.append(grille[i][j])
        return liste

    def getLigne(self, a, grille):
        return grille[a]

    def getCarre(self, pos, grille):
        liste = []
        a, b = pos
        for i, j in self.allCases:
            if i // 3 == a // 3 and b // 3 == j // 3:
                liste.append(grille[i][j])
        return liste

    def shuffle(self):
        for i, j in random.sample(self.allCases, int(81*self.proba_hidden/100)):
            self.grille[i][j] = 0

    def solved(self):
        ok = True
        for i in range(9):
            ok = ok and set(self.getLigne(i, self.grille)) == self.NUMBERS
            ok = ok and set(self.getColonne(i, self.grille)) == self.NUMBERS
            ok = ok and set(self.getCarre((i//3, i%3), self.grille)) == self.NUMBERS
        return ok

    def __repr__(self):
        rep, nb = "", 0
        for i, j in self.allCases:
            num = self.grille[i][j]
            if num:
                rep += f"{num} "
            else:
                rep += "_ "
            nb += 1
            if not nb % 3:
                rep += " "
            if not nb % 9:
                rep += "\n"
            if not nb % 27:
                rep += "\n"

        return rep
            
        
    
