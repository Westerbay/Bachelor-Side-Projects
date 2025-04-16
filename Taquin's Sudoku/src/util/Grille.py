""" A Class for more utilities on grid """
class Grille:

    """ Copy grid """
    @staticmethod
    def copy(grille):
        return [grille[i].copy() for i in range(len(grille))]

    """ Generate cell coordinates """
    @staticmethod
    def generateCasesCarres(n):
        return [(i // n, i % n) for i in range(n**2)]
