from PIL import Image
import numpy as np

from src.aliases import *


def dominant_color(image: Image.Image, palette_size: int = 16) -> RGBColor:
    image.thumbnail((100, 100))
    paletted = image.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    palette = paletted.getpalette()
    color_list = sorted(paletted.getcolors(), reverse=True)
    color_index = color_list[0][1]
    if palette is None:
        raise TypeError # ! Description
    dominant_color = palette[color_index * 3:color_index * 3 + 3]
    return RGBColor(*dominant_color)


def average_color(image: Image.Image) -> RGBColor:
    image_array = np.array(image)
    return RGBColor(*map(round, np.mean(image_array, axis=(0, 1))))
