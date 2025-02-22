from manim import *
from random import choice

valid_point_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
point_names = []


class Point:
    def __init__(self, x: float, y: float, name=None):
        self.x, self.y = x, y

        self.rendered = False

        # if name of the point was not specified, we choose random name
        if name is None:
            name = choice(valid_point_names)

        if name in point_names:
            raise Exception(f"The name {name} is already in use")

        self.name = name
        point_names.append(name)
        valid_point_names.remove(name)

    def __iter__(self):
        yield self.x
        yield self.y
        yield 0

    def render(self, scene):
        if not self.rendered:
            self.rendered = True

            circle = Circle(radius=0.05, color=RED, fill_opacity=1)
            circle.move_to((self.x, self.y, 0))
            scene.play(Create(circle))

            point_name_text = Text(self.name, font_size=30)
            point_name_text.move_to((self.x, self.y + 0.3, 0))
            scene.play(Write(point_name_text))