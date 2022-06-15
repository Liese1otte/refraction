from PIL import Image
from unittest import TestCase

from src.image import *


class ImageScriptTest(TestCase):
    def setUp(self) -> None:
        self.image = Image.open("refraction/tests/assets/Lucia.jpg")
    
    def test_dominant_color(self) -> None:
        output_color = dominant_color(self.image, 10)
        expected = RGBColor(139, 147, 150)
        self.assertEqual(output_color, expected)
    
    def test_average_color(self) -> None:
        output_color = average_color(self.image)
        expected = RGBColor(169, 159, 141)
        self.assertEqual(output_color, expected)

