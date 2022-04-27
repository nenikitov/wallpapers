from enum import Enum
import re

import fast_colorthief as fc
from PIL import Image

class AspectRatio(Enum):
    NARROW     = 0.5
    SQUARE     = 1      # 1/1
    CLASSIC    = 1.33   # 4/3
    WIDE       = 1.78   # 16/9
    CINEMATIC  = 1.85   # 37/20
    IMAX       = 1.9    # 19/10
    ULTRAWIDE  = 2.33   # 21/9
    DOUBLE     = 3.56   # 32/9
    TRIPLE     = 5.34   # 48/9
    SUPERWIDE  = 7


class ImageTags:
    def __init__(self, img, csv):
        self.__img = img
        self.__csv = csv


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
        color = fc.get_dominant_color(self.__img, quality=1)
        return color

    @property
    def name(self):
        return ImageTags.__split_camel(self.__csv['name'])

    @property
    def style(self):
        return self.__csv['style'].capitalize()

    @property
    def note(self):
        return self.__csv['note']

    @property
    def link(self):
        return self.__csv['link']


    def __split_camel(text):
        return ' '.join(re.sub('([A-Z0-9][a-z]+)', r' \1', re.sub('([A-Z0-9]+)', r' \1', text)).split())