from util.Bouton import Bouton
from util.Sprite import Sprite
from util.Images import *
from util.Interface import *
from util.Events import *
from util.Slider import Slider

from Assets import Assets

from game.TaquinSudoku import *

import pygame
import game.taquin as t
import game.sudoku as s

""" The Maintitle """


class Maintitle(pygame.sprite.Sprite):
    DIFFICULTY = 0
    MODE = 0
    MARGIN = 5

    FONT = pygame.font.SysFont(None, 90, False)
    FONT2 = pygame.font.SysFont(None, 35, False)

    """ Initialization """
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.make_sprites()
        self.main_buttons = self.make_main_buttons()
        self.option_buttons = self.make_option_buttons()
        self.buttons = self.main_buttons

    """ Create visible contents """
    def make_sprites(self):

        self.sprites = pygame.sprite.Group()

        title = self.FONT.render("Taquin's Sudoku", True, (255, 255, 255))
        x, y = Interface.center(title)
        y = 80
        title = Sprite(title, x, y)

        x, y = Interface.center(Assets.MENU)
        y += 50
        menu = Sprite(Assets.MENU, x, y)

        x, y, w = 830, 185 + 50, 350
        taquin = t.Sprite.Sprite(t.Taquin.Taquin(), True, (x, y), w)
        sudoku = s.Sprite.Sprite(s.Sudoku.Sudoku(), False, w, y)

        self.sprites.add(menu, sudoku, title, taquin)

        x, y = 200, 625
        self.main_button = Bouton(Assets.MAIN, x, y, self.toggle, Assets.MAIN_HOVER)

    """ Create visible buttons """
    def make_main_buttons(self):

        group = pygame.sprite.Group()

        x, y = Interface.center(Assets.BUTTON)
        y -= 70
        self.modes = {
            0: Bouton(Assets.BUTTON, x, y, self.switchMode, Assets.BUTTON_HOVER, "Classic", police=35),
            1: Bouton(Assets.BUTTON, x, y, self.switchMode, Assets.BUTTON_HOVER, "Taquin", police=35),
            2: Bouton(Assets.BUTTON, x, y, self.switchMode, Assets.BUTTON_HOVER, "Sudoku", police=35)
        }

        y += self.MARGIN + Assets.BUTTON.get_height()
        self.difficulties = {
            0: Bouton(Assets.BUTTON, x, y, self.switchDifficulty, Assets.BUTTON_HOVER, "Easy", police=35),
            1: Bouton(Assets.BUTTON, x, y, self.switchDifficulty, Assets.BUTTON_HOVER, "Medium", police=35),
            2: Bouton(Assets.BUTTON, x, y, self.switchDifficulty, Assets.BUTTON_HOVER, "Hard", police=35)
        }

        self.difficulty_button = self.difficulties[self.DIFFICULTY]
        self.mode_button = self.modes[self.MODE]

        y += self.MARGIN + Assets.BUTTON.get_height()
        play_button = Bouton(Assets.BUTTON, x, y, self.toggle, Assets.BUTTON_HOVER, "Play", police=35)

        y += self.MARGIN + Assets.BUTTON.get_height()
        option_button = Bouton(Assets.BUTTON, x, y, self.toggle_options, Assets.BUTTON_HOVER, "Options", police=35)

        y += self.MARGIN + Assets.BUTTON.get_height()
        exit_button = Bouton(Assets.BUTTON, x, y, Events.quitter, Assets.BUTTON_HOVER, "Exit", police=35)

        group.add(option_button, exit_button, play_button)
        return group

    """ Create option buttons """
    def make_option_buttons(self):

        group = pygame.sprite.Group()

        x, y = Interface.center(Assets.BUTTON)
        y -= 20

        volume_text = self.FONT2.render("Volume", True, (255, 255, 255))
        volume_text = Sprite(volume_text, x + 14, y)

        y += Assets.BUTTON.get_height() - 20
        volume = Slider(x + 2, y, 120, Assets.set_volume)

        y += self.MARGIN + Assets.BUTTON.get_height()
        toggle_button = Bouton(Assets.BUTTON, x, y, Events.toggle_fullscreen, Assets.BUTTON_HOVER, "Fullscreen",
                               police=27)

        y += self.MARGIN + Assets.BUTTON.get_height()
        back_button = Bouton(Assets.BUTTON, x, y, self.toggle_main, Assets.BUTTON_HOVER, "Back", police=35)

        group.add(volume, volume_text, toggle_button, back_button)
        return group

    def toggle_main(self):
        self.buttons = self.main_buttons

    def toggle_options(self):
        self.buttons = self.option_buttons

    def new(self):

        Interface.clear()

        if self.MODE > 2:
            Interface.add(self)
            self.MODE -= 3
        elif self.MODE == 0:
            Interface.add(TaquinSudoku(3 + self.DIFFICULTY // 2, self.DIFFICULTY))
            self.MODE += 3
            Interface.add(self.main_button)
        elif self.MODE == 1:
            Interface.add(Taquin(self.DIFFICULTY + 3, self.DIFFICULTY))
            self.MODE += 3
            Interface.add(self.main_button)
        else:
            Interface.add(Sudoku(self.DIFFICULTY))
            self.MODE += 3
            Interface.add(self.main_button)

    def toggle(self):
        Interface.transition(self)

    def update(self, screen):

        self.sprites.update(screen)

        if self.buttons == self.main_buttons:
            self.difficulty_button.update(screen)
            self.mode_button.update(screen)

        self.buttons.update(screen)

    """ Switch the difficulty """
    def switchDifficulty(self):

        self.DIFFICULTY = (self.DIFFICULTY + 1) % 3
        self.difficulty_button = self.difficulties[self.DIFFICULTY]

    """ Switch the mode """
    def switchMode(self):

        self.MODE = (self.MODE + 1) % 3
        self.mode_button = self.modes[self.MODE]
