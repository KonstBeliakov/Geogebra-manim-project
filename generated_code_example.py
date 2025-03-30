from manim import *
from point import *
from segment import *
from utils import *

class MyScene(Scene):
    def construct(self):
        Point(self, 'A', 4.34, 2.6)
        Point(self, 'B', 7.52, 2.56)
        Point(self, 'C', 7.22, 0.18)
        Segment(self, 'A', 'C', 'f')
        midPoint(self, 'A', 'C', 'D')
        Point(self, 'E', 4.98, -1.38)
        Point(self, 'F', 5.76, 3.18)
        Segment(self, 'E', 'F', 'g')
        intersect_figures('f', 'g', 'G')
        Point(self, 'H', 12.58, 3.34)
        Point(self, 'I', 14.28, 1.74)
        Circle(self, 'H', 'I', 'c')
        Point(self, 'J', 15.36, -1.34)
        Point(self, 'K', 12.0, 1.74)
        Circle(self, 'J', 'K', 'd')
        intersect_figures('c', 'd', 'L', index=2)
        intersect_figures('c', 'd', 'M', index=1)
        Point(self, 'N', 1.14, 4.56)
        Circle(self, 'N', 2.5107767722360337, 'e')

        self.wait(1)
