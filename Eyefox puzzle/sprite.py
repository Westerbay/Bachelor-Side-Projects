import pygame

class Fox(pygame.sprite.Sprite):

    def __init__(self, standing, x=550, y=280):

        super().__init__()
        self.fox_sleep = self.get_images("sleeping", 6)
        self.fox_stand = self.get_images("stand", 5)
        self.fox_awake = self.get_images("awake", 5)
        self.images = eval(f"self.fox_{standing}")
        self.index = 0
        self.vel = 0.2
        self.x = x
        self.y = y

    def get_images(self, name, nb):

        liste = [pygame.image.load(f"assets/images/fox/{name}{i}.png") for i in range(1, nb+1)]
        x, y = liste[0].get_size()
        return [pygame.transform.scale(i, (x*4, y*4)).convert_alpha() for i in liste]

    def update(self, screen):

        screen.blit(self.images[int(self.index % len(self.images))], (self.x, self.y))
        self.index += self.vel
        if self.index >= len(self.images):
            self.index = 0
