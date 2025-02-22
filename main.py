from manim import *
from triangle import Triangle


class Main(Scene):
    def construct(self):
        t = Triangle(scene=self, point_names=('A', 'B', 'C'))
        t.render()
        t.printPoints()
        t.median('A', 'D')
        self.wait(5)
