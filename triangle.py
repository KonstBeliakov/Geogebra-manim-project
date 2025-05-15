import circle
from point import *
from settings import *
from utils import *
from math_utils import *

from segment import *
from figures import Figure


class Triangle(Figure):
    def __init__(self, scene,
                 p1: str | Point | tuple[float, float] = None,
                 p2: str | Point | tuple[float, float] = None,
                 p3: str | Point | tuple[float, float] = None,
                 label: str = None,
                 segment_labels: list[str] = None,
                 render=True):
        """
        :param scene: scene where to draw a triangle
        :param p1: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param p2: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param p3: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param labels: (optional) labels of three segments from which triangle consists
        """

        self.p1 = to_point(scene, p1)
        self.p2 = to_point(scene, p2)
        self.p3 = to_point(scene, p3)

        # Maby creating 3 segments for a triangle is not very good idea...
        if segment_labels is None:
            segment_labels = [f'{self.p1.name}{self.p2.name}',
                              f'{self.p2.name}{self.p3.name}',
                              f'{self.p3.name}{self.p1.name}']
        elif len(segment_labels) != 3:
            raise ValueError(f'There should be a list of 3 labels (not {len(segment_labels)}')

        self.s1 = Segment(scene, self.p1, self.p2, label=segment_labels[0], render=False)
        self.s2 = Segment(scene, self.p2, self.p3, label=segment_labels[1], render=False)
        self.s3 = Segment(scene, self.p3, self.p1, label=segment_labels[2], render=False)

        super().__init__(scene, label=label, render=render)

    def circumscribed_circle(self, circle_label=None, point_name=None):
        """
        Drawing the circumscribes circle of the triangle
        :param circle_label: optional label of the circle that will be returned
        :param point_name: optional name of the center of the circle
        :return: Circle -- circumscribed circle of the triangle
        """

        center = Point(self.scene, name=point_name,
                       get_position=lambda: get_circumscribed_pos_r(self.p1, self.p2, self.p3)[0],
                       show_point=False)

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
