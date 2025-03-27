from manim import *

from figures import *
from point import get_point_or_random
from settings import *


class Circle(Figure):
    def __init__(self, scene, center=None, r=1, label=None):
        """
        :param scene: scene where to draw a circle
        :param center: Point instance or name of the point. (If there is no such point it will be created)
        :param r: radius of the circle
        :param label: label of the circle
        """
        self.scene = scene

        if isinstance(center, str) or center is None:
            center = get_point_or_random(scene, center)

        self.center = center
        self.r = r

        super().__init__(label=label)

    def render(self):
        circle = manim.Circle(radius=self.r, color=LINES_COLOR, fill_opacity=FIGURE_FILL_OPACITY)
        circle.move_to((self.center[0], self.center[1], 0))
        self.scene.play(Create(circle))
        self.scene.wait(0.3)
        circle.add_updater(lambda m: m.move_to((self.center[0], self.center[1], 0)))
        self.scene.add(circle)
