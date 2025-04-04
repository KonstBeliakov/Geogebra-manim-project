from random import randrange

from manim import *
from utils import *


def example0():
    triangle('ABC')

    median('ABC', 'BM')


def example1():
    points(('A', 0, 0), 'B', 'C')

    triangle(('A','B', 'C'))

    median(('A', 'B', 'C'),  ('B', 'M'))
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


def example3():
    for i in range(1, 10):
        point('ABCDEFGHIJ'[i], randrange(-10*i, 10*i), randrange(-10*i, 10*i))
        recenter_camera()


def example4():
    circle((0,0), 2, 'a')
    circle((3,0), 3, 'b')

    intersect_figures('a', 'b', ('A', 'B'))


def example5():
    circle((0, 0), 2, 'a')
    points(('A', -3, -3), ('B', 3, 3))
    segment('AB', 'b')
    intersect_figures('a', 'b', pointNames=('C', 'D'))

    move('A', -3, -1)


def example6(scene):
    triangle('ABC', 'a')
    circumscribed_circle('a', center_name='O')

    move('A', 0, 0)

    scene.wait(2)


def example7(scene):
    point('A', 0, 1)

    circle((0, 0), 0.75, 'a')
    circle('A', 0.75, 'b')

    intersect_figures('a', 'b')

    move('A', 0, -1.5)

    scene.wait(2)

    move('A', 0, -2)


def example8(scene):
    point('A', -1, -1)

    circle((0, 0), 1, 'c')

    s = Segment(scene, (-1, -1), (1, 1), 's')

    intersect_figures('c', 's')

    move('A', 0, -1)

    scene.wait(2)

    move('A', -0.3, -0.3)


def example9(scene):
    circle((0, 0), 1, 'c')
    tangent('c', (2.3, 1.4))
    scene.wait(2)


def example10(scene):
    points(('A', -1, 0), ('B', 0, 1))
    circle((0, 0), 1, 'c')

    arc_midpoint_pos('A', 'B', 'c')

    scene.wait(2)

    move_along_circle('A', 'c')


def example11(scene):
    points(('A', 0, 0), ('B', 1, 1), ('C', -1, 2))
    triangle('ABC', 'a')
    inscribed_circle('a', 'O', 'w')

    move('A', 1, -0.8)

    scene.wait(2)


class Main(Scene):
    def construct(self):
        init(scene=self)

        example4()
