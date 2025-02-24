from manim import *
from triangle import Triangle


class Main(Scene):
    def construct(self):
        t = Triangle(self, 'A1', 'B1', 'C1')
        t.bisector('A1', 'B')
        t.median('A1', 'M')
        self.wait(1)
