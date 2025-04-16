from text import Text
from pokemon import Pokemon

import pygame


class Saisie(pygame.sprite.Sprite):
    """ Zone de saisie """

    text = ""
    longueur, hauteur = 250, 720
    pokemon_search = []
    collision = 0
    events = []
    pokemon = None
    name = None

    def __init__(self, screen: pygame.surface) -> None:
        """ Initialisation """

        super().__init__()
        self.surface = pygame.Surface((self.longueur, self.hauteur))
        self.screen = screen
        self.saisie_rect = pygame.Rect(0, 0, self.longueur, 50)
        self.hidden = 0

    def update(self) -> None:
        """ Affichage """

        self.collision = 0
        self.surface.fill((60, 60, 60))
        pygame.draw.rect(self.surface, (150, 150, 150), self.saisie_rect, 2)
        pygame.draw.rect(self.surface, (150, 150, 150), self.surface.get_rect(), 2)
        text = Text.font.render(self.text, True, (255, 255, 255))
        self.curseur(text)
        self.surface.blit(text, (10, 8))
        for pokemon in self.pokemon_search:
            if 40 < pokemon.rect.y < 680:
                self.surface.blit(pokemon.image, pokemon.rect)
                if pokemon.rect.collidepoint(pygame.mouse.get_pos()):
                    self.collision += 1
                    if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:
                        self.name = pokemon.text
                        self.pokemon = Pokemon(self.screen, pokemon.text)
        self.screen.blit(self.surface, (0, 0))

    def curseur(self, text: pygame.Surface) -> None:
        """ Actualisation du curseur """

        if int(self.hidden) == 2:
            self.hidden = 0
        if int(self.hidden) % 2:
            pygame.draw.rect(self.surface, (255, 255, 255), (text.get_width() + 12, 8, 2, text.get_height()))
        self.hidden += 0.05

    @staticmethod
    def scroll_down() -> None:
        """ Scroll vers le bas """

        if Saisie.pokemon_search and Saisie.pokemon_search[-1].rect.y > 680:
            for pokemon in Saisie.pokemon_search:
                pokemon.rect.y -= pokemon.image.get_height()

    @staticmethod
    def scroll_up() -> None:
        """ Scroll vers le bas """

        if Saisie.pokemon_search and Saisie.pokemon_search[0].rect.y < 40:
            for pokemon in Saisie.pokemon_search:
                pokemon.rect.y += pokemon.image.get_height()
