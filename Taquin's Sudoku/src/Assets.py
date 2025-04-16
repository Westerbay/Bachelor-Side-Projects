from util.Images import *

import pygame, os


""" All Assets data """
class Assets:

    taquin = os.listdir("assets/images/taquin")
    taquin = ["taquin/" + i for i in taquin]
    BUTTON = Images.rescale(Images.load("empty_button.png"), 4)
    BUTTON_HOVER = Images.rescale(Images.load("empty_hover.png"), 4)
    BACKGROUND = Images.rescaleWidth(Images.load("background.png"), 1280)
    BUTTON_SMALL = Images.rescale(Images.load("empty_small_button.png"), 4)
    BUTTON_SMALL_HOVER = Images.rescale(Images.load("empty_small_hover.png"), 4)
    TICK = Images.rescale(Images.load("correct.png"), 50)
    MENU = Images.rescale(Images.load("menu.png"), 6)

    MAIN = Images.rescale(Images.load("home.png"), 4)
    MAIN_HOVER = Images.rescale(Images.load("home_hover.png"), 4)

    MUSIC = "assets/sound/Arabesque.wav"
    
    SOUNDS = {"correct": pygame.mixer.Sound("assets/sound/correct.wav")}
    VOLUMES = {"correct": 0.06}
    
    SOUNDS["correct"].set_volume(0.06)

    """ The main function of volume settings """
    @staticmethod
    def set_volume(a):
        pygame.mixer.music.set_volume(a)
        for i in Assets.SOUNDS:
            Assets.SOUNDS[i].set_volume(Assets.VOLUMES[i] * a)
            
