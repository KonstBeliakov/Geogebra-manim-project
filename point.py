from manim import *
from random import choice, uniform
from object import Object


valid_point_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
point_names = []


class Point(Object):
    def __init__(self, scene, x=None, y=None, get_position=None, name=None):
        self.rendered = False
        super().__init__(scene)

        self.get_positionLambda = get_position

        if self.get_positionLambda is not None:
            self.x, self.y = self.get_positionLambda()
        else:
            if x is None:
                x = uniform(-3, 3)
            if y is None:
                y = uniform(-3, 3)

            self.x, self.y = x, y



        # if name of the point was not specified, we choose random name
        if name is None:
            name = choice(valid_point_names)

        if name in point_names:
            raise Exception(f"The name {name} is already in use")

        self.name = name
        point_names.append(name)
        valid_point_names.remove(name)

        self.render()

    def __getattribute__(self, item):
        if item in ('x', 'y'):
            get_position = object.__getattribute__(self, 'get_positionLambda')
            if get_position is not None:
                pos = get_position()
                return pos[0] if item == 'x' else pos[1]
        return object.__getattribute__(self, item)

    def __iter__(self):
        yield self.x
        yield self.y
        yield 0

    def render(self):
        if not self.rendered:
            self.rendered = True

            self.circle = Circle(radius=0.05, color=RED, fill_opacity=1)
            self.circle.move_to((self.x, self.y, 0))
            self.scene.play(Create(self.circle))

            self.point_name_text = Text(self.name, font_size=30)
            self.point_name_text.move_to((self.x, self.y + 0.3, 0))
            self.scene.play(Write(self.point_name_text))

    def transform(self):
        circle2 = Circle(radius=0.05, color=RED, fill_opacity=1)
        circle2.move_to((self.x, self.y, 0))

        self.scene.play(Transform(self.circle, circle2))
        self.circle = circle2

        point_name_text2 = Text(self.name, font_size=30)
        point_name_text2.move_to((self.x, self.y + 0.3, 0))
        self.scene.play(Transform(self.point_name_text, point_name_text2))

        self.point_name_text = point_name_text2

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

        self.update()
