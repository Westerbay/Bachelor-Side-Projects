from util.Sprite import Sprite
from util.Events import Events
from util.Color import Color

import pygame

""" A Class for a Slider """


class Slider(Sprite):
    HEIGHT = 30
    HEIGHT_LINE = HEIGHT // 4
    GRAY = Color.make_gray(100)
    GREY = Color.make_gray(200)
    Y = (HEIGHT - HEIGHT_LINE) // 2

    """ Initialization """

    def __init__(self, x, y, width, action=lambda x: None):

        Sprite.__init__(self, self.create_base(width), x, y)
        self.width = width
        self.action = action
        self.pos = width

    def check_events(self):

        if self.triggered():
            Events.hover += 1

            if Events.mouse_button_downed():
                self.pos = Events.mouse_pos()[0] - self.rect.x
                self.action(self.pos / self.width)

    def create_base(self, width):

        base = pygame.Surface((width, self.HEIGHT))
        base.set_colorkey(Color.BLACK)
        pygame.draw.rect(base, self.GRAY, (0, self.Y, width, self.HEIGHT_LINE))
        return base

    def draw(self):

        base = self.img.copy()
        pygame.draw.rect(base, Color.WHITE, (0, self.Y, self.pos, self.HEIGHT_LINE))
        pygame.draw.rect(base, self.GREY, (self.cursor_x(), 0, self.HEIGHT // 3, self.HEIGHT))
        return base

    def cursor_x(self):

        x = self.pos - self.HEIGHT // 6
        maxi, mini = self.width - self.HEIGHT // 3, 0
        if x > maxi:
            return maxi
        elif x < mini:
            return mini
        return x
