""" A Dataclass for colors in form of tuples """
class Color:

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)

    """ Create a shade of grey """
    @staticmethod
    def make_gray(value):
        return (value, value, value)
