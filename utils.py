import math
from random import uniform

from point import Point, get_point_by_name
from functools import update_wrapper

from segment import Segment
import triangle as tr


def midPoint(scene, p1: Point, p2: Point, name=None):
    return Point(scene, get_position=lambda: ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), name=name)


def get_bisector_position(vertex, A, B):
    """
    A function that will calculate the coordinates of the intersection of the bisector
    from 'vertex' with the side AB (points A and B) using the formula:
      BD/DC = vertexA / vertexB
    where D is the desired point on side AB.
    """
    distA = math.hypot(vertex.x - A.x, vertex.y - A.y)
    distB = math.hypot(vertex.x - B.x, vertex.y - B.y)

    # If the triangle is degenerate or distA + distB = 0, return one of the vertices
    if distA + distB == 0:
        return A.x, A.y

    # Parameter t defining the position of point D on AB
    # D = A + t*(B - A)
    t = distA / (distA + distB)

    # Calculate the coordinates of point D
    xD = A.x + t * (B.x - A.x)
    yD = A.y + t * (B.y - A.y)
    return xD, yD


_scene = None


def init(scene):
    global _scene
    _scene = scene


def on_scene(func):
    def wrapper(*args, **kwargs):
        if _scene is None:
            raise Exception(f"Need scene to use function {func.__name__}")
        return func(*args, **kwargs)

    update_wrapper(wrapper, func)
    return wrapper


@on_scene
def median(triangle: str, segment_name: str):
    if segment_name[0] not in triangle:
        segment_name = segment_name[::-1]

    p1 = get_point_by_name(segment_name[0])
    p2 = midPoint(_scene, *[get_point_by_name(i) for i in triangle if i not in segment_name], name=segment_name[1])

    Segment(_scene, p1, p2)
    return p2


@on_scene
def bisector(triangle: str, segment_name: str):
    if segment_name[0] not in triangle:
        segment_name = segment_name[::-1]

    p1 = get_point_by_name(segment_name[0])
    A, B = [get_point_by_name(i) for i in triangle if i not in segment_name]

    p2 = Point(_scene, name=segment_name[1], get_position=lambda: get_bisector_position(p1, A, B))

    Segment(_scene, p1, p2)

    return p2


@on_scene
def height(triangle: str, point_name: str):
    pass


@on_scene
def triangle(pointNames: str):
    return tr.Triangle(scene=_scene, p1=pointNames[0], p2=pointNames[1], p3=pointNames[2])


@on_scene
def segment(pointNames: str):
    return Segment(_scene, pointNames[0], pointNames[1])


@on_scene
def point(name: str, x=None, y=None):
    return Point(_scene, name, x, y)


@on_scene
def points(*points_data):
    points = []
    for point_data in points_data:
        if isinstance(point_data, str):
            points.append(Point(_scene, name=point_data))
        else:
            points.append(Point(_scene, *point_data))
    return points


@on_scene
def intersect(segment1: str, segment2: str, point_name=None):
    p1_name = get_point_by_name(segment1[0])
    p2_name = get_point_by_name(segment1[1])

    p3_name = get_point_by_name(segment2[0])
    p4_name = get_point_by_name(segment2[1])

    s1 = Segment(_scene, p1_name, p2_name)
    s2 = Segment(_scene, p3_name, p4_name)

    return s1.intersect(s2, pointName=point_name)


@on_scene
def move(pointName, x, y, run_time=2):
    get_point_by_name(pointName).move(x, y, run_time)


@on_scene
def move_randomly(pointName, run_time=2):
    move(pointName, uniform(-3, 3), uniform(-3, 3), run_time)
