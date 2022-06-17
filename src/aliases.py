# pyright: reportWildcardImportFromLibrary=false

from typing import *


class RGBColor(NamedTuple):
    r: int
    g: int
    b: int


class RGBAColor(NamedTuple):
    r: int
    g: int
    b: int
    a: float


class Point(NamedTuple):
    x: float
    y: float


class BoundBox(NamedTuple):
    t_l: Point
    b_r: Point


class Sizes(NamedTuple):
    w: int
    h: int


AVERAGE = Literal["AVERAGE"]
DOMINANT = Literal["DOMINANT"]

__ELLIPSE = Literal["ELLIPSE"]
__RECTANGLE = Literal["RECTANGLE"]

ShapeTypes = Union[__ELLIPSE, __RECTANGLE]
