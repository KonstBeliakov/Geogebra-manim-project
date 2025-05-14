from manim import *
from random import choice, uniform

import settings
from settings import *

valid_point_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
user_point_names = []
point_names = {}


def mark_used_labels_for_points(labels):
    global user_point_names
    user_point_names = labels


def get_point_by_name(name: str) -> Point:
    if name not in point_names:
        raise ValueError(f"There is no such point {name}.")
    return point_names[name]


def get_point_or_random(scene, name: str | None, show_point=True) -> Point:
    """
    Get a point instance by it's name or generate Point instance with such name if there is no such point
    :param scene: scene where will be generated a new point
    :param name: name of the point that we want to get
    :return: Point that we are searching for
    """
    if name in point_names:
        return point_names[name]
    return Point(scene, name, show_point=show_point)


def to_point(scene, point: str | Point | tuple[int | float, int | float] | list[int | float, int | float] | None,
             show_point=True):
    match point:
        case None:
            return Point(scene, show_point=show_point)
        case str():
            return get_point_or_random(scene, point, show_point=show_point)
        case Point():
            return point
        case tuple() | list():
            if len(point) != 2:
                raise ValueError(f"Can't create a point from {type(point)} of length {len(point)}.")
            if not (isinstance(point[0], int) or isinstance(point[0], float)):
                raise ValueError(f"Can't create a point from {point}, because of wrong type of the x coordinate.")
            if not (isinstance(point[1], int) or isinstance(point[1], float)):
                raise ValueError(f"Can't create a point from {point}, because of wrong type of the y coordinate.")

            for p in point_names.values():
                if abs(p.x - point[0]) < 10 ** -6 and abs(p.y - point[1]) < 10 ** -6:
                    return p

            return Point(scene, x=point[0], y=point[1], show_point=show_point)
        case default:
            raise TypeError(f'Can\'t create a point from the argument of type {type(point)}')


class Point:
    def __init__(self, scene, name=None, x=None, y=None, get_position=None,
                 label_x=None, label_y=None, show_label=None, show_point=True):
        """
        :param scene: scene where to draw a point
        :param name: name of the point (can use LaTeX)
        :param x: x coordinate of the point
        :param y: y coordinate of the point
        :param get_position: function that produces point coordinates
        :param label_x: (optional) x position of the label of the point
        :param label_y: (optional) y position of the label of the point
        :param show_label: determines show label of the point on the scene or not
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
            for l in valid_point_names:
                if l not in user_point_names:
                    name = l
            if name is None:
                name = choice(valid_point_names)
        if name in point_names:
            raise ValueError(f"The name {name} is already in use")
        self.name = name
        point_names[name] = self

        if name in valid_point_names:
            valid_point_names.remove(name)

        self.label_dx = ValueTracker(default_label_offset_x if label_x is None else label_x)
        self.label_dy = ValueTracker(default_label_offset_y if label_y is None else label_y)

        self.update_label_position()

        if show_label is None:
            self.show_label = settings.show_point_labels
        else:
            self.show_label = show_label

        self._show_point = show_point

        self.render()

    def update_label_position(self):
        self.label_position = lambda: (self.x + self.label_dx.get_value() * settings.label_position_scaling_factor,
                                       self.y + self.label_dy.get_value() * settings.label_position_scaling_factor,
                                       0)

    def move_label_to(self, label_dx, label_dy, run_time=0):
        self.update_label_position()

        if run_time:
            self.scene.play(
                self.label_dx.animate.set_value(label_dx),
                self.label_dy.animate.set_value(label_dy),
                run_time=run_time
            )
        else:
            self.label_dx.set_value(label_dx)
            self.label_dy.set_value(label_dy)

    def move_label(self, dx=0, dy=0, run_time=0):
        self.move_label_to(label_dx=self.label_dx.get_value() + dx,
                           label_dy=self.label_dy.get_value() + dy,
                           run_time=run_time)

    @property
    def show_point(self):
        return self._show_point

    @show_point.setter
    def show_point(self, value):
        self._show_point = value

        if hasattr(self, "circle"):
            self.circle.set_opacity(1 if value else 0)

    @property
    def show_label(self):
        return self._show_label

    @show_label.setter
    def show_label(self, value):
        self._show_label = value

        if hasattr(self, "point_name_text"):
            if value:
                self.scene.play(Write(self.point_name_text), run_time=point_label_render_time)
            self.point_name_text.set_opacity(1 if value else 0)

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

    @property
    def active(self):
        if self._get_position is not None:
            return self._get_position() is not None
        return True

    def render(self):
        opacity = (1 if self._show_point else 0)
        self.circle = Circle(radius=0.05, color=LINES_COLOR,
                             fill_opacity=opacity,
                             stroke_opacity=opacity)
        self.circle.move_to((self.x, self.y, 0))
        self.scene.play(Create(self.circle), run_time=point_render_time)
        self.scene.wait(point_delay)
        self.circle.add_updater(lambda m: m.move_to((self.x, self.y, 0)))
        self.scene.add(self.circle)

        print(self.name, self._show_label, self._show_point)

        self.point_name_text = Text(self.name, font_size=30,
                                    fill_opacity=(1 if self._show_label and self._show_point else 0))
        self.point_name_text.move_to(self.label_position())
        if self._show_label and self._show_point:
            self.scene.play(Write(self.point_name_text), run_time=point_label_render_time)
        self.scene.wait(point_delay)
        self.point_name_text.add_updater(lambda m: m.move_to(self.label_position()))
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

    def move_along_circle(self, circle: Circle, run_time=4, start_angle=None, angle=TAU):
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
