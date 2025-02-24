from manim import Scene
from point import Point
from circle import Circle


class Main(Scene):
    def construct(self):
        A = Point(self, 'A', 0, 0)

        Circle(self, 'A')

        # The circle moves when we move its center
        A.move(1, 1)

        self.wait(1)
