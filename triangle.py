import math

from manim import *
from utils import *
from segment import Segment
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

    def median(self, point_name, median_point_name=None):
        """
        Draw a median in the triangle
        :param point_name: name of the vertex from which we want to draw a median
        :param median_point_name: name of the intersection point of the median with the side (to be created)
        :return: intersection point of the median with the side
        """
        vertices = [self.p1, self.p2, self.p3]

        vertex = None
        for p in self.p1, self.p2, self.p3:
            if p.name == point_name:
                vertex = p
        if vertex is None:
            raise ValueError(f"There is no vertex {point_name} in the triangle {self}")

        side_vertices = [p for p in vertices if p.name != point_name]

        intersection_point = midPoint(self.scene, side_vertices[0], side_vertices[1], name=median_point_name)

        Segment(self.scene, vertex, intersection_point)

        return intersection_point

    def bisector(self, vertex_name, intersection_point_name=None):
        """
        Draw the bisector from the vertex ``vertex_name`` and return the intersection point with the opposite side.
        :param vertex_name: name of the vertex (one of p1, p2, p3)
        :param intersection_point_name: optional name for the intersection point
        :return: Point -- the intersection point of the bisector with the opposite side
        """
        vertices = [self.p1, self.p2, self.p3]
        vertex = None
        for v in vertices:
            if v.name == vertex_name:
                vertex = v
                break
        if vertex is None:
            raise ValueError(f"There is no vertex {vertex_name} in the triangle {self}")

        # vertices on the side where the bisector intersects
        A, B = [p for p in vertices if p != vertex]

        def get_bisector_position():
            """
            A function that will calculate the coordinates of the intersection of the bisector
            from 'vertex' with the side AB (points A and B) using the formula:
              BD/DC = vertexA / vertexB
            where D is the desired point on side AB.
            """
            distA = math.hypot(vertex.x - A.x, vertex.y - A.y)
            distB = math.hypot(vertex.x - B.x, vertex.y - B.y)

            # If the triangle is degenerate or distA + distB = 0, return one of the vertices
            if distA + distB == 0:
                return A.x, A.y

            # Parameter t defining the position of point D on AB
            # D = A + t*(B - A)
            t = distA / (distA + distB)

            # Calculate the coordinates of point D
            xD = A.x + t * (B.x - A.x)
            yD = A.y + t * (B.y - A.y)
            return xD, yD

        intersection_point = Point(
            self.scene,
            name=intersection_point_name,
            get_position=get_bisector_position
        )

        Segment(self.scene, vertex, intersection_point)

        return intersection_point

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
