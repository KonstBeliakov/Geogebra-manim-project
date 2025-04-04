from functools import update_wrapper
from math import *
from random import uniform

from manim import TAU

import figures
import triangle as tr
from circle import Circle, to_figure
from figures import Figure
from math_utils import *
from point import Point, get_point_by_name, point_names, to_point
from segment import Segment
from triangle import Triangle


def midPoint(scene, p1: Point, p2: Point, name=None):
    return Point(scene, get_position=lambda: ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), name=name)


_scene = None
_scaling_coefficient = 1


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


def prepare_segment(scene, triangle: str, segment_name: str, point_builder):
    """
    Auxiliary function to prepare a segment within a triangle.

    This function performs the following steps:
      1) Checks whether to reverse the segment_name so that the first character
         represents the vertex that belongs to the triangle.
      2) Retrieves p1, the point corresponding to the vertex in segment_name,
         and the remaining two vertices A and B (from the triangle that are not in segment_name).
      3) Creates a second point p2 using the provided point_builder callable.
      4) Constructs a segment between p1 and p2 and returns p2.

    Parameters:
        scene: The scene or canvas where the segment is being created.
        triangle (str): A string representing the triangle's vertices.
        segment_name (str): A two-character string where exactly one character must be a vertex
                            of the triangle (representing the common vertex) and the other must not.
        point_builder (callable): A function that takes (scene, p1, A, B, name) as parameters
                                  and returns the second point (p2) for the segment.

    Returns:
        The point p2 created by the point_builder.

    Raises:
        ValueError: If both characters in segment_name belong to the triangle.
                    "Segment name must contain exactly one vertex from the triangle (not both)."
        ValueError: If neither of the characters in segment_name belong to the triangle.
                    "Segment name must contain exactly one vertex from the triangle."
    """
    if segment_name[0] in triangle and segment_name[1] in triangle:
        raise ValueError("Segment name must contain exactly one vertex from the triangle (not both).")
    if segment_name[0] not in triangle and segment_name[1] not in triangle:
        raise ValueError("Segment name must contain exactly one vertex from the triangle.")
    if segment_name[0] not in triangle:
        segment_name = segment_name[::-1]

    p1 = get_point_by_name(segment_name[0])
    A, B = [get_point_by_name(i) for i in triangle if i not in segment_name]

    p2 = point_builder(scene, p1, A, B, segment_name[1])
    Segment(scene, p1, p2)


@on_scene
def median(triangle: str, segment_name: str):
    def midpoint_builder(scene, p1, A, B, name):
        return midPoint(scene, A, B, name=name)

    return prepare_segment(_scene, triangle, segment_name, midpoint_builder)


@on_scene
def bisector(triangle: str, segment_name: str):
    def bisector_builder(scene, p1, A, B, name):
        return Point(scene, name=name, get_position=lambda: get_bisector_position(p1, A, B))

    return prepare_segment(_scene, triangle, segment_name, bisector_builder)


@on_scene
def height(triangle: str, segment_name: str):
    def altitude_builder(scene, p1, A, B, name):
        return Point(scene, name=name, get_position=lambda: get_altitude_position(p1, A, B))

    return prepare_segment(_scene, triangle, segment_name, altitude_builder)


@on_scene
def triangle(pointNames: str, label=None):
    return tr.Triangle(scene=_scene, p1=pointNames[0], p2=pointNames[1], p3=pointNames[2], label=label)


@on_scene
def circle(center=None, r=1, label=None):
    return Circle(_scene, center=center, r=r, label=label)


@on_scene
def segment(pointNames: str, label=None):
    return Segment(_scene, pointNames[0], pointNames[1], label=label)


@on_scene
def point(name: str, x=None, y=None):
    return Point(_scene, name,
                 None if x is None else x / _scaling_coefficient,
                 None if y is None else y / _scaling_coefficient)


@on_scene
def points(*points_data):
    points = []
    for point_data in points_data:
        if isinstance(point_data, str):
            points.append(point(name=point_data))
        else:
            points.append(point(*point_data))
    return points


@on_scene
def _intersect_segments(segment1: str, segment2: str, point_name=None):
    p1_name = get_point_by_name(segment1[0])
    p2_name = get_point_by_name(segment1[1])

    p3_name = get_point_by_name(segment2[0])
    p4_name = get_point_by_name(segment2[1])

    s1 = Segment(_scene, p1_name, p2_name)
    s2 = Segment(_scene, p3_name, p4_name)

    return s1.intersect(s2, pointName=point_name)


@on_scene
def _circle_intersection(circle1, circle2, pointNames: tuple[str, str] = (None, None)):
    name1 = None if pointNames is None else pointNames[0]
    name2 = None if pointNames is None else pointNames[1]
    return [Point(_scene, name=name1, get_position=lambda: circle_intersection_positions(circle1, circle2)[0]),
            Point(_scene, name=name2, get_position=lambda: circle_intersection_positions(circle1, circle2)[1])]


@on_scene
def _segment_circle_intersections(segment: Segment, circle: Circle, pointNames: tuple[str, str] = (None, None)):
    return [Point(_scene, pointNames[0], get_position=lambda: segment_circle_intersection_positions(segment, circle)[0]),
            Point(_scene, pointNames[1], get_position=lambda: segment_circle_intersection_positions(segment, circle)[1])]


@on_scene
def intersect_figures(f1: str | Figure, f2: str | Figure, pointNames: tuple[str, str] = (None, None)):
    f1 = to_figure(f1)
    f2 = to_figure(f2)

    if isinstance(f1, Circle) and isinstance(f2, Circle):
        return _circle_intersection(f1, f2)
    if isinstance(f1, Segment) and isinstance(f2, Circle):
        return _segment_circle_intersections(f1, f2, pointNames=pointNames)
    if isinstance(f2, Segment) and isinstance(f1, Circle):
        return _segment_circle_intersections(f2, f1, pointNames=pointNames)
    if isinstance(f1, Segment) and isinstance(f2, Segment):
        return f1.intersect(f2, None if pointNames is None else pointNames[0])
    raise ValueError(f'Can\'t intersect {f1.label} and {f2.label}.')


@on_scene
def circumscribed_circle(triangle: str | Triangle, circle_label=None, center_name=None):
    triangle = to_figure(triangle)

    return triangle.circumscribed_circle(circle_label=circle_label, point_name=center_name)


@on_scene
def triangle_center(p1: str | Point | tuple[int | float, int | float],
                    p2: str | Point | tuple[int | float, int | float],
                    p3: str | Point | tuple[int | float, int | float],
                    pointName: str = None):
    p1 = to_point(_scene, p1)
    p2 = to_point(_scene, p2)
    p3 = to_point(_scene, p3)

    return Point(_scene, name=pointName, get_position=tr.get_circumscribed_pos_r(p1, p2, p3))


@on_scene
def move(point: str | Point | tuple[int | float, int | float],
         x: float,
         y: float,
         run_time=2):
    to_point(_scene, point).move(x, y, run_time=run_time)


@on_scene
def move_randomly(point: str | Point | tuple[int | float, int | float],
                  run_time=2):
    move(point, uniform(-3, 3), uniform(-3, 3), run_time=run_time)


@on_scene
def move_along_circle(point: str | Point | tuple[int | float, int | float],
                      circle: str | Circle,
                      run_time=4):
    p = to_point(_scene, point)
    circle = to_figure(circle)
    p.move_along_circle(circle,
                        run_time=run_time,
                        angle=TAU)


@on_scene
def tangent(circle: Circle | str,
            point: str | Point | tuple[int | float, int | float],
            pointNames: tuple[str, str] = (None, None),
            segment_labels: tuple[str, str] = (None, None)):
    circle = to_figure(circle)
    point = to_point(_scene, point)

    p1 = Point(_scene, pointNames[0], get_position=lambda: find_tangent_circle_intersections(circle, point)[0])
    p2 = Point(_scene, pointNames[1], get_position=lambda: find_tangent_circle_intersections(circle, point)[1])

    Segment(_scene, point, p1, label=segment_labels[0])
    Segment(_scene, point, p2, label=segment_labels[1])

    return [p1, p2]


@on_scene
def arc_midpoint(p1: str | Point | tuple[int | float, int | float],
                 p2: str | Point | tuple[int | float, int | float],
                 circle: Circle | str,
                 pointName: str = None):
    p1 = to_point(_scene, p1)
    p2 = to_point(_scene, p2)
    circle = to_figure(circle)

    return Point(_scene, name=pointName, get_position=lambda: arc_midpoint_pos(p1, p2, circle))


@on_scene
def inscribed_circle(triangle: str | Triangle,
                     pointName: str = None,
                     circle_label: str = None):
    triangle = to_figure(triangle)

    center = Point(_scene, name=pointName,
                   get_position=lambda: incenter_and_inradius(triangle.p1, triangle.p2, triangle.p3)[0])

    return Circle(_scene, center=center,
                  get_r=lambda: incenter_and_inradius(triangle.p1, triangle.p2, triangle.p3)[1], label=circle_label)


@on_scene
def point_on_circle(circle, pointName=None):
    cx, cy = circle.center.x, circle.center.y

    angle = uniform(0, TAU)
    x = cx + circle.r * cos(angle)
    y = cy + circle.r * sin(angle)

    return Point(_scene, name=pointName, x=x, y=y)


@on_scene
def move_points(points, positions, run_time=2):
    _scene.play(
        *[point.x_tracker.animate.set_value(new_x) for point, (new_x, _) in zip(points, positions)],
        *[point.y_tracker.animate.set_value(new_y) for point, (_, new_y) in zip(points, positions)],
        run_time=run_time
    )


@on_scene
def recenter_camera(run_time=2):
    global _scaling_coefficient

    points = point_names.values()
    point_cords = [(p.x, p.y) for p in points if p.x != 10 ** 18 and p.y != 10 ** 18]

    for figure in figures.figure_names.values():
        if isinstance(figure, Circle):
            x, y, r = figure.center.x, figure.center.y, figure.r
            point_cords.append((x + r, y))
            point_cords.append((x - r, y))
            point_cords.append((x, y - r))
            point_cords.append((x, y + r))

    min_x = min(p[0] for p in point_cords)
    max_x = max(p[0] for p in point_cords)
    min_y = min(p[1] for p in point_cords)
    max_y = max(p[1] for p in point_cords)

    print(min_x, max_x, min_y, max_y)

    width = (max_x - min_x) / 0.9
    height = (max_y - min_y) / 0.9

    scale_x = _scene.camera.frame_width / width
    scale_y = _scene.camera.frame_height / height
    scale_factor = min(scale_x, scale_y)

    _scaling_coefficient *= scale_factor

    def new_position(x, y):
        return (
            (x - min_x) * scale_factor - 0.5 * _scene.camera.frame_width * 0.9,
            (y - min_y) * scale_factor - 0.5 * _scene.camera.frame_height * 0.9
        )

    move_points(points, [new_position(point.x, point.y) for point in points], run_time=run_time)
