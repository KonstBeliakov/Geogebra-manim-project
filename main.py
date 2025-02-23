from manim import *
from triangle import Triangle
import point


class Main(Scene):
    def construct(self):
        A = point.Point(self, 0, 0, name='A')
        B = point.Point(self, name='B')
        C = point.Point(self, name='C')
        E = point.Point(self, name='E')

        t = Triangle(self, A, B, C)
        t2 = Triangle(self, A, B, E)

        t.median('A', 'D')
        A.move(1, 1)


        self.wait(5)
