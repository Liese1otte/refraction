from PIL import Image, ImageDraw
from abc import ABC, abstractmethod

from src.aliases import *


# * Config tuple types.

# ? perhaps it is best to ditch config objects
# ? because then all params are explicitly defined
# ? in inits


class ShapeConfig(NamedTuple):
    # For shapes.
    type_: ShapeTypes
    bdbox: BoundBox
    angle: Union[int, None]
    color: RGBAColor
    

class CanvasConfig(NamedTuple):
    # For canvas.
    shape_factories: Tuple[Callable[[ShapeConfig], "Shape"]]  # TODO: the funny
    background_type: Union[DOMINANT, AVERAGE]
    generative_seed: Union[int, None]


# * Geometric data types.


class Shape(ABC):
    """Shape data type interface.
    All custom shapes should inherit from this class.
    
    Methods:
        append_shape (self -> None): method required to draw the
        desired shape of this object's canvas. Refer to method's
        documentation for more details.
    """
    
    @abstractmethod
    def __init__(self, config: ShapeConfig) -> None:
        """Shape constructor.

        Args:
            config (ShapeConfig): tuple of shape's parameters
        """
        self.type_ = config.type_
        self.bdbox = config.bdbox
        self.angle = config.angle
        self.color = config.color
        self.__post_init__()
    
    def __post_init__(self) -> None:
        # Mainly on init calculations.
        w = self.bdbox.b_r.x - self.bdbox.t_l.x
        h = self.bdbox.b_r.y - self.bdbox.t_l.y
        if not isinstance(w, int):
            raise TypeError(SIZES_NOT_INT)
        if not isinstance(h, int):
            raise TypeError(SIZES_NOT_INT)
        self.sizes  = Sizes(w, h)
        self.center = Point(w / 2, h / 2)
        self.image  = Image.new(mode="RGBA", size=self.sizes, color=self.color)
        self.drawer = ImageDraw.Draw(self.image)
        self.draw_shape()
        del self.drawer
        self._rotate_shape()
    
    @abstractmethod
    def draw_shape(self) -> None:
        """Method called on init to draw the desired shape.
        Use `self.drawer` to do so and `self.sizes` to get info on the
        size limits.
        """
        ...
    
    def _rotate_shape(self) -> None:
        # Rotates shape image.
        if self.angle is None: return
        self.image = self.image.rotate(self.angle)
        angled_box = self.image.getbbox()
        if angled_box is None:
            raise TypeError(NO_ANGLED_BOX)
        w = angled_box[2] - angled_box[0]
        h = angled_box[3] - angled_box[1]
        self.sizes = Sizes(w, h)
        t_l = Point(self.center.x - w / 2, self.center.y - h / 2)
        b_r = Point(self.center.x + w / 2, self.center.y + h / 2)
        self.bdbox = BoundBox(t_l, b_r)


class Ellipse(Shape):
    """Ellipse-type shape."""
    
    def __init__(self, config: ShapeConfig) -> None:
        super().__init__(config)
    
    def draw_shape(self) -> None:
        self.drawer.ellipse((0, 0, *self.sizes))


def ellipse_factory(box: BoundBox, angle: int, color: RGBAColor) -> Ellipse:
    """Factory for Ellipse objects.

    Args:
        box (BoundBox): upper left and bottom right coordinates
        angle (int): angle of rotation in degrees
        color (RGBAColor): shape's filling color

    Returns:
        Ellipse: desired object
    """
    
    config = ShapeConfig("ELLIPSE", box, angle, color)
    return Ellipse(config)


class Rectangle(Shape):
    """Rectangle-type shape."""
    
    def __init__(self, config: ShapeConfig) -> None:
        super().__init__(config)
    
    def draw_shape(self) -> None:
        self.drawer.rectangle((0, 0, *self.sizes))


def rectangle_factory(box: BoundBox, angle: int, color: RGBAColor) -> Rectangle:
    """Factory for Rectangle objects.

    Args:
        box (BoundBox): upper left and bottom right coordinates
        angle (int): angle of rotation in degrees
        color (RGBAColor): shape's filling color

    Returns:
        Rectangle: desired object
    """
    
    config = ShapeConfig("RECTANGLE", box, angle, color)
    return Rectangle(config)


NO_ANGLED_BOX = "Shape's bounding box is None because it's size is equal to 0x0 after rotation."
SIZES_NOT_INT = "Shape's dimensions are floats, expected int."