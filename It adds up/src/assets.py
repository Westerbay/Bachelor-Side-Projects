import os
import pygame


def load_image(name: str, classe: str) -> pygame.Surface:
    """ Charge une image """

    path = os.path.join("assets", "images", classe, name+".png")
    return pygame.image.load(path)


def load_sound(name: str) -> pygame.mixer.Sound:
    """ Charge un son """

    path = os.path.join("assets", "sounds", name)
    return pygame.mixer.Sound(path)


def set_volume(volume: float) -> None:
    """ Règle le volume """

    pygame.mixer.music.set_volume(volume)
    for sound in Sound.all_sounds:
        if sound == Sound.roll:
            sound.set_volume(volume*0.05)
        elif sound == Sound.plaque:
            sound.set_volume(volume * 0.3)
        else:
            sound.set_volume(volume * 0.2)


def scale(img: pygame.Surface, x: float) -> pygame.Surface:
    """ Scale * x"""

    a, b = img.get_size()
    return pygame.transform.scale(img, (a*x, b*x))


class Font:
    """ Gestion des polices d'écriture """

    default_font = pygame.font.SysFont("helvetica", 24)
    title_font = pygame.font.SysFont("helvetica", 40)
    default_font2 = pygame.font.SysFont("helvetica", 20)
    default_font3 = pygame.font.SysFont("helvetica", 14)


class Image:
    """ Gestion des images """

    # Empty buttons
    bouton = load_image("bouton", "bouton")
    bouton = pygame.transform.scale(bouton, (30 * 2, 14 * 2))
    bouton_hover = load_image("bouton_hover", "bouton")
    bouton_hover = pygame.transform.scale(bouton_hover, (30 * 2, 14 * 2))

    # Buttons
    size = (14 * 2, 14 * 2)
    retour = load_image("retour", "bouton")
    retour = pygame.transform.scale(retour, size)
    retour_hover = load_image("retour_hover", "bouton")
    retour_hover = pygame.transform.scale(retour_hover, size)
    suivant = load_image("suivant", "bouton")
    suivant = pygame.transform.scale(suivant, size)
    suivant_hover = load_image("suivant_hover", "bouton")
    suivant_hover = pygame.transform.scale(suivant_hover, size)
    home = load_image("home", "bouton")
    home = pygame.transform.scale(home, size)
    home_hover = load_image("home_hover", "bouton")
    home_hover = pygame.transform.scale(home_hover, size)
    valider = load_image("valider", "bouton")
    valider = pygame.transform.scale(valider, size)
    valider_hover = load_image("valider_hover", "bouton")
    valider_hover = pygame.transform.scale(valider_hover, size)

    # Game
    clock = load_image("clock", "game")
    correct = load_image("correct", "game")
    x, y = correct.get_size()
    correct = pygame.transform.scale(correct, (x * 20, y * 20))
    false = load_image("false", "game")
    false = pygame.transform.scale(false, (x * 20, y * 20))

    # Maintitle
    menu = load_image("menu", "maintitle")
    menu = scale(menu, 3)
    sound_bar = load_image("sound_bar", "maintitle")
    curseur = load_image("curseur", "maintitle")
    sound_bar = scale(sound_bar, 3)
    curseur = scale(curseur, 3)
    icon = load_image("icon", "maintitle")


class Sound:
    """ Sound """

    roll = load_sound("roll.wav")
    roll.set_volume(0.05)
    plaque = load_sound("plaque.wav")
    plaque.set_volume(0.3)
    time = load_sound("time.wav")
    time.set_volume(0.2)
    correct = load_sound("correct.wav")
    false = load_sound("wrong.wav")
    correct.set_volume(0.2)
    false.set_volume(0.2)
    all_sounds = [roll, plaque, time, correct, false]
