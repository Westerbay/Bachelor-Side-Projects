import pygame

""" A Class for a Timer """


class Timer(pygame.sprite.Sprite):

    """ Initialization"""
    def __init__(self, x, y, font=None, color=(255, 255, 255), police=85):

        pygame.sprite.Sprite.__init__(self)
        self.initTime = pygame.time.get_ticks()
        self.time = (0, 0)
        self.pos = (x, y)
        self.font = pygame.font.SysFont(font, police, False)
        self.color = color
        self.stop = False

    """ Draw the timer on the screen """
    def update(self, screen):

        if not self.stop:
            self.time = self.getTime()

        time = "Too long" if self.time[0] > 60 else self.timeToStr(self.time)
        time = self.font.render(time, True, self.color)
        screen.blit(time, self.pos)

    """ Return a couple of the time with (minute, second) """
    def getTime(self):

        time = (pygame.time.get_ticks() - self.initTime) // 1000
        return time // 60, time % 60

    """ Convert a time in couple to the string representation """
    def timeToStr(self, time):

        m, s = time

        if m < 10:
            m = "0" + str(m)
        else:
            m = str(m)

        if s < 10:
            s = "0" + str(s)
        else:
            s = str(s)

        return m + " : " + s
