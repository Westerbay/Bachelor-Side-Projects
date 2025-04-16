from bs4 import BeautifulSoup
from urllib.request import urlopen
from text import *
from bouton import rondusButton, Bouton

import requests
import io


class Pokemon(pygame.sprite.Sprite):
    """ Classe Pokemon """

    exception = "pikachu évoli darumacho wimessir"
    pokemons = []
    events = None
    hover = 0
    nb_gen = 0
    soup = None

    def __init__(self, screen: pygame.Surface, name: str) -> None:
        """ Initialisation """

        super().__init__()
        self.boutons = pygame.sprite.Group()
        self.name = name
        self.infos = self.load()
        self.version = list(self.infos['localisations'].keys())
        self.index = 0
        self.image = self.create_board()
        self.loc = self.impress_loc()
        self.rect = self.image.get_rect()
        self.screen = screen
        if self.infos['stats']:
            self.boutons.add(rondusButton(">", 845, 520))
            self.boutons.add(rondusButton("<", 265, 520))
        else:
            self.boutons.add(rondusButton(">", 1035, 520))
            self.boutons.add(rondusButton("<", 455, 520))

    def localisation(self, soup: BeautifulSoup, dico: dict, gen: int = 0) -> None:
        """ Localisations """

        if gen:
            url = "https://www.pokepedia.fr/" + self.name.replace(" ", "_") + f"/Génération_{gen}"
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, features="html.parser")

        if 'Méga-' not in self.name:
            tds = soup.findAll('th')
            tds = [td for td in tds if td.text == 'Localisations']
            trs = [td.findParent('tr').findParent('tbody').findAll('tr') for td in tds]
            for t in trs:
                t.pop(0)
            version = ""
            for t in trs:
                for tr in t:
                    tds = tr.findAll('td')
                    for td in tds:
                        if td.has_key('rowspan') and td.text != '[+]':
                            version = str(td.text).replace("\xa0: ", " ")
                            dico['localisations'][version] = list()
                        else:
                            for a in td.findAll('a'):
                                text = str(a.text)
                                if text in self.pokemons:
                                    text = Text.obtain + text
                                dico['localisations'][version].append(text)
            for d in dico['localisations']:
                if not dico['localisations'][d]:
                    dico['localisations'][d].append(Text.indis)

    def load(self) -> dict:
        """ Charge les informations du pokemons """

        dico = {}
        url = "https://www.pokepedia.fr/" + self.name.replace(" ", "_")
        response = requests.get(url)

        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")
            self.soup = soup

            # Image
            td = soup.find('td', {'class': 'illustration'})
            img = td.find('img')
            url_image = "https://www.pokepedia.fr" + img['src']
            image_str = urlopen(url_image).read()
            image_file = io.BytesIO(image_str)
            image = pygame.image.load(image_file).convert_alpha()
            if image.get_width() > image.get_height():
                image = pygame.transform.scale(image, (250, 250 * image.get_height() / image.get_width()))
            else:
                image = pygame.transform.scale(image, (250 * image.get_width() / image.get_height(), 250))
            dico['image'] = image

            # Type
            td = soup.find('a', {'title': 'Type'})
            dico['types'] = []
            if td:
                if td.findParent('tr').find('td'):
                    types = td.findParent('tr').find('td').findAll('a')
                else:
                    types = td.findParent('tr').findNext('tr').find('td').findAll('a')
                for t in types:
                    url_image = "https://www.pokepedia.fr" + t.find('img')['src']
                    image_str = urlopen(url_image).read()
                    image_file = io.BytesIO(image_str)
                    image = pygame.image.load(image_file).convert_alpha()
                    image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
                    dico['types'].append(image)

            # Stats
            if self.name.lower() in self.exception:
                tds = soup.findAll('a', {'title': 'Statistique'})
                for _ in range(7):
                    tds.pop()
            else:
                tds = soup.findAll('a', {'title': 'Statistique'})
            dico2 = {}
            if len(tds) > 6:
                if tds[-1] == tds[-2]:
                    tds.pop()
                tds = [tds.pop() for _ in range(7)]
                stats = [td.findParent('tr') for td in tds if td.findParent('tr') is not None]
                for stat in stats:
                    if len(stat.findAll('td')) > 1:
                        dico2[stat.find('a').text] = str(int(stat.findAll('td')[1].text))
            dico['stats'] = dico2

            # Localisation
            dico['localisations'] = {}
            self.localisation(soup, dico)

            # Talents
            dico['talent'] = list()
            if dico['localisations'] or dico['stats']:
                tds = soup.findAll('a', {'title': 'Talent'})
                for td in tds:
                    if td.findParent('span') is not None:
                        tds = td.findParent('span')
                        break
                tds = tds.findParent('h3')
                talents = tds.findNext('ul').findAll('li')
                talents = [td.find('a') for td in talents]
                if None in talents:
                    talents = [Text.notalent]
                else:
                    talents = [td.text for td in talents]
                dico['talent'] = talents

        return dico

    def create_board(self) -> pygame.Surface:
        """ Renvoie le board """

        surface = pygame.Surface((1030, 720))
        surface.fill((240, 240, 240))

        if self.infos['stats'] != dict():

            # Gen
            surface.blit(Text.gen, (820 - Text.gen.get_width() / 2, 150))
            for i in range(1, self.nb_gen + 1):
                bouton = Bouton(str(i), (0, 0, 0))
                bouton.rect.x = 1140 - self.nb_gen * 20 + i * 20
                bouton.rect.y = 200
                self.boutons.add(bouton)

            # Pokemon
            surface.blit(self.infos['image'], (80, 60))
            name = Text.font.render(self.name, True, (0, 0, 0))
            surface.blit(name, (360, 140))

            # Type(s)
            for i in range(len(self.infos['types'])):
                surface.blit(self.infos['types'][i], (360 + i * 150, 190))

            # Stats
            width, height = 300, 380
            tableau = pygame.Surface((width, height))
            tableau.fill((240, 240, 240))
            pygame.draw.rect(tableau, (255, 94, 77), (0, 0, width, 50), border_radius=10)
            pygame.draw.rect(tableau, (0, 0, 0), (0, 0, width, 50), 4, 10)
            pygame.draw.rect(tableau, (0, 0, 0), (0, 0, width, height), 4, 10)
            tableau.blit(Text.statistiques, (width / 2 - Text.statistiques.get_width() / 2, 10))
            higher = max(map(int, list(self.infos['stats'].values())))

            def create_rect(value: str) -> pygame.Surface:
                """ Renvoie une surface """
                if not value.isdigit():
                    return pygame.Surface((1, 1))
                value = int(value)
                s = pygame.Surface((125, 20))
                s.fill((240, 240, 240))
                if value < 75:
                    color = (220, 20, 60)
                elif value < 100:
                    color = (255, 165, 0)
                else:
                    color = (46, 139, 87)
                if higher < 126:
                    pygame.draw.rect(s, color, (0, 0, value, 20))
                    pygame.draw.rect(s, (0, 0, 0), (0, 0, value, 20), 2)
                else:
                    pygame.draw.rect(s, color, (0, 0, value / higher * 125, 20))
                    pygame.draw.rect(s, (0, 0, 0), (0, 0, value / higher * 125, 20), 2)
                return s

            tableau.blit(Text.pv, (15, 70))
            tableau.blit(make_surface(self.infos['stats']['PV']), (90, 70))
            tableau.blit(create_rect(self.infos['stats']['PV']), (160, 78))
            tableau.blit(Text.atk, (15, 120))
            tableau.blit(make_surface(self.infos['stats']['Attaque']), (90, 120))
            tableau.blit(create_rect(self.infos['stats']['Attaque']), (160, 128))
            tableau.blit(Text.defense, (15, 170))
            tableau.blit(make_surface(self.infos['stats']['Défense']), (90, 170))
            tableau.blit(create_rect(self.infos['stats']['Défense']), (160, 178))
            tableau.blit(Text.spa, (15, 220))
            tableau.blit(make_surface(self.infos['stats']['Attaque Spéciale']), (90, 220))
            tableau.blit(create_rect(self.infos['stats']['Attaque Spéciale']), (160, 228))
            tableau.blit(Text.spd, (15, 270))
            tableau.blit(make_surface(self.infos['stats']['Défense Spéciale']), (90, 270))
            tableau.blit(create_rect(self.infos['stats']['Défense Spéciale']), (160, 278))
            tableau.blit(Text.spe, (15, 320))
            tableau.blit(make_surface(self.infos['stats']['Vitesse']), (90, 320))
            tableau.blit(create_rect(self.infos['stats']['Vitesse']), (160, 328))

            surface.blit(tableau, (670, 270))  # Position stats

            # Talent
            text = ""
            for i in self.infos['talent']:
                text += i + "  "
            text = make_surface(text, size=25)
            surface.blit(text, (350 - text.get_width() / 2, 350))

        else:

            # Pokemon
            name = Text.font.render(self.name, True, (0, 0, 0))
            width = self.infos['image'].get_width() + name.get_width()
            height = self.infos['image'].get_height()
            pos_x = surface.get_width() / 2 - width / 2
            pos_y = surface.get_height() / 2 - height / 2 - 100
            surface.blit(self.infos['image'], (pos_x, pos_y))
            surface.blit(name, (pos_x + self.infos['image'].get_width() + 10, pos_y + 40))

            # Type(s)
            for i in range(len(self.infos['types'])):
                surface.blit(self.infos['types'][i],
                             (pos_x + self.infos['image'].get_width() + 10 + i * 150, pos_y + 90))

        return surface

    def impress_loc(self) -> pygame.Surface or None:
        """ Imprime les localisations """

        if self.version:
            width, height = 500, 225
            tableau = pygame.Surface((width, height))
            tableau.fill((240, 240, 240))
            pygame.draw.rect(tableau, (0, 0, 0), (0, 0, 120, height), 4, 10)
            pygame.draw.rect(tableau, (120, 120, 255), (0, 0, width, 50), border_radius=10)
            pygame.draw.rect(tableau, (0, 0, 0), (0, 0, width, 50), 4, 10)
            pygame.draw.rect(tableau, (0, 0, 0), (0, 0, width, height), 4, 10)
            tableau.blit(Text.localisation, (width / 2 - Text.localisation.get_width() / 2, 10))
            text = make_version(self.version[self.index])
            tableau.blit(text, (60 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 25))
            localisations = make_local(list(self.infos['localisations'][self.version[self.index]]))
            tableau.blit(localisations,
                         (320 - localisations.get_width() / 2, height / 2 - localisations.get_height() / 2 + 25))

            return tableau

    def update(self) -> bool:
        """ Affichage """

        self.hover = 0
        if self.loc is not None:
            if self.infos['stats'] != dict():
                self.image.blit(self.loc, (80, 425))
            else:
                self.image.blit(self.loc, (270, 425))
        self.screen.blit(self.image, (250, 0))
        self.screen.blit(Text.source, (self.screen.get_width() - Text.source.get_width() - 20, 10))
        if self.loc is not None:
            self.boutons.draw(self.screen)
        for bouton in self.boutons:
            if bouton.rect.collidepoint(pygame.mouse.get_pos()):
                self.hover += 1
                if pygame.MOUSEBUTTONDOWN in self.events and pygame.mouse.get_pressed()[0]:
                    if bouton.name == '>':
                        self.index += 1
                        if self.index == len(self.version):
                            self.index = 0
                        self.loc = self.impress_loc()
                    elif bouton.name == '<':
                        self.index -= 1
                        if self.index == -1:
                            self.index = len(self.version) - 1
                        self.loc = self.impress_loc()
                    elif bouton.name.isdigit():
                        self.infos['localisations'] = dict()
                        self.index = 0
                        self.localisation(self.soup, self.infos, int(bouton.name))
                        self.version = list(self.infos['localisations'].keys())
                        self.loc = self.impress_loc()
                return True
