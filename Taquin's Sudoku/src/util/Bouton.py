from util.Events import *
from util.Sprite import *
from util.Images import *


""" A Class for making buttons easier """
class Bouton(Sprite):

    """ Initialization """
    def __init__(self, img, x, y, action = lambda : None,
                 img_hover = None, text = "", color = (255, 255, 255),
                 police = 40, font = None):
        
        Sprite.__init__(self, img.copy(), x, y)

        self.font = pygame.font.SysFont(font, police, False)
        self.action = action
        
        if img_hover is not None:
            self.img_hover = img_hover.copy()
        else:
            self.img_hover = img
            
        self.text = self.createText(text, color)
        self.textPos = Images.center(self.text, self.img)
        self.img.blit(self.text, self.textPos)
        self.img_hover.blit(self.text, self.textPos)

    """ The main function which will be called every frame """
    def update(self, screen):

        if self.triggered():
            screen.blit(self.img_hover, self.rect)
            Events.hover += 1
        else:
            Sprite.update(self, screen)
        
        self.checkEvents()

    """ Call the referred action of the button by clicking on it """
    def checkEvents(self):
        if Events.mouse["left"] and self.triggered():
            self.action()

    """ Overwrite a text on the image if there is a text parameter on the initialization """
    def createText(self, text, color):        
        return self.font.render(text, True, color)
