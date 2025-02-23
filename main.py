from manim import *
import triangle
import point


class Main(Scene):
    def construct(self):
        A = point.Point(self, 0, 0, name='A')
        B = point.Point(self, 2, 0, name='B')
        C = point.Point(self, 0, 2, name='C')

        t = triangle.Triangle(self, A, B, C)
        t.median('A', 'D')

        A.move(1, 1)
        self.wait(2)
