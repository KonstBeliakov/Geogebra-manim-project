from manim import *
from figures import *
from settings import *
from point import Point, to_point
from math_utils import *


class Circle(Figure):
    def __init__(
        self,
        scene,
        center: Point | str | tuple[float, float] = None,
        r: float = 1,
        get_r=None,
        label: str = None
    ):
        """
        :param scene:  the scene where the circle will be drawn.
        :param center: Point object, point name (if it doesn't exist, it will be created), or (x, y) tuple.
        :param r:      radius of the circle (used only if get_r is None).
        :param get_r:  a lambda/function returning the current radius; if provided,
                       the circle will update dynamically based on this function.
        :param label:  label for the circle.
        """
        self.scene = scene
        self.center = to_point(scene, center)
        self._get_radius = get_r

        if self._get_radius is None:
            self.r_tracker = ValueTracker(r)

        super().__init__(scene, label=label)

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
        circle = manim.Circle(
            radius=self.r,
            color=LINES_COLOR,
            fill_opacity=FIGURE_FILL_OPACITY
        )
        circle.move_to((self.center.x, self.center.y, 0))
        self.scene.play(Create(circle))
        self.scene.wait(0.3)

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
        :param center_name: optional name for the center point.
        :return: an instance of Circle with a dynamically computed center and radius.
        """
        # Convert inputs to Point objects
        p1 = to_point(scene, p1)
        p2 = to_point(scene, p2)
        p3 = to_point(scene, p3)

        # Create a dynamic center point using a lambda that computes the center.
        center = Point(scene, name=center_name, get_position=lambda: get_circumscribed_pos_r(p1, p2, p3)[0])
        # Create the circle with a dynamic radius using the get_center_and_radius function.
        return cls(scene, center=center, get_r=lambda: get_circumscribed_pos_r(p1, p2, p3)[1], label=label)
