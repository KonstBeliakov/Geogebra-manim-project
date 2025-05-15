from manim import *

import settings
from figures import *
from settings import *
from point import Point, to_point
from math_utils import *
import math


class Circle(Figure):
    def __init__(
        self,
        scene,
        center: Point | str | tuple[float, float] = None,
        r: float = 1,
        get_r=None,
        label: str = None,
        render=True
    ):
        """
        :param scene:  the scene where the circle will be drawn.
        :param center: Point object, point name (if it doesn't exist, it will be created), or (x, y) tuple.
        :param r:      radius of the circle (used only if get_r is None).
        :param get_r:  a lambda/function returning the current radius; if provided,
                       the circle will update dynamically based on this function.
        :param label:  label for the circle.
        :param render: whether to render the circle immediately.
        """
        self.scene = scene
        self.center = to_point(scene, center, show_point=settings.show_circle_centers)
        print('center of circle: ', self.center.name, self.center.show_label, self.center.show_point)
        self._get_radius = get_r

        if self._get_radius is None:
            self.r_tracker = ValueTracker(r)

        super().__init__(scene, label=label, render=render)

    def show_center(self):
        self.center.show_point = True

    @property
    def r(self) -> float:
        """
        Current radius value.
        If self._get_radius is defined, use its return value.
        Otherwise, use the value from r_tracker.
        """
        if self._get_radius is not None:
            return self._get_radius()
        return self.r_tracker.get_value()

    @r.setter
    def r(self, new_r: float):
        """
        Radius setter. Only works if _get_radius was not provided.
        """
        if self._get_radius is not None:
            raise ValueError("Cannot set r directly when using get_r for dynamic radius.")
        self.r_tracker.set_value(new_r)

    def render(self):
        # Create the circle with initial values.
        if settings.show_circle_centers:
            self.center.show_point = True
            if settings.show_point_labels:
                self.center.show_label = True

        circle = manim.Circle(
            radius=self.r,
            color=LINES_COLOR,
            fill_opacity=FIGURE_FILL_OPACITY
        )
        circle.move_to((self.center.x, self.center.y, 0))
        self.scene.play(Create(circle), run_time=circle_render_time)
        self.scene.wait(circle_delay)

        # Updater function to update the circle dynamically.
        def update_circle(m: manim.Circle):
            new_circle = manim.Circle(
                radius=self.r,
                color=LINES_COLOR,
                fill_opacity=FIGURE_FILL_OPACITY
            )
            new_circle.move_to((self.center.x, self.center.y, 0))
            m.become(new_circle)

        circle.add_updater(update_circle)
        self.scene.add(circle)

    @classmethod
    def from_three_points(cls, scene,
                          p1: str | Point | tuple[float, float],
                          p2: str | Point | tuple[float, float],
                          p3: str | Point | tuple[float, float],
                          label: str = None,
                          center_name: str = None):
        """
        Alternative constructor to create a circle passing through three points.
        Computes the circumscribed circle of the three points.
        :param scene: the scene where the circle will be drawn.
        :param p1: first point (Point object, point name as a string, or (x, y) tuple).
        :param p2: second point (Point object, point name as a string, or (x, y) tuple).
        :param p3: third point (Point object, point name as a string, or (x, y) tuple).
        :param label: optional label for the circle.
        :return: an instance of Circle with a dynamically computed center and radius.
        """
        p1 = to_point(scene, p1)
        p2 = to_point(scene, p2)
        p3 = to_point(scene, p3)

        center = Point(
            scene,
            name=center_name,
            get_position=lambda: get_circumscribed_pos_r(p1, p2, p3)[0],
        )
        return cls(
            scene,
            center=center,
            get_r=lambda: get_circumscribed_pos_r(p1, p2, p3)[1],
            label=label
        )

    @classmethod
    def from_two_points(cls, scene,
                        center_pt: str | Point | tuple[float, float],
                        boundary_pt: str | Point | tuple[float, float],
                        label: str = None):
        """
        Alternative constructor to create a circle from a center and a point on its circumference.
        :param scene:       the scene where the circle will be drawn.
        :param center_pt:   center of the circle (Point object, point name as a string, or (x, y) tuple).
        :param boundary_pt: a point on the circumference (Point object, point name, or (x, y) tuple).
        :param label:       optional label for the circle.
        :return: an instance of Circle with a dynamically computed radius.
        """
        center = to_point(scene, center_pt, show_point=settings.show_circle_centers)
        boundary = to_point(scene, boundary_pt)

        return cls(
            scene,
            center=center,
            get_r=lambda: math.hypot(boundary.x - center.x, boundary.y - center.y),
            label=label
        )
