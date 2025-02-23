from manim import *
from utils import *
from segment import Segment
from point import *


class Triangle:
    def __init__(self, scene, p1=None, p2=None, p3=None):
        self.scene = scene

        if isinstance(p1, str) or p1 is None:
            p1 = get_point_or_random(scene, p1)
        if isinstance(p2, str) or p2 is None:
            p2 = get_point_or_random(scene, p2)
        if isinstance(p3, str) or p3 is None:
            p3 = get_point_or_random(scene, p3)

        self.p1, self.p2, self.p3 = p1, p2, p3

        self.render()

    def median(self, point_name, median_point_name=None):
        if all([p.name != point_name for p in (self.p1, self.p2, self.p3)]):
            raise ValueError(f"There is no vertex {point_name} in the triangle {self}")

        t = []
        for p in self.p1, self.p2, self.p3:
            if p.name != point_name:
                t.append(p)

        mid1 = midPoint(self.scene, t[0], t[1], name=median_point_name)
        print(f'median: {mid1.name} {mid1.x} {mid1.y}')

        mid2 = None
        for p in self.p1, self.p2, self.p3:
            if p.name == point_name:
                mid2 = p

        Segment(self.scene, mid2, mid1)

        return mid1

    def render(self):
        self.triangle = always_redraw(lambda: Polygon(tuple(self.p1), tuple(self.p2), tuple(self.p3),
                                                      color=RED,
                                                      fill_opacity=0.3))
        self.scene.play(Create(self.triangle))

    def __repr__(self):
        return f'{self.p1.name}{self.p2.name}{self.p3.name}'

    def print_points(self):
        for p in self.p1, self.p2, self.p3:
            print(f'{p.name} {p.x} {p.y}')
