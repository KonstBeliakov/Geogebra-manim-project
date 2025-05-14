from random import randrange

from manim import *

import settings
from tick import Tick
from utils import *


def example0():
    triangle('ABC')

    median('ABC', 'BM')


def example1():
    points(('A', 0, 0), 'B', 'C')

    triangle(('A', 'B', 'C'))

    median(('A', 'B', 'C'), ('B', 'M'))
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
        point('ABCDEFGHIJ'[i], randrange(-10 * i, 10 * i), randrange(-10 * i, 10 * i))
        recenter_camera()


def example4():
    circle((0, 0), 2, 'a')
    circle((3, 0), 3, 'b')

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


def example12(scene):
    circle((0, 0), 1, 'c')
    point('A', 2.3, 1.4)
    tangent('c', 'A', segment_labels=('a', 'b'))

    mark_equals(['a', 'b'])

    move('A', 1.4, -2)

    scene.wait(2)


def example13(scene):
    for i in range(3):
        for j in range(3):
            point(f'A{i}{j}', i, j)

    for i in range(2):
        for j in range(2):
            segment((f'A{i}{j}', f'A{i}{j + 1}'), f'a{i}{j}_1')
            segment((f'A{i}{j}', f'A{i + 1}{j}'), f'a{i}{j}_2')

    mark_all_equal_to(f'a00_1')

    scene.wait(2)


def generate_heart_points(n_points=1000):
    t = np.linspace(0, 2 * np.pi, n_points)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    return x.tolist(), y.tolist()


def example14(scene):
    x, y = generate_heart_points(26)
    l = [(i, j) for i, j in zip(x, y)]
    recenter_camera(l)
    for i in range(len(l)):
        x, y = l[i][0], l[i][1]
        point(chr(ord('A')+i), x=x, y=y)

    for i in range(len(l)):
        name1 = chr(ord('A')+i)
        name2 = chr(ord('A') + (i + 1) % 26)
        segment((name1, name2))

    scene.wait(5)


def example15(scene):
    """
    Testing reflection functions (reflecting about a point)
    """
    point('A', 0, 0)

    point('B', 2, 1)
    mirror_point('B', 'A')

    points(('C', 0.5, 0.5), ('D', 1, 0.5), ('E', 0.5, 1))

    triangle('CDE', 't')

    reflect_figure_about_point('t', 'A')

    scene.wait(2)


def example16(scene):
    """
    Testing a reflection function (reflection about a line)
    """
    point('F', 0, 0)
    point('G', 4, 0)
    segment('F', 'G', label='line')

    point('H', 2, 2)
    reflect_point_about_line('H', 'line', 'H\'')

    points(('I', 1, 1), ('J', 2, 3), ('K', 3, 1))
    triangle('IJK', 'triangle')
    reflect_figure_about_line('triangle', 'line', 'triangle_reflected')

    point('L', 1.5, -1.5)
    point('M', 2.5, -1.5)
    segment('LM', 'seg')
    reflect_figure_about_line('seg', 'FG', 'seg_reflected')

    scene.wait(2)


def example17(scene):
    triangle('ABC', 't')

    bisector('ABC', 'BX')

    mark_equal_angles(['ABX', 'XBC'])

    move_randomly('A')
    scene.wait(1)
    move_randomly('B')
    scene.wait(1)
    move_randomly('C')

    scene.wait(3)


def example18(scene):
    A = point('A', 0, 0, label_x=50, label_y=30)
    B = point('B', 1, 1, label_x=100, label_y=0)

    A.move(1, 0)
    B.move_label_to(0, 0, run_time=1)
    B.move(0, 1)
    hide_label(B)
    B.move(1, 1)
    show_label(B)
    B.move(0, 1)

    settings.show_point_labels = False

    points(('C', 2, 2), ('D', -2, -2))

    scene.wait(1)

    show_label('C')

    scene.wait(1)


def example19(scene):
    A = point('A')
    scene.wait(1)
    hide_point('A')
    scene.wait(1)
    show_point('A')
    scene.wait(1)


def example20(scene):
    points(('A', 0, 0), ('B', 2, 2), ('C', 2, 0), ('D', 0.6, 1.4), ('E', 1.4, 0.6))
    triangle('ABC')
    segment('D', 'E')
    intersect_figures('DE', 'AB', pointNames=('X',))
    scene.wait(1)


def example21(scene):
    settings.show_circle_centers = False
    C = circle((0, 0), 1)
    scene.wait(1)
    point('X')
    C.show_center()
    C.center.show_label = True
    scene.wait(1)


def example22(scene):
    c = circle((0, 0), 1)
    points(('A', -1, 1), ('B', 1, 1))
    s = segment('A', 'B')
    intersect_figures(s, c, pointNames=('X', ))
    scene.wait(1)


class Main(Scene):
    def construct(self):
        init(scene=self)

        example18(self)
