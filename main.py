from manim import *
from point import Point, get_point_by_name
from segment import Segment


class Main(Scene):
    def construct(self):
        Point(self, 'A', 0, 0)
        Point(self, 'B', 2, 2)

        Point(self, 'C', 2, 0)
        Point(self, 'D', 0, 2)

        s1 = Segment(self, 'A', 'B')
        s2 = Segment(self, 'C', 'D')

        X = s1.intersect(s2, 'X')

        get_point_by_name('A').move(0, 1.0)

        self.wait(1)
