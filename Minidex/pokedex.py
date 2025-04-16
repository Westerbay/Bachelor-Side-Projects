import random

from bs4 import BeautifulSoup

from pokemon import Pokemon
from text import Text
from saisi import Saisie
from bouton import Bouton

import pygame
import requests


def update_list_pokemon() -> None:
    """ Actualisation de la liste des pokemons """

    Saisie.pokemon_search.clear()
    for pokemon in Pokedex.all_pokemon:
        if Saisie.text.lower() in pokemon.lower():
            Saisie.pokemon_search.append(Pokedex.all_pokemon[pokemon])
    for i in range(len(Saisie.pokemon_search)):
        Saisie.pokemon_search[i].rect.x = 10
        Saisie.pokemon_search[i].rect.y = 60 + i * Saisie.pokemon_search[i].image.get_height()


class Pokedex:
    """ Pokedex """

    all_pokemon = {}

    def __init__(self, screen: pygame.Surface) -> None:
        """ Initialisation """

        self.screen = screen
        self.links = []
        self.load_gens()
        self.nb_gen = len(self.links)
        Pokemon.nb_gen = self.nb_gen
        self.sprites = pygame.sprite.Group()
        self.saisie = Saisie(self.screen)
        self.sprites.add(self.saisie)
        self.init = True

    def load_gens(self) -> None:
        """ Charge les générations """

        url = "https://www.pokepedia.fr/Catégorie:Pokémon_par_génération"
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")
            tds = soup.findAll('div')
            all_gens_div = [td for td in tds if "mw-category-group" in td.get_attribute_list("class")]
            for div in all_gens_div:
                a = div.find('a')
                link = a['href']
                self.links.append(link)

    def load_pokemons(self) -> None:
        """ Charge tout les pokemons """

        url = "https://www.pokepedia.fr" + self.links.pop()
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")
            tds = soup.findAll('li')
            tds = [td.find('a') for td in tds if td.findParent('div') is not None
                   and td.findParent('div').find('h3') is not None and
                   td.findParent('div').find('h3').text in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
            for td in tds:
                self.all_pokemon[td.text] = Bouton(td.text)

    def update(self) -> None:
        """ Affichage """

        if self.links:
            self.chargement()
        else:
            if self.init:
                update_list_pokemon()
                Pokemon.pokemons = self.all_pokemon.keys()
                pokemon = random.choice(list(self.all_pokemon.keys()))
                Saisie.name = pokemon
                Saisie.pokemon = Pokemon(self.screen, pokemon)
                self.init = False
            self.sprites.update()
            if self.saisie.pokemon.update():
                self.saisie.collision += 1
            if self.saisie.collision:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    def chargement(self) -> None:
        """ Chargement """

        pygame.draw.rect(self.screen, (0, 180, 0), (320, 300, (self.nb_gen-len(self.links)) * 80, 20), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (320, 300, (self.nb_gen-1) * 80, 20), 2, 10)
        self.screen.blit(Text.chargement, (640 - Text.chargement.get_width()/2, 340))
        self.load_pokemons()
