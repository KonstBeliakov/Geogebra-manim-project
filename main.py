from manim import *


class Main(Scene):
    def construct(self):
        t = Triangle()
        t.render(self)
        self.wait(5)
