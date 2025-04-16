import pygame

class Type:

    """ Cette class gère la table des types """

    def __init__(self, type):

        """ Initialisation"""

        self.type = type
        self.image = self.get_image()

    def __eq__(self, type):

        """ Test d'égalité """

        return self.type == type

    def get_image(self):

        """ Retourne l'image du type """

        return pygame.image.load(f"../assets/images/type/{self.type}.png").convert_alpha()

    def est_fort_contre(self, type):

        """ Cette méthode retourne quel type est le plus fort"""

        if self.type == "fire" and (type == "ice" or type == "forest"):

            return True

        elif self.type == "aqua" and type == "fire":

            return True

        elif self.type == "forest" and type == "aqua":

            return True

        elif self.type == "ice" and type == "ventus":

            return True

        elif self.type == "ventus" and type == "fire":

            return True

        return False

    def __repr__(self):

        """ Représentation """

        return self.type

    def get_color(self):

        """ Retourne la couleur associée au type """

        if self.type == "aqua":

            return (34, 60, 255)

        elif self.type == "darkus":

            return (20, 20, 20)

        elif self.type == "fire":

            return (217, 47, 55)

        elif self.type == "forest":

            return (31, 168, 79)

        elif self.type == "ice":

            return (128, 128, 255)

        elif self.type == "light":

            return (255, 255, 255)

        elif self.type == "ventus":

            return (128, 255, 128)