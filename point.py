from manim import *
from random import choice, uniform

valid_point_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
point_names = []


class Point:
    def __init__(self, scene, x=None, y=None, get_position=None, name=None):
        self.scene = scene

        self._get_position = get_position
        if self._get_position is not None:
            x, y = self._get_position()
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
        point_names.append(name)
        valid_point_names.remove(name)

        self.render()

    @property
    def x(self):
        if self._get_position is not None:
            return self._get_position()[0]
        return self.x_tracker.get_value()

    @property
    def y(self):
        if self._get_position is not None:
            return self._get_position()[1]
        return self.y_tracker.get_value()

    def render(self):
        self.rendered = True

        self.circle = Circle(radius=0.05, color=RED, fill_opacity=1)
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

    def move(self, new_x, new_y):
        self.scene.play(
            self.x_tracker.animate.set_value(new_x),
            self.y_tracker.animate.set_value(new_y),
            run_time=2
        )

    def __iter__(self):
        yield self.x
        yield self.y
        yield 0
