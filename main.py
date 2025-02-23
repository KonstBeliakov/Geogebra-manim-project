from manim import *
from triangle import Triangle
from point import Point
from segment import Segment


class Main(Scene):
    def construct(self):
        A = Point(self, 0, 0, name='A')
        B = Point(self, 2, 0, name='B')
        C = Point(self, 0, 2, name='C')

        t = Triangle(self, A, B, C)
        D = t.median('A', 'D')

        E = Point(self, 2, 3, name='E')
        t2 = Triangle(self, 'A', D, 'E')

        A.move(2, 2)

        CE = Segment(self, 'C', 'E')

        self.wait(2)
