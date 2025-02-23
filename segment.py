from manim import *
from point import *


class Segment:
    def __init__(self, scene, p1=None, p2=None):
        self.scene = scene

        if isinstance(p1, str) or p1 is None:
            p1 = get_point_or_random(scene, p1)
        if isinstance(p2, str) or p2 is None:
            p2 = get_point_or_random(scene, p2)

        self.p1 = p1
        self.p2 = p2

        self.render()

    def render(self):
        self.line = always_redraw(lambda: Line(tuple(self.p1), tuple(self.p2), color=RED))
        self.scene.play(Create(self.line))
