import pygame

class Hand:

    """ Mains """

    def __init__(self, x, y):

        """ Initialisation """

        self.x = x
        self.y = y
        self.initial_y = y
        self.image = pygame.image.load("../assets/images/hand.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.vel = -1

    def update(self, screen):

        """ Affichage """

        screen.blit(self.image, (self.x, self.y))
        self.y += self.vel * 0.7
        if self.y >= self.initial_y + 10:
            self.vel *= -1
        elif self.y <= self.initial_y - 10:
            self.vel *= -1

class Button(pygame.sprite.Sprite):
    """ Les boutons """

    resolution = (120, 56)

    def __init__(self, name, x, y):

        """ Initialisation """

        super().__init__()
        self.image = pygame.image.load("../assets/images/boutons/empty_button.png").convert_alpha()
        self.hover = pygame.image.load("../assets/images/boutons/empty_hover.png").convert_alpha()
        self.font = pygame.font.Font("../assets/font/font.ttf", 32)
        self.name = self.font.render(name, False, (255, 255, 255))
        pos = self.center(self.name.get_size(), self.resolution)
        self.image = pygame.transform.scale(self.image, self.resolution)
        self.hover = pygame.transform.scale(self.hover, self.resolution)
        self.image.blit(self.name, pos)
        self.hover.blit(self.name, pos)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_hover = False

    def update(self, screen):

        """ Affichage """

        if not self.is_hover:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.hover, self.rect)

    def center(self, size1, size2):

        """ Renvoie le centre entre 2 sizes """

        x, y = size1
        a, b = size2

        return a / 2 - x / 2, b / 2 - y / 2 - 5

class Button_preload(Button):

    """ Bouton avec image prédéfini """

    def __init__(self, image, hover, pos):

        """ Initialisation """

        x, y = pos
        super().__init__("", x, y)
        self.image = image
        if hover is None:
            self.hover = image
        else:
            self.hover = hover
        self.rect.width, self.rect.height = self.image.get_size()

class Menu_Button(Button):

    """ Bouton avec image prédéfini """

    def __init__(self, name, x, y):

        """ Initialisation """

        super().__init__(name, x, y)
        self.image = pygame.transform.scale(self.image, (180, 84))
        self.hover = pygame.transform.scale(self.hover, (180, 84))
        self.rect.x, self.rect.y = x, y
        self.rect.width, self.rect.height = self.image.get_size()


class Desc(pygame.sprite.Sprite):

    """ Sprite d'une description """

    screensize = (1280, 720)

    def __init__(self, description, x=0, y=0):

        """ Initialisation """

        super().__init__()
        font = pygame.font.Font("../assets/font/font.ttf", 40)
        desc = font.render(description, False, (255, 255, 255))
        a, b = desc.get_size()
        image = pygame.Surface((a + 60, b + 20))
        image.fill((47, 49, 54))
        self.rect = image.get_rect()
        pygame.draw.rect(image, (32, 34, 37), self.rect, 6)
        pos = self.center(desc.get_size(), image.get_size())
        image.blit(desc, pos)
        self.image = image
        if x or y:
            self.rect.x, self.rect.y = x, y
        else:
            self.rect.x, self.rect.y = self.center(self.image.get_size(), self.screensize)

    def update(self, screen):
        """ Affichage """

        screen.blit(self.image, self.rect)

    def center(self, size1, size2):
        """ Renvoie le centre entre 2 sizes """

        x, y = size1
        a, b = size2

        return a / 2 - x / 2, b / 2 - y / 2 - 5


class Brawler_Sprite(pygame.sprite.Sprite):

    """ Sprite du brawler """

    dep = 0
    vel = 1
    time = 0
    time2 = 0
    animation = False
    affiche_stats = True

    def __init__(self, brawler):

        """ Initialisation """

        super().__init__()
        self.power = brawler.power
        self.challenger = brawler.challenger
        self.ancient_power = self.power
        self.type = brawler.type
        self.image = brawler.image
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font("../assets/font/font.ttf", 100)
        self.power_img = self.font.render(str(self.ancient_power), False, (255, 255, 255))
        self.name = brawler.name
        self.sound_power_up = pygame.mixer.Sound("../assets/sounds/power_up.wav")
        self.icon = brawler.card_icon

    def update_data(self):

        """ Actualise les données """

        self.pos_power_x = 640 / 2 - self.power_img.get_size()[0] / 2
        if self.rect.x > 500:
            self.pos_power_x += 780
        else:
            self.pos_power_x -= 140

        self.fight_power_y = 360 / 2 - self.power_img.get_size()[1] / 2 + 360

    def update(self, screen):

        """ Affichage """

        screen.blit(self.image, self.rect)

        self.update_stats(screen)

        if not (self.time % 5):
            self.move()
            self.time = 0
        self.time += 1

    def move(self):

        """ Déplacement """

        if self.vel > 0:
            self.rect.y -= self.vel
            self.dep += self.vel
            if self.dep >= 10:
                self.vel = - 1
        else:
            self.rect.y -= self.vel
            self.dep += self.vel
            if self.dep < 0:
                self.vel = 1

    def update_stats(self, screen):

        """ Affiche les statistiques """

        pos_power_y = self.rect.y - self.power_img.get_size()[1] + 40
        if self.name in "Harpy Blue Dragon Orkgre Sea Octopus Chimera Book Master":
            pos_power_y = 620 - self.dep

        if self.ancient_power != self.power:

            if self.power > self.ancient_power:
                self.ancient_power += 1
                power_up = "+"
                power_up = self.font.render(power_up, False, (0, 255, 0))
            else:
                self.ancient_power -= 1
                power_up = "-"
                power_up = self.font.render(power_up, False, (255, 0, 0))

            self.power_img = self.font.render(str(self.ancient_power), False, (255, 255, 255))
            self.animation = True

            if self.affiche_stats:
                self.sound_power_up.play()
                screen.blit(power_up, (self.pos_power_x + self.power_img.get_size()[0], pos_power_y))

        else:
            self.power_up = ""
            self.time2 += 1

        if self.time2 > 120 and self.power == self.ancient_power:
            self.animation = False
            self.time2 = 0

        if self.affiche_stats:
            screen.blit(self.power_img, (self.pos_power_x, pos_power_y))
