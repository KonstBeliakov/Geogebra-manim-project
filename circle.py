import math
from random import choice

import manim
from manim import *

import point
from point import get_point_or_random
from segment import Segment
from settings import *

valid_figure_labels = [chr(i) for i in range(ord('a'), ord('z') + 1)]
figure_names = {}


def get_figure(label):
    if label not in figure_names:
        raise ValueError(f'There is no such figure with label "{label}".')
    return figure_names[label]


class Circle:
    def __init__(self, scene, center=None, r=1, label=None):
        """
        :param scene: scene where to draw a circle
        :param center: Point instance or name of the point. (If there is no such point it will be created)
        :param r: radius of the circle
        """
        self.scene = scene

        if isinstance(center, str) or center is None:
            center = get_point_or_random(scene, center)

        self.center = center
        self.r = r

        if label is None:
            label = choice(valid_figure_labels)
        if label in figure_names:
            raise ValueError(f"The name {label} is already in use")
        self.label = label
        figure_names[label] = self

        if label in valid_figure_labels:
            valid_figure_labels.remove(label)

        self.render()

    def render(self):
        circle = manim.Circle(radius=self.r, color=LINES_COLOR, fill_opacity=FIGURE_FILL_OPACITY)
        circle.move_to((self.center[0], self.center[1], 0))
        self.scene.play(Create(circle))
        self.scene.wait(0.3)
        circle.add_updater(lambda m: m.move_to((self.center[0], self.center[1], 0)))
        self.scene.add(circle)
