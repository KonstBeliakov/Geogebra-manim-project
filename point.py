from manim import *
from random import choice, uniform
from settings import *

valid_point_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
point_names = {}


def get_point_by_name(name: str) -> Point:
    if name not in point_names:
        raise ValueError(f"There is no such point {name}.")
    return point_names[name]


def get_point_or_random(scene, name: str | None) -> Point:
    """
    Get a point instance by it's name or generate Point instance with such name if there is no such point
    :param scene: scene where will be generated a new point
    :param name: name of the point that we want to get
    :return: Point that we are searching for
    """
    if name in point_names:
        return point_names[name]
    return Point(scene, name)


def to_point(scene, point: str | Point | tuple[int | float, int | float] | list[int | float, int | float] | None):
    if point is None:
        return Point(scene)
    if isinstance(point, str):
        return get_point_or_random(scene, point)
    if isinstance(point, Point):
        return point
    if isinstance(point, tuple) or isinstance(point, list):
        if len(point) != 2:
            raise ValueError(f"Can't create a point from {type(point)} of length {len(point)}.")
        if not (isinstance(point[0], int) or isinstance(point[0], float)):
            raise ValueError(f"Can't create a point from {point}, because of wrong type of the x coordinate.")
        if not (isinstance(point[1], int) or isinstance(point[1], float)):
            raise ValueError(f"Can't create a point from {point}, because of wrong type of the y coordinate.")

        for p in point_names.values():
            if abs(p.x - point[0]) < 10 ** -6 and abs(p.y - point[1]) < 10 ** -6:
                return p

        return Point(scene, x=point[0], y=point[1])


class Point:
    def __init__(self, scene, name=None, x=None, y=None, get_position=None):
        """
        :param scene: scene where to draw a point
        :param name: name of the point (can use LaTeX)
        :param x: x coordinate of the point
        :param y: y coordinate of the point
        :param get_position: function that produces point coordinates
        """
        self.scene = scene

        self._get_position = get_position
        if self._get_position is not None:
            x, y = self.x, self.y
        else:
            if x is None:
                x = uniform(-3, 3)
            if y is None:
                y = uniform(-3, 3)

        self.x_tracker = ValueTracker(x)
        self.y_tracker = ValueTracker(y)

        if name is None:
            name = choice(valid_point_names)
        if name in point_names:
            raise ValueError(f"The name {name} is already in use")
        self.name = name
        point_names[name] = self

        if name in valid_point_names:
            valid_point_names.remove(name)

        self.render()

    @property
    def x(self):
        if self._get_position is not None:
            if self._get_position() is None:
                return 10 ** 18  # infinitelly far point
            return self._get_position()[0]
        return self.x_tracker.get_value()

    @property
    def y(self):
        if self._get_position is not None:
            if self._get_position() is None:
                return 10 ** 18  # infinitelly far point...
            return self._get_position()[1]
        return self.y_tracker.get_value()

    def render(self):
        self.circle = Circle(radius=0.05, color=LINES_COLOR, fill_opacity=1)
        self.circle.move_to((self.x, self.y, 0))
        self.scene.play(Create(self.circle))
        self.scene.wait(0.3)
        self.circle.add_updater(lambda m: m.move_to((self.x, self.y, 0)))
        self.scene.add(self.circle)

        self.point_name_text = Text(self.name, font_size=30)
        self.point_name_text.move_to((self.x, self.y + 0.3, 0))
        self.scene.play(Write(self.point_name_text))
        self.scene.wait(0.3)
        self.point_name_text.add_updater(lambda m: m.move_to((self.x, self.y + 0.3, 0)))
        self.scene.add(self.point_name_text)

    def move(self, new_x, new_y, run_time=2):
        """
        Smoothly moves the point (and all dependent objects)
        :param new_x: new x coordinate of the point
        :param new_y: new y coordinate of the point
        :return:
        """
        self.scene.play(
            self.x_tracker.animate.set_value(new_x),
            self.y_tracker.animate.set_value(new_y),
            run_time=run_time
        )

    def move_along_circle(self, circle, run_time=4, start_angle=None, angle=TAU):
        center = circle.center
        r = circle.r

        if start_angle is None:
            start_angle = np.arctan2(self.y - center.y, self.x - center.x)

        def update_func(mob, alpha):
            new_x = center.x + r * np.cos(start_angle + alpha * angle)
            new_y = center.y + r * np.sin(start_angle + alpha * angle)
            self.x_tracker.set_value(new_x)
            self.y_tracker.set_value(new_y)

        self.scene.play(UpdateFromAlphaFunc(self.circle, update_func), run_time=run_time)

    def __iter__(self):
        """
        We can use a point as list of it's coordinates: ``tuple(point)``
        :return:
        """
        yield self.x
        yield self.y
        yield 0
