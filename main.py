from manim import *
from utils import *

from math import *


def example1():
    triangle('ABC')

    median('ABC', "BM")
    bisector('ABC', 'BD')
    height('ABC', 'AH')

    move_randomly('A')
    move_randomly('B')
    move_randomly('C')


def example2():
    points(('A', 1, 0))
    c = circle('A', r=1.5)

    point_on_circle(c, 'B')
    point_on_circle(c, 'C')
    point_on_circle(c, 'D')

    triangle('BCD')

    move_along_circle('B', c)


class Main(Scene):
    def construct(self):
        init(scene=self)

        example2()
