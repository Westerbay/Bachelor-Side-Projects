from util.Grille import *

import random


""" Class for a Taquin's game """
class Taquin:

    ITERATIONS = {0: 5,
                  1: 7,
                  2: 10}

    def __init__(self, taille = 3, difficulty = 1):
        
        self.taille = taille
        self.difficulty = difficulty
        self.soluce = [] #Solution

        #See the shuffle method
        self.iteration = self.ITERATIONS[difficulty]

        self.allCases = Grille.generateCasesCarres(self.taille) #Positions of all cells
        self.posZero = self.allCases[random.choice(
            [0, self.taille - 1, -1, -self.taille])] #Position of the empty cell

        self.origin = self.generateGrille(taille) #Final state grid
        self.grille = self.generateGrille(taille) #First state grid

        while self.solved(): self.shuffle()
        self.grilleRestart = Grille.copy(self.grille) #In state of restart, we save the first state
        self.posZeroRestart = self.posZero
        self.soluceRestart = self.soluce.copy()
        #print(self.generateGoodSoluce())

    def new(self):
        self.__init__(self.taille, self.difficulty)

    """ Return an initialized grid """
    def generateGrille(self, n):
        grille = [[i + 1 + n * j for i in range(n)] for j in range(n)]
        i, j = self.posZero
        grille [i][j] = 0
        return grille
    
	
    """ Shuffle the grid """
    def shuffle(self):
        self.soluce.append(self.posZero)
        for _ in range(self.iteration ** (self.taille - 1) + 1): 
            coup = random.choice(self.coupsPossibles())
            self.move(coup)
	
	
    """ Return True if the game ended, false instead """
    def solved(self):
        return self.grille == self.origin


    """ Return a list of all possible moves """
    def coupsPossibles(self):
        i, j = self.posZero
        voisins = [(i-1, j), (i+1, j), (i, j+1), (i, j-1)]
        return [i for i in voisins if i in self.allCases]
	
	
    """ Move a cell """
    def move(self, pos):
        if pos in self.coupsPossibles():
            self.soluce.append(pos)
            i, j = pos
            k, l = self.posZero
            self.grille[i][j], self.grille[k][l] = self.grille[k][l], self.grille[i][j]
            self.posZero = pos

    def moveGrille(self, pos, posZero, grille):
        i, j = pos
        k, l = posZero
        grille[i][j], grille[k][l] = grille[k][l], grille[i][j]
        return pos
            

    """ Restart """
    def restart(self):
        self.grille = Grille.copy(self.grilleRestart)
        self.posZero = self.posZeroRestart
        self.soluce = self.soluceRestart.copy()
    

    """ Withdraw useless moves from self.soluce """
    def generateGoodSoluce(self):
        
        copySoluce, grille = self.soluce.copy(), Grille.copy(self.grille)
        copySoluce.pop()
        copySoluce.reverse()
        
        soluce, grilles = [], {str(Grille.copy(grille)): []}
        posZero = self.posZero
        
        for coup in copySoluce:
            posZero = self.moveGrille(coup, posZero, grille)
            soluce.append(coup)
            if str(grille) in grilles:
                soluce = grilles[str(grille)].copy()
            else:
                grilles[str(Grille.copy(grille))] = soluce.copy()

        return soluce
	
	
    """ String representation """
    def __repr__(self):
        repr = ""
        for ligne in self.grille:
            repr += str(ligne) + "\n"
        return repr

    
