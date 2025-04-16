import pygame, os
        

""" A Class for all picture applicatives """
class Images:

    """ Return the centered position of a surface on another surface """
    @staticmethod
    def center(image, surface):
        x, y = image.get_size()
        a, b = surface.get_size()
        return (a - x) // 2, (b - y) // 2

    """ Load an image """
    @staticmethod
    def load(name):
        return pygame.image.load(os.path.join("assets/images", name)).convert_alpha()

    """ Rescale an image by multiplication """
    @staticmethod
    def rescale(img, coef):
        x, y = img.get_size()
        return pygame.transform.scale(img, (x * coef, y * coef))

    """ Rescale an image to the dimension parameter """
    @staticmethod
    def rescaleDim(img, dim):
        return pygame.transform.scale(img, dim)

    """ Rescale an image by the width """
    @staticmethod
    def rescaleWidth(img, width):
        return Images.rescale(img, width / img.get_width())

    """ Rescale an image by the Height """
    @staticmethod
    def rescaleHeight(img, height):
        return Images.rescale(img, height / img.get_height())

    """ Rescale an image to be squared """
    @staticmethod
    def scaleSquare(image, dim):
        
        width, height = image.get_size()

        if width == height:
            return pygame.transform.scale(image, (dim ,dim))

        elif width == dim or height == dim:
            im = pygame.Surface((dim, dim))
            if width > height:
                im.blit(image, ((dim-width)//2, 0))
            else:
                im.blit(image, (0, (dim-height)//2))
            return im
        
        elif width > height:
            im = pygame.transform.scale(image, (width*dim//height, dim))
            return Images.scaleSquare(im, dim)
        
        else:
            im = pygame.transform.scale(image, (dim, height*dim//width))
            return Images.scaleSquare(im, dim)
