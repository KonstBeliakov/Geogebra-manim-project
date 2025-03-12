import math

from manim import *
from utils import *
from segment import Segment
import circle
from point import *
from settings import *


class Triangle:
    def __init__(self, scene, p1=None, p2=None, p3=None):
        """
        :param scene: scene where to draw a triangle
        :param p1: Point instance or name of the point. (If there is no such point it will be created)
        :param p2: Point instance or name of the point. (If there is no such point it will be created)
        :param p3: Point instance or name of the point. (If there is no such point it will be created)
        """
        self.scene = scene

        if isinstance(p1, str) or p1 is None:
            p1 = get_point_or_random(scene, p1)
        if isinstance(p2, str) or p2 is None:
            p2 = get_point_or_random(scene, p2)
        if isinstance(p3, str) or p3 is None:
            p3 = get_point_or_random(scene, p3)

        self.p1, self.p2, self.p3 = p1, p2, p3

        self.render()

    def circumscribed_circle(self, point_name=None):
        """
        Drawing the circumscribes circle of the triangle
        :param point_name: optional name of the center of the circle
        :return: Circle -- circumscribed circle of the triangle
        """

        def get_circumscribed_center_position(triangle):
            x1, y1 = triangle.p1.x, triangle.p1.y
            x2, y2 = triangle.p2.x, triangle.p2.y
            x3, y3 = triangle.p3.x, triangle.p3.y

            D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

            if abs(D) < 1e-9:
                raise ValueError(
                    f"Triangle {triangle} is degenerate or the points are collinear - cannot define a circumscribed circle.")

            Ux = ((x1 ** 2 + y1 ** 2) * (y2 - y3) +
                  (x2 ** 2 + y2 ** 2) * (y3 - y1) +
                  (x3 ** 2 + y3 ** 2) * (y1 - y2)) / D

            Uy = ((x1 ** 2 + y1 ** 2) * (x3 - x2) +
                  (x2 ** 2 + y2 ** 2) * (x1 - x3) +
                  (x3 ** 2 + y3 ** 2) * (x2 - x1)) / D

            r = math.sqrt((x1 - Ux) ** 2 + (y1 - Uy) ** 2)

            return (Ux, Uy), r

        center = Point(self.scene, name=point_name, get_position=lambda: get_circumscribed_center_position(self))

        circ_circle = circle.Circle(self.scene, center, get_circumscribed_center_position(self)[1])

        return circ_circle

    def render(self):
        self.triangle = always_redraw(lambda: Polygon(tuple(self.p1), tuple(self.p2), tuple(self.p3),
                                                      color=LINES_COLOR,
                                                      fill_opacity=FIGURE_FILL_OPACITY))
        self.scene.play(Create(self.triangle))

    def __repr__(self):
        return f'{self.p1.name}{self.p2.name}{self.p3.name}'

    def print_points(self):
        for p in self.p1, self.p2, self.p3:
            print(f'{p.name} {p.x} {p.y}')
