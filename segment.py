from manim import *
from object import Object


class Segment(Object):
    def __init__(self, scene, p1=None, p2=None, point_names=(None, None)):
        super().__init__(scene)

        if p1 is None:
            p1 = Point(scene, name=point_names[0])
        if p2 is None:
            p2 = Point(scene, name=point_names[1])

        self.p1 = p1
        self.p2 = p2

        self.p1.add_dependent(self)
        self.p2.add_dependent(self)

        self.render()

    def render(self):
        self.line = Line(tuple(self.p1), tuple(self.p2), color=RED)
        self.scene.play(Create(self.line))
        self.p1.render()
        self.p2.render()

    def transform(self):
        line2 = Line(tuple(self.p1), tuple(self.p2), color=RED)
        self.scene.play(ReplacementTransform(self.line, line2))
        self.line = line2
