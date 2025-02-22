from manim import *


class Segment:
    def __init__(self, scene, p1=None, p2=None, point_names=(None, None)):
        self.scene = scene

        if p1 is None:
            p1 = Point(scene, name=point_names[0])
        if p2 is None:
            p2 = Point(scene, name=point_names[1])

        self.p1 = p1
        self.p2 = p2

    def render(self):
        line = Line(tuple(self.p1), tuple(self.p2), color=RED)
        self.scene.play(Create(line))
        self.p1.render()
        self.p2.render()
