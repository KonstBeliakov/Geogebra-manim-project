from point import Point
from random import uniform


def rand_point():
    return Point(uniform(-3, 3), uniform(-3, 3))
