from manim import *
from utils import *


class Triangle:
    def __init__(self, scene, p1=None, p2=None, p3=None, point_names=(None, None, None)):
        self.scene = scene
        if p1 is None:
            p1 = Point(scene, name=point_names[0])
        if p2 is None:
            p2 = Point(scene, name=point_names[1])
        if p3 is None:
            p3 = Point(scene, name=point_names[2])

        self.p1, self.p2, self.p3 = p1, p2, p3

    def median(self, point_name, median_point_name=None):
        if all([p.name != point_name for p in (self.p1, self.p2, self.p3)]):
            raise ValueError(f"There is no vertex {point_name} in the triangle {self}")

        t = []
        for p in self.p1, self.p2, self.p3:
            if p.name != point_name:
                t.append(p)

        mid1 = midPoint(self.scene, t[0], t[1], name=median_point_name)
        print(f'median: {mid1.name} {mid1.x} {mid1.y}')
        mid1.render()

        mid2 = None
        for p in self.p1, self.p2, self.p3:
            if p.name == point_name:
                mid2 = p

        #segment = Segment(mid1, mid2)

    def render(self):
        triangle = Polygon(tuple(self.p1), tuple(self.p2), tuple(self.p3), color=RED, fill_opacity=0.5)
        self.scene.play(Create(triangle))

        for p in self.p1, self.p2, self.p3:
            p.render()
            self.scene.wait(0.5)

    def __repr__(self):
        return f'{self.p1.name}{self.p2.name}{self.p3.name}'

    def printPoints(self):
        for p in self.p1, self.p2, self.p3:
            print(f'{p.name} {p.x} {p.y}')
