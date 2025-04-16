from plaque import *
from random import randint, choice


def pick_number(nombre: int, plaquette: list) -> int:
    """ Choix du nombre """

    plaquette.remove(nombre)
    return nombre


def enleve_operateurs(operateurs: list, liste: list) -> None:
    """ Enleve un operateur de la liste """

    for operateur in operateurs:
        if operateur in liste:
            liste.remove(operateur)


def liste_operations_possibles(a: int, b: int, limite: int = 2000) -> list:
    """ Renvoie la liste des opérations possibles entre deux nombres """

    liste = ["+", "-", "*"]
    if b != 0:
        liste.append("%")
        if a / b == a // b:
            liste.append("/")
    if a != 0 or b != 0:
        if b > 0:
            liste.append("**")
    liste2 = liste.copy()
    for op in liste2:
        if abs(operation(a, op, b)) > limite:
            enleve_operateurs([op], liste)

    return liste


def choix_pertinant(a: int, b: int) -> list:
    """ Renvoie la liste des meilleurs opérations possibles entre deux nombres """

    liste = liste_operations_possibles(a, b)

    if a == 0 or b == 0:
        enleve_operateurs(["+", "-", "*", "/", "%"], liste)
    if a == 1 or b == 1:
        enleve_operateurs(["*", "/", "%", "**"], liste)
    if a < b:
        enleve_operateurs(["%"], liste)

    return liste


def operation(a: int, o: str, b: int) -> int:
    """ Renvoie l'operation entre deux nombres avec l'opérateur o """

    return int(eval(f"{a} {o} {b}"))


class Partie:
    """ Une partie """

    liste_nombres = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 25, 50, 75, 100]
    operateur = ["+", "-", "*", "/", "%", "**"]

    def __init__(self, difficulty: int = 0):
        """ Initialisation """

        self.liste_plaques = [Number(value) for value in self.liste_nombres]
        self.plaquettes = [self.liste_plaques.pop(randint(0, len(self.liste_plaques) - 1)) for _ in range(6)]
        self.difficulty = difficulty + 3
        self.nb_find, path = 0, ""
        self.limite = 2000
        while not (99 < self.nb_find < 1000) or self.nb_find in self.liste_nombres:
            self.nb_find, self.path = self.create()

    def create(self) -> (Number, str):
        """ Création du nombre à trouver """

        plaquettes = self.plaquettes.copy()
        nombres_choisis = [pick_number(choice(plaquettes), plaquettes) for _ in range(self.difficulty + 1)]
        path = ""
        for _ in range(self.difficulty):
            a = pick_number(choice(nombres_choisis), nombres_choisis)
            b = pick_number(choice(nombres_choisis), nombres_choisis)
            if not choix_pertinant(a, b):  # On évite une erreur avec choice sur une empty liste
                return 0, ""
            o = choice(choix_pertinant(a, b))
            nombre = Number(operation(a, o, b))
            path += f"{a} {o} {b} = {nombre},"
            nombres_choisis.append(nombre)
        return nombres_choisis[0], path
