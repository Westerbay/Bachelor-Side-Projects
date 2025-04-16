from assets import Image, Font, scale
import pygame


def create_button(image: pygame.Surface, text: str, default: bool = True) -> pygame.Surface:
    """ Creation de l'image du bouton """

    surface = image.copy()
    if default is None:
        text = Font.default_font3.render(text, False, (255, 255, 255))
    elif default:
        text = Font.default_font.render(text, False, (255, 255, 255))
    else:
        text = Font.default_font2.render(text, False, (255, 255, 255))
    a, b = image.get_size()
    c, d = text.get_size()
    surface.blit(image, (0, 0))
    surface.blit(text, (a/2 - c/2, b/2 - d/2 - 2))
    return surface.convert_alpha()


class Bouton(pygame.sprite.Sprite):
    """ On définit un bouton """

    def __init__(self, text: str = "", x: int = 0, y: int = 0):
        """ Initialisation """

        super().__init__()
        self.image = create_button(Image.bouton, text)
        self.hover = create_button(Image.bouton_hover, text)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.is_hover = False
        self.used = False

    def update(self, screen: pygame.Surface) -> None:
        """ Affichage """

        if self.is_hover:
            screen.blit(self.hover, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def set_pos(self, x: int, y: int) -> None:
        """ Actualise les positions """

        self.rect.x = x
        self.rect.y = y


class BoutonMenu(Bouton):
    """ Bouton du menu """

    def __init__(self, text: str = "", x: int = 0, y: int = 0, default: bool or None = False):
        """ Initialisation """

        super().__init__(text, x, y)
        self.image = create_button(scale(Image.bouton, 1.5), text, default)
        self.hover = create_button(scale(Image.bouton_hover, 1.5), text, default)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class BoutonPredef(Bouton):
    """ Bouton prédéfinit """

    def __init__(self, image: pygame.surface.Surface, hover: pygame.surface.Surface):
        """ Initialisation """

        super().__init__()
        self.image = image.convert_alpha()
        self.hover = hover.convert_alpha()
        self.rect = self.image.get_rect()
