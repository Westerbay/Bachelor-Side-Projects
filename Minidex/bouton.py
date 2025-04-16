from text import Text

import pygame


class Bouton(pygame.sprite.Sprite):
    """ Classe Bouton """

    def __init__(self, text: str, color: tuple = (255, 255, 255)) -> None:
        """ Initialisation """

        super().__init__()
        self.text = text
        self.image = Text.font_small.render(self.text, True, color)
        self.rect = self.image.get_rect()
        self.name = text


class rondusButton(pygame.sprite.Sprite):
    """ Class bouton angle arrondi """

    def __init__(self, text: str, x: int = 0, y: int = 0):
        """ Initialisation """

        super().__init__()
        self.text = text
        self.text = Text.font.render(self.text, True, (255, 255, 255))
        self.image = pygame.Surface((50, 50))
        self.image.fill((240, 240, 240))
        pygame.draw.rect(self.image, (120, 120, 120), (0, 0, 50, 50), border_radius=5)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 50, 50), 2, 5)
        self.image.blit(self.text, (25 - self.text.get_width() / 2, 25 - self.text.get_height() / 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = text
