import math
from random import uniform
from math import *

import numpy as np
from manim import TAU

from circle import Circle, to_figure
from figures import Figure
from point import Point, get_point_by_name, point_names, to_point
from functools import update_wrapper

from segment import Segment
import triangle as tr
from triangle import Triangle


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


def get_altitude_position(vertex, A, B):
    # vector AB
    ABx = B.x - A.x
    ABy = B.y - A.y

    denom = ABx * ABx + ABy * ABy
    if denom == 0:
        return A.x, A.y

    # vector AV
    AVx = vertex.x - A.x
    AVy = vertex.y - A.y

    # product of AV and AB
    dotAV_AB = AVx * ABx + AVy * ABy

    t = dotAV_AB / denom

    xH = A.x + t * ABx
    yH = A.y + t * ABy

    return xH, yH


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
    def get_positions(circle1, circle2):
        x0, y0 = circle1.center.x, circle1.center.y
        x1, y1 = circle2.center.x, circle2.center.y
        r0, r1 = circle1.r, circle2.r

        dx = x1 - x0
        dy = y1 - y0
        d = math.hypot(dx, dy)

        if d > r0 + r1:
            # The circles do not intersect because they are too far apart
            return None, None
        if d < abs(r0 - r1):
            # One circle is completely contained within the other
            return None, None
        if d == 0 and r0 == r1:
            # The circles coincide: infinite number of intersection points
            return None, None

        # Distance from the center of the first circle to the line passing through the intersection points
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        # Distance from this line to the intersection points
        h = math.sqrt(max(r0 ** 2 - a ** 2, 0))

        # Coordinates of the point on the line between the centers, from which we offset h perpendicularly
        x2 = x0 + a * dx / d
        y2 = y0 + a * dy / d

        rx = -h * dy / d
        ry = h * dx / d

        intersection1 = (x2 + rx, y2 + ry)
        intersection2 = (x2 - rx, y2 - ry)

        if dist(intersection1, intersection2) < 10 ** -6:
            return intersection1, None

        return intersection1, intersection2

    name1 = None if pointNames is None else pointNames[0]
    name2 = None if pointNames is None else pointNames[1]
    return [Point(_scene, name=name1, get_position=lambda: get_positions(circle1, circle2)[0]),
            Point(_scene, name=name2, get_position=lambda: get_positions(circle1, circle2)[1])]


@on_scene
def _segment_circle_intersections(segment: Segment, circle: Circle, pointNames: tuple[str, str] = (None, None)):
    def get_positions(segment, circle):
        x1, y1 = segment.p1.x, segment.p1.y
        x2, y2 = segment.p2.x, segment.p2.y

        cx, cy = circle.center.x, circle.center.y
        r = circle.r

        dx = x2 - x1
        dy = y2 - y1

        # Translate the coordinate system so that the center of the circle is at the origin
        x1c = x1 - cx
        y1c = y1 - cy

        # Substitute the parametric equation of the line into the equation of the circle:
        # (x1c + t*dx)^2 + (y1c + t*dy)^2 = r^2
        # This results in a quadratic equation in t:
        # (dx^2 + dy^2) * t^2 + 2*(x1c*dx + y1c*dy) * t + (x1c^2 + y1c^2 - r^2) = 0
        A = dx ** 2 + dy ** 2
        B = 2 * (x1c * dx + y1c * dy)
        C = x1c ** 2 + y1c ** 2 - r ** 2

        discriminant = B ** 2 - 4 * A * C

        intersections = []

        if discriminant < 0:
            # No real roots - the segment and the circle do not intersect
            return [None, None]
        else:
            # Find the roots of the quadratic equation
            sqrt_disc = math.sqrt(discriminant)
            # t1 must be < t2
            t1 = (-B - sqrt_disc) / (2 * A)
            t2 = (-B + sqrt_disc) / (2 * A)

            # Check if the intersection points lie on the segment (t in the range [0,1])
            for t in [t1, t2]:
                if 0 <= t <= 1:
                    xi = x1 + t * dx
                    yi = y1 + t * dy
                    intersections.append((xi, yi))
        if len(intersections) == 1:
            intersections.append(None)
        return intersections

    return [Point(_scene, pointNames[0], get_position=lambda: get_positions(segment, circle)[0]),
            Point(_scene, pointNames[1], get_position=lambda: get_positions(segment, circle)[1])]


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

    def find_tangent_circle_intersections(circle, point):
        px, py = point.x, point.y
        cx, cy = circle.center.x, circle.center.y
        r = circle.r

        dx = px - cx
        dy = py - cy

        d_sq = dx * dx + dy * dy
        d = math.sqrt(d_sq)

        # If the point coincides with the center and radius > 0 — tangents are undefined
        if d == 0:
            return [None, None]

        # If the external point is inside the circle (d < r) — no tangents exist
        if d < r:
            return [None, None]

        # If the external point lies on the circle (d == r) — exactly one tangent,
        # it "touches" at that same point
        if abs(d - r) < 1e-12:
            return [(px, py), None]

        # Case d > r: two tangents
        # The angle between the line (center -> external point) and the tangent
        # can be found using arccos(r / d)
        alpha = math.acos(r / d)

        # The angle of direction from the center to the external point
        theta = math.atan2(dy, dx)

        # Now calculate the coordinates of the tangent points for angles (theta ± alpha)
        # Shift them back by adding (cx, cy).
        # When r/d < 1, the angle delta is valid because acos(r/d) exists.
        t1_angle = theta + alpha
        t2_angle = theta - alpha

        x1 = cx + r * math.cos(t1_angle)
        y1 = cy + r * math.sin(t1_angle)
        x2 = cx + r * math.cos(t2_angle)
        y2 = cy + r * math.sin(t2_angle)

        return [(x1, y1), (x2, y2)]

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

    def arc_midpoint(p1, p2, circle):
        cx, cy = circle.center.x, circle.center.y
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        d1 = hypot(x1 - cx, y1 - cy)
        d2 = hypot(x2 - cx, y2 - cy)

        if abs(d1 - circle.r) > 10**-6:
            raise ValueError(f'Points {p1} is not on the circle {circle}')

        if abs(d2 - circle.r) > 10**-6:
            raise ValueError(f'Point {p2} is not on the circle {circle}')

        # Calculate angles for p1 and p2 relative to the circle's center
        angle1 = math.atan2(y1 - cy, x1 - cx)
        angle2 = math.atan2(y2 - cy, x2 - cx)

        # Compute the difference between angles and normalize it to the range (-pi, pi]
        d_angle = angle2 - angle1
        while d_angle <= -math.pi:
            d_angle += 2 * math.pi
        while d_angle > math.pi:
            d_angle -= 2 * math.pi

        # Find the mid-angle for the minor arc
        mid_angle = angle1 + d_angle / 2

        # The radius is the distance from the center to either point (they lie on the circle)
        r = math.sqrt((x1 - cx) ** 2 + (y1 - cy) ** 2)

        # Compute the coordinates of the arc midpoint using the mid-angle
        mx = cx + r * math.cos(mid_angle)
        my = cy + r * math.sin(mid_angle)

        return mx, my

    return Point(_scene, name=pointName, get_position=lambda: arc_midpoint(p1, p2, circle))


@on_scene
def inscribed_circle(triangle: str | Triangle,
        pointName: str = None,
        circle_label: str = None):
    triangle = to_figure(triangle)

    def incenter_and_inradius(triangle):
        x1, y1 = triangle.p1.x, triangle.p1.y
        x2, y2 = triangle.p2.x, triangle.p2.y
        x3, y3 = triangle.p3.x, triangle.p3.y

        # Sides of triangle
        a = math.hypot(x2 - x3, y2 - y3)
        b = math.hypot(x1 - x3, y1 - y3)
        c = math.hypot(x1 - x2, y1 - y2)

        # Half-perimeter
        p = (a + b + c) / 2

        area = math.sqrt(p * (p - a) * (p - b) * (p - c))

        # inscribed radius
        r = area / p if p != 0 else 0

        # Center of the circle
        x_incenter = (a * x1 + b * x2 + c * x3) / (a + b + c)
        y_incenter = (a * y1 + b * y2 + c * y3) / (a + b + c)

        return (x_incenter, y_incenter), r

    center = Point(_scene, name=pointName, get_position=lambda: incenter_and_inradius(triangle)[0])

    return Circle(_scene, center=center, get_r=lambda: incenter_and_inradius(triangle)[1], label=circle_label)


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


'''
@on_scene
def recenter_camera():
    p_x = [point.x for point in point_names.values()]
    p_y = [point.y for point in point_names.values()]

    center = np.array([(max(p_x) + min(p_x)) / 2, (max(p_y) + min(p_y)) / 2, 0])
    width = max(p_x) - min(p_x) + 2
    height = max(p_y) - min(p_y) + 2

    print(_scene)
    print(_scene.camera)
    print(_scene.camera.__dict__)

    new_width = max(width, height * _scene.camera.frame.get_aspect_ratio())

    _scene.play(
        _scene.camera.frame.animate.move_to(center).set_width(new_width),
        run_time=2
    )
'''


@on_scene
def recenter_camera(run_time=2):
    global _scaling_coefficient

    points = point_names.values()
    p_x = [point.x for point in points]
    p_y = [point.y for point in points]

    center = np.array([(max(p_x) + min(p_x)) / 2, (max(p_y) + min(p_y)) / 2, 0])
    width = max(p_x) - min(p_x) + 2
    height = max(p_y) - min(p_y) + 2

    new_width = max(width, height * _scene.camera.frame.get_aspect_ratio())

    scaling_factor = new_width / _scene.camera.frame_width
    _scaling_coefficient *= scaling_factor

    def new_position(x, y):
        x_new = (x - center[0]) / scaling_factor
        y_new = (y - center[1]) / scaling_factor

        return x_new, y_new

    move_points(points, [new_position(point.x, point.y) for point in points], run_time=run_time)
