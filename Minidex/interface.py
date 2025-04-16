from pokedex import Pokedex
from saisi import Saisie
from pokemon import Pokemon
from text import Text

import sys
import pygame
import io


def quitter() -> None:
    """ Quitter python"""

    Interface.running = False
    pygame.quit()
    sys.exit()


def handle_input() -> None:
    """ Gestion des touches """

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LALT] and keys[pygame.K_F4]:
        quitter()


def update_list_pokemon() -> None:
    """ Actualisation de la liste des pokemons """

    Saisie.pokemon_search.clear()
    for pokemon in Pokedex.all_pokemon:
        if Saisie.text.lower() in pokemon.lower():
            Saisie.pokemon_search.append(Pokedex.all_pokemon[pokemon])
    for i in range(len(Saisie.pokemon_search)):
        Saisie.pokemon_search[i].rect.x = 10
        Saisie.pokemon_search[i].rect.y = 60 + i * Saisie.pokemon_search[i].image.get_height()


class Interface:
    """ Notre interface """

    pygame.init()
    fullscreen = pygame.display.Info().current_w, pygame.display.Info().current_h
    running = True

    def __init__(self) -> None:
        """ Initialisation """

        resol = 1280, 720
        self.screen = pygame.display.set_mode(resol)
        pygame.display.set_caption('Minidex')
        self.pokedex = Pokedex(self.screen)
        icon = pygame.image.load(io.BytesIO(Text.img)).convert_alpha()
        pygame.display.set_icon(icon)

    def run(self) -> None:
        """ Lancement de l'interface """

        clock = pygame.time.Clock()
        while True:

            clock.tick(30)  # 30 FPS
            events = pygame.event.get()
            handle_input()

            for event in events:
                if event.type == pygame.QUIT:
                    quitter()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        Saisie.text = Saisie.text[:-1]
                    else:
                        Saisie.text += event.unicode
                    update_list_pokemon()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        Saisie.scroll_up()
                    elif event.button == 5:
                        Saisie.scroll_down()

            Saisie.events = [event.type for event in events]
            Pokemon.events = Saisie.events
            self.screen.fill((240, 240, 240))
            self.update()
            pygame.display.flip()

    def update(self) -> None:
        """ Actualisation """

        self.pokedex.update()
