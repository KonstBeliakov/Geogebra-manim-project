import math

from figures import *
from point import *
from settings import *


class Segment(Figure):
    def __init__(self, scene,
                 p1: str | Point | tuple[float, float] = None,
                 p2: str | Point | tuple[float, float] = None,
                 label: str = None,
                 render=True):
        """
        :param scene: scene where to draw the segment
        :param p1: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param p2: Point instance or name of the point or it's coordinates. (If there is no such point it will be created)
        :param label: label of the segment
        """

        self.p1 = to_point(scene, p1)
        self.p2 = to_point(scene, p2)

        super().__init__(scene, label=label, render=render)

    @property
    def length(self):
        return math.hypot(self.p1.x - self.p2.x, self.p1.y - self.p2.y)

    def render(self):
        self.line = always_redraw(lambda: Line(tuple(self.p1), tuple(self.p2), color=LINES_COLOR))
        self.scene.play(Create(self.line), run_time=segment_render_time)

    def middle(self, middle_point_name=None):
        """
        Draw the middle of the segment
        :param middle_point_name: name of the middle point that will be created
        :return: middle point
        """
        return Point(self.scene, name=middle_point_name,
                     get_position=lambda: ((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2))

    def intersect(self, other, pointName=None):
        """
        Draw the intersection of two segments
        :param other: the segment with which we want to find the intersection point
        :param pointName: name of the point of the intersection
        :return: Point of the intersection
        """

        def get_position(segment1, segment2):
            x1, y1 = segment1.p1.x, segment1.p1.y
            x2, y2 = segment1.p2.x, segment1.p2.y

            x3, y3 = segment2.p1.x, segment2.p1.y
            x4, y4 = segment2.p2.x, segment2.p2.y

            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if denom == 0:
                return None

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

            #if 0 <= t <= 1 and 0 <= u <= 1:
            intersect_x = x1 + t * (x2 - x1)
            intersect_y = y1 + t * (y2 - y1)
            return intersect_x, intersect_y
            #else:
            #    return None

        return Point(self.scene, pointName, get_position=lambda: get_position(self, other))
