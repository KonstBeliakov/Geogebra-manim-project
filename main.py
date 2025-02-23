from manim import *
from point import Point
from segment import Segment


class Main(Scene):
    def construct(self):
        A = Point(self, 'A', 0, 0)
        Point(self, 'B', 1, 1)

        # We can create a segment using existing points or their names
        s1 = Segment(self, A, 'B')

        # If points are not specified, they will be generated randomly
        s2 = Segment(self)

        self.wait(1)
