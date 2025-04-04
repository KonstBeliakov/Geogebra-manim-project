import circle
from point import *
from settings import *
from utils import *
from math_utils import *


class Triangle(Figure):
    def __init__(self, scene,
                 p1: str | Point | tuple[float, float] = None,
                 p2: str | Point | tuple[float, float] = None,
                 p3: str | Point | tuple[float, float] = None,
                 label: str = None):
        """
        :param scene: scene where to draw a triangle
        :param p1: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param p2: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param p3: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        """

        self.p1 = to_point(scene, p1)
        self.p2 = to_point(scene, p2)
        self.p3 = to_point(scene, p3)

        super().__init__(scene, label=label)

    def circumscribed_circle(self, circle_label=None, point_name=None):
        """
        Drawing the circumscribes circle of the triangle
        :param circle_label: optional label of the circle that will be returned
        :param point_name: optional name of the center of the circle
        :return: Circle -- circumscribed circle of the triangle
        """

        center = Point(self.scene, name=point_name,
                       get_position=lambda: get_circumscribed_pos_r(self.p1, self.p2, self.p3)[0])

        circ_circle = circle.Circle(self.scene, center,
                                    get_r=lambda: get_circumscribed_pos_r(self.p1, self.p2, self.p3)[1],
                                    label=circle_label)

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
