from point import Point, get_point_by_name
from functools import update_wrapper

from segment import Segment
import triangle as tr


def midPoint(scene, p1: Point, p2: Point, name=None):
    return Point(scene, get_position=lambda: ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), name=name)


_scene = None


def init(scene):
    global _scene
    _scene = scene


def on_scene(func):
    def wrapper(*args, **kwargs):
        if _scene is None:
            raise Exception(f"Need scene to use function {func.__name__}")
        print(f'func: {func.__name__}\nargs: {args}\nkwargs: {kwargs}')
        return func(*args, **kwargs)

    update_wrapper(wrapper, func)
    return wrapper


@on_scene
def median(triangle: str, point_name: str):
    pass


@on_scene
def bisector(triangle: str, segment_name: str):
    p1_name, p2_name, p3_name = triangle

    p1 = get_point_by_name(p1_name)
    p2 = get_point_by_name(p2_name)
    p3 = get_point_by_name(p3_name)

    t = tr.Triangle(_scene, p1, p2, p3)
    t.bisector(segment_name[0], segment_name[1])

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
