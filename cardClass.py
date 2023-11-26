from cmu_graphics import *
from PIL import Image

class Card:
    def __init__(self, number, suite, image):
        self.number = number
        self.suite = suite
        self.image = CMUImage(Image.open('image'))
