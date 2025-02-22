from manim import *
from triangle import Triangle


class Main(Scene):
    def construct(self):
        t = Triangle(scene=self, point_names=('A', 'B', 'C'))
        t.print_points()
        t.median('A', 'D')
        self.wait(5)
