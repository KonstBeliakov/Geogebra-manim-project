from manim import *
from triangle import Triangle
import point
from utils import *


class Main(Scene):
    def construct(self):
        init(scene=self)

        triangle('ABC')

        median('ABC', "BM")
        bisector('ABC', 'BD')

        points(('E', -1, -1), ('F', 1, 1), ('G', -1, 1), ('I', 1, -1), 'U')

        intersect('EF', 'GI', 'X')
