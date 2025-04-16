import pygame


""" A Class for visible content """
class Sprite(pygame.sprite.Sprite):

    """ Initialization """
    def __init__(self, img, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.img = img
        self.rect = pygame.Rect(x, y, img.get_width(), img.get_height())

    """ Draw the sprite on the screen """
    def update(self, screen):
        
        screen.blit(self.draw(), self.rect)
        self.check_events()

    """ Check if the mouse is colliding with the sprite """
    def triggered(self):
        
        return self.rect.collidepoint(pygame.mouse.get_pos())

    """ Return the image we want to draw """
    def draw(self):

        return self.img

    """ Check all sprite's events """
    def check_events(self):

        pass
    
