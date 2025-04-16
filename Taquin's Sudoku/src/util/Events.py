import pygame, sys


""" A Class for all Mouse/Keyboard Events """
class Events:

    lock = False
    key = None
    keys = []
    hover = 0    
    mouse = {"left": False,
             "right": False,
             "pos": (0, 0)}

    """ Toggle Fullscreen """
    @staticmethod
    def toggle_fullscreen():
        pygame.display.toggle_fullscreen()

    """ Delete all the current events """
    @staticmethod
    def clear():
        Events.mouse["left"] = False
        Events.mouse["right"] = False
        keys = pygame.key.get_pressed()
        Events.keys = keys
        Events.key = None
        Events.hover = 0

    """ Return True if we are left clicking, False instead """
    @staticmethod
    def mouse_button_downed():
        return pygame.mouse.get_pressed()[0]

    """ Return the position of the mouse on the screen """
    @staticmethod
    def mouse_pos():
        return pygame.mouse.get_pos()

    """ Stop all current and future events """
    @staticmethod
    def locked():
        Events.lock = True

    """ Consider all current and future events """
    @staticmethod
    def unlocked():
        Events.lock = False

    """ Stop the process """
    @staticmethod
    def quitter():
        pygame.quit()
        sys.exit()

    """ Return True if the key parameter is pressed """
    @staticmethod
    def keyPressed(key):
        return Events.keys[key]

    """ Update all event states """
    @staticmethod
    def update():

        Events.clear()

        if Events.lock: return

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                leftclick, midclick, rightclick = pygame.mouse.get_pressed()
                Events.mouse["left"] = leftclick
                Events.mouse["right"] = rightclick
                Events.mouse["pos"] = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                Events.quitter()

            if event.type == pygame.KEYDOWN:
                
                Events.key = event.key
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_F11]:
                    Events.toggle_fullscreen()
                if keys[pygame.K_LALT] and keys[pygame.K_F4]:
                    Events.quitter()

                
