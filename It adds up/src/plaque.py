from bouton import Bouton


class Number(int, Bouton):
    """ Un nombre """

    def __init__(self, value: int):
        """ Initialisation """

        super().__init__(str(value))
        self.value = value


class Operateur(Bouton):
    """ Un nombre """

    def __init__(self, value: str, original: bool = True):
        """ Initialisation """

        super().__init__(value)
        self.inial_value = value
        if value == "x":
            self.value = "*"
        elif value == "÷":
            self.value = "/"
        elif value == "^":
            self.value = "**"
        else:
            self.value = value

        self.original = original

    def __str__(self) -> str:
        """ Représentation textuelle """

        return self.value
