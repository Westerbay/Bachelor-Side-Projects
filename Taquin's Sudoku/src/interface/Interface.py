from util.Bouton import Bouton

import util.Interface as window
import pygame

""" The main Screen """


class Interface(window.Interface):

    RESOL = (1280, 720)
    TITLE = "Taquin's Sudoku"

    """ Initialization"""
    def __init__(self):
        window.Interface.__init__(self, self.RESOL, self.TITLE)

        from Assets import Assets

        self.set_background(Assets.BACKGROUND)

        from interface.Maintitle import Maintitle

        self.maintitle = Maintitle()
        self.add(self.maintitle)

        pygame.mixer.music.load(Assets.MUSIC)
        pygame.mixer.music.play(-1)

        self.run()
