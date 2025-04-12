from manim import *
import numpy as np
import math

from point import to_point
from settings import *


class ArcMark:
    def __init__(self, scene, p1, p2, p3):
        self.scene = scene
        self.p1 = to_point(scene, p1)
        self.p2 = to_point(scene, p2)
        self.p3 = to_point(scene, p3)

        self.render()

    def angle_marker_arc(self):
        center = np.array([self.p2.x, self.p2.y, 0])
        v1 = np.array([self.p1.x, self.p1.y, 0]) - center
        v2 = np.array([self.p3.x, self.p3.y, 0]) - center

        if np.linalg.norm(v1) < 1e-12 or np.linalg.norm(v2) < 1e-12:
            return VGroup()

        def angle_of_vector(v):
            return math.atan2(v[1], v[0])

        start_angle = angle_of_vector(v1)
        end_angle = angle_of_vector(v2)
        raw_angle = end_angle - start_angle

        if raw_angle < 0:
            raw_angle += 2 * math.pi
        # if raw_angle > math.pi:
        #    raw_angle = 2 * math.pi - raw_angle
        #
        #    start_angle, end_angle = end_angle, start_angle
        #    if raw_angle < 0:
        #        raw_angle += 2 * math.pi

        arc = Arc(
            radius=arc_radius,
            start_angle=start_angle,
            angle=raw_angle,
            arc_center=center,
            color=LINES_COLOR
        )
        return arc

    def render(self):
        arc_mob = always_redraw(self.angle_marker_arc)
        self.scene.play(Create(arc_mob))
