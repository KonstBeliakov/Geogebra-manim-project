from manim import *
from utils import *


class Triangle:
    def __init__(self, p1=None, p2=None, p3=None):
        if p1 is None:
            p1 = rand_point()
        if p2 is None:
            p2 = rand_point()
        if p3 is None:
            p3 = rand_point()

        self.p1, self.p2, self.p3 = p1, p2, p3

    def render(self, scene):
        triangle = Polygon(tuple(self.p1), tuple(self.p2), tuple(self.p3), color=RED, fill_opacity=0.5)
        scene.play(Create(triangle))

        for p in self.p1, self.p2, self.p3:
            p.render(scene)
            scene.wait(0.5)
