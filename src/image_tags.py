from enum import Enum

from colorthief import ColorThief
from PIL import Image

class AspectRatio(Enum):
    NARROW        = 0.5
    SQUARE        = 1      # 1/1
    CLASSIC       = 1.33   # 4/3
    WIDE          = 1.78   # 16/9
    CINEMA        = 1.85   # 37/20
    ULTRAWIDE     = 2      # 2/1
    DOUBLE        = 3.56   # 32/9
    TRIPLE        = 5.34   # 48/9
    SUPERWIDE     = 7


class ImageTags:
    def __init__(self, img):
        self.__img = img

    @property
    def ratio(self):
        with Image.open(self.__img) as image:
            w, h = image.size
            aspect = w / h
            ratios = [ e.value for e in AspectRatio ]
            closest_ratio = min(ratios, key=lambda x:abs(aspect - x))
            return AspectRatio(closest_ratio).name.capitalize()
    
    @property
    def color(self):
        thief = ColorThief(self.__img)
        color = thief.get_color(quality=10)
        return color
