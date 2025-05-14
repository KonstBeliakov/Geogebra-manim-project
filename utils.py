from functools import update_wrapper
from math import *
from random import uniform

from manim import TAU

import figures
import settings
import triangle as tr
from circle import Circle, to_figure
from figures import Figure
from math_utils import *
from point import Point, get_point_by_name, point_names, to_point
from segment import Segment
from tick import Tick
from arcmark import ArcMark
from triangle import Triangle


def midPoint(p1: Point, p2: Point, name=None):
    return Point(_scene, get_position=lambda: ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), name=name)


_scene = None


# function that calculates new position of points with respect to scaling (by default it does not change coordinates)
def _new_position(x, y):
    return x, y


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
def median(triangle: str, segment_name: str) -> Point:
    """
    Draw the **median** from a vertex of *triangle*.

    :param triangle : str
            The three-character label of the triangle, e.g. ``'ABC'``.
    :param segment_name : str
            A two-character string such as ``'AD'`` where the first character is
            the vertex of the median and the second is the new point to be
            created on the opposite side.

    :returns: Point The midpoint of the opposite side, i.e. the foot of the median.
    """

    def midpoint_builder(scene, p1, A, B, name):
        return midPoint(A, B, name=name)

    return prepare_segment(_scene, triangle, segment_name, midpoint_builder)


@on_scene
def bisector(triangle: str, segment_name: str):
    """
    Draw an **internal angle-bisector** from a vertex of *triangle*.

    The interface is the same as median; the created point lies on
    the opposite side at such a position that the two adjacent angles are
    equal.
    """

    def bisector_builder(scene, p1, A, B, name):
        return Point(scene, name=name, get_position=lambda: get_bisector_position(p1, A, B))

    return prepare_segment(_scene, triangle, segment_name, bisector_builder)


@on_scene
def height(triangle: str, segment_name: str):
    """
    Draw an **altitude (height)** from a vertex of *triangle*.

    The altitude is dropped perpendicularly on the opposite side (or its
    extension).  The second character of *segment_name* names the foot of the
    perpendicular.
    """

    def altitude_builder(scene, p1, A, B, name):
        return Point(scene, name=name, get_position=lambda: get_altitude_position(p1, A, B))

    return prepare_segment(_scene, triangle, segment_name, altitude_builder)


@on_scene
def triangle(pointNames: str, label=None, segment_labels=None, render=True):
    """
    Convenience wrapper around :class:`triangle.Triangle`.

    :param pointNames : str Exactly three characters (e.g. ``'ABC'``).
    :param label : str | None - Optional label for the triangle itself.
    :returns Triangle
    """
    return tr.Triangle(scene=_scene, p1=pointNames[0], p2=pointNames[1], p3=pointNames[2], label=label,
                       segment_labels=segment_labels, render=render)


def line_coefficients(p1: Point, p2: Point) -> tuple[float, float, float]:
    """
    Returns the coefficients (A, B, C) of the line Ax + By + C = 0
    passing through the points p1(x1, y1) and p2(x2, y2).
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    # Line equation through (x1, y1) and (x2, y2):
    # A = (y2 - y1), B = (x1 - x2), C = x2*y1 - x1*y2
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    return A, B, C


@on_scene
def mirror_point(
        point: str | Point | tuple,
        center: str | Point | tuple,
        name: str = None
) -> Point:
    """
    Creates a new point — the reflection of the point 'point'
    with respect to the point 'center'.
    """
    p = to_point(_scene, point)
    c = to_point(_scene, center)

    def get_position():
        return 2 * c.x - p.x, 2 * c.y - p.y

    return Point(_scene, name=name, get_position=get_position)


@on_scene
def reflect_figure_about_point(
        figure: str | Figure,
        reflection_center: str | Point | tuple,
        new_figure_label: str = None
) -> Figure:
    """
    Reflects a given geometric figure (circle, segment, triangle)
    with respect to the point 'reflection_center'. Returns a new figure.
    """
    figure = to_figure(figure)
    center = to_point(_scene, reflection_center)

    if isinstance(figure, Circle):
        new_center = mirror_point(figure.center, center)
        return Circle(
            _scene,
            center=new_center,
            get_r=figure._get_radius,
            label=new_figure_label
        )
    if isinstance(figure, Segment):
        new_p1 = mirror_point(figure.p1, center)
        new_p2 = mirror_point(figure.p2, center)
        return Segment(_scene, new_p1, new_p2, label=new_figure_label)
    if isinstance(figure, Triangle):
        new_p1 = mirror_point(figure.p1, center)
        new_p2 = mirror_point(figure.p2, center)
        new_p3 = mirror_point(figure.p3, center)
        return Triangle(
            _scene,
            p1=new_p1,
            p2=new_p2,
            p3=new_p3,
            label=new_figure_label
        )


@on_scene
def reflect_point_about_line(
        point: str | Point | tuple,
        reflection_line: str | Segment,
        name: str = None
) -> Point:
    """
    Reflects the point 'point' about the line defined by the segment 'reflection_line'.
    The reflection uses the infinite line passing through the endpoints of the segment.
    Returns a new point.
    """
    p = to_point(_scene, point)
    line_segment = to_figure(reflection_line)

    if not isinstance(line_segment, Segment):
        raise TypeError(f"The argument reflection_line must be a Segment, not {type(line_segment)}.")

    A, B, C = line_coefficients(line_segment.p1, line_segment.p2)

    def get_position():
        x0, y0 = p.x, p.y
        denom = A * A + B * B
        # Formula for reflection of a point (x0, y0) about the line A x + B y + C = 0:
        # x' = x0 - 2A(A*x0 + B*y0 + C)/(A^2 + B^2)
        # y' = y0 - 2B(A*x0 + B*y0 + C)/(A^2 + B^2)
        factor = 2 * (A * x0 + B * y0 + C) / denom
        xr = x0 - factor * A
        yr = y0 - factor * B
        return xr, yr

    return Point(_scene, name=name, get_position=get_position)


@on_scene
def reflect_figure_about_line(
        figure: Figure | str,
        reflection_line: str | Segment,
        new_figure_label: str = None
) -> Figure:
    """
    Reflects the given figure about the infinite line
    passing through the endpoints of the segment 'reflection_line'.
    Returns a new figure.
    """
    figure = to_figure(figure)
    line_segment = to_figure(reflection_line)

    if not isinstance(line_segment, Segment):
        raise TypeError(f"The argument reflection_line must be a Segment, not {type(line_segment)}.")

    if isinstance(figure, Circle):
        new_center = reflect_point_about_line(figure.center, line_segment)
        return Circle(_scene, center=new_center, get_r=figure._get_radius, label=new_figure_label)
    if isinstance(figure, Segment):
        new_p1 = reflect_point_about_line(figure.p1, line_segment)
        new_p2 = reflect_point_about_line(figure.p2, line_segment)
        return Segment(_scene, new_p1, new_p2, label=new_figure_label)
    if isinstance(figure, Triangle):
        new_p1 = reflect_point_about_line(figure.p1, line_segment)
        new_p2 = reflect_point_about_line(figure.p2, line_segment)
        new_p3 = reflect_point_about_line(figure.p3, line_segment)
        return Triangle(
            _scene,
            p1=new_p1,
            p2=new_p2,
            p3=new_p3,
            label=new_figure_label
        )


@on_scene
def circle(center: Point | str | tuple[int | float] = None,
           r: float = 1,
           label: str = None,
           render=True):
    """
    Draw a circle
    :param center - center of the circle
    :param r - radius of the circle
    :label - optional label of the circle
    """
    return Circle(_scene, center=center, r=r, label=label, render=render)


@on_scene
def circle_from_two_points(center: str | Point | tuple[float, float],
                             p: str | Point | tuple[float, float],
                             label: str = None):

    return Circle.from_two_points(_scene, center, p, label)

@on_scene
def circle_from_three_points(p1: str | Point | tuple[float, float],
                             p2: str | Point | tuple[float, float],
                             p3: str | Point | tuple[float, float],
                             label: str = None,
                             center_name: str = None):
    return Circle.from_three_points(_scene, p1, p2, p3, label, center_name)


@on_scene
def segment(p1: str | Point | tuple[float, float] = None,
            p2: str | Point | tuple[float, float] = None,
            label: str = None,
            render=True):
    return Segment(_scene, p1, p2, label, render=render)


@on_scene
def point(name: str, x=None, y=None, label_x=None, label_y=None, show_label=None, show_point=True):
    """
    Draw a point
    :param name - name of the point
    :param x - x position of the point
    :param y - y position of the point
    :param label_x - (optional) x position of the label of the point
    :param label_y - (optional) y position of the label of the point
    :param show_label: determines show label of the point on the scene or not
    """
    # x_new = None if x is None else _new_position(x, y)[0]
    # print(f'x: {x}, x_new: {x_new}')
    #
    # y_new = None if y is None else _new_position(x, y)[1]
    # print(f'y: {y}, y_new: {y_new}')
    #
    # label_x_new = None if label_x is None else _new_position(label_x, label_y)[0]
    # print(f'label_x: {label_x}, label_x_new: {label_x_new}')
    #
    # label_y_new = None if label_y is None else _new_position(label_x, label_y)[1]
    # print(f'label_y: {label_y}, label_y_new: {label_y_new}')

    return Point(_scene, name,
                 x=None if x is None else _new_position(x, y)[0],
                 y=None if y is None else _new_position(x, y)[1],
                 label_x=None if label_x is None else _new_position(label_x, label_y)[0],
                 label_y=None if label_y is None else _new_position(label_x, label_y)[1],
                 show_label=show_label,
                 show_point=show_point)


@on_scene
def show_label(point: str | Point | tuple[float, float]):
    to_point(_scene, point).show_label = True


@on_scene
def hide_label(point: str | Point | tuple[float, float]):
    to_point(_scene, point).show_label = False


@on_scene
def show_point(point: str | Point | tuple[float, float]):
    to_point(_scene, point).show_point = True


@on_scene
def hide_point(point: str | Point | tuple[float, float]):
    to_point(_scene, point).show_point = False


@on_scene
def move_label(point: str | Point | tuple[float, float],
               label_x: float = None,
               label_y: float = None,
               run_time: float = 0):
    to_point(_scene, point).move_label_to(label_dx=label_x, label_dy=label_y, run_time=run_time)


@on_scene
def points(*points_data):
    """
    Function for creation of multiple points
    :param points_data – strings of names or tuples (name, x, y)
    :return list[Point] – list of created points
    """
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
    return [
        Point(_scene, pointNames[0], get_position=lambda: segment_circle_intersection_positions(segment, circle)[0]),
        Point(_scene, pointNames[1], get_position=lambda: segment_circle_intersection_positions(segment, circle)[1])]


@on_scene
def intersect_figures(f1: str | Figure, f2: str | Figure, pointNames: tuple[str, str] = (None, None)):
    """
    Function for intersecting two figures (Circles or Segments)
    :param f1 - first figure or its label
    :param f2 - second figure or its label
    :param pointNames - names of intersection points
    """
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
    """
    Draw a circumcircle of a triangle
    :param triangle – Triangle object or its label
    :param circle_label – label for the circle
    :param center_name – name for the center point of a circle
    :return Circle – the circumscribed circle
    """
    triangle = to_figure(triangle)

    return triangle.circumscribed_circle(circle_label=circle_label, point_name=center_name)


@on_scene
def triangle_center(p1: str | Point | tuple[int | float, int | float],
                    p2: str | Point | tuple[int | float, int | float],
                    p3: str | Point | tuple[int | float, int | float],
                    pointName: str = None):
    """
    Draw a circum-centre of three points
    :param p1 – first vertex (Point or its name)
    :param p2 – second vertex (Point or its name)
    :param p3 – third vertex (Point or its name)
    :param pointName – name for the center point
    :return Point – the circumcenter
    """
    p1 = to_point(_scene, p1)
    p2 = to_point(_scene, p2)
    p3 = to_point(_scene, p3)

    return Point(_scene, name=pointName, get_position=tr.get_circumscribed_pos_r(p1, p2, p3)[0])


@on_scene
def triangle_orthocenter(triangle: str | Triangle,
                         label: str = None):
    triangle = to_figure(triangle)

    return Point(_scene, name=label,
                 get_position=lambda: get_orthocenter(triangle.p1, triangle.p2, triangle.p3))


@on_scene
def triangle_centroid(triangle: str | Triangle,
                         label: str = None):
    triangle = to_figure(triangle)

    return Point(_scene, name=label,
                 get_position=lambda: get_centroid(triangle.p1, triangle.p2, triangle.p3))


@on_scene
def move(point: str | Point | tuple[int | float, int | float],
         x: float,
         y: float,
         run_time=2):
    """
    Animate point to absolute coordinates
    :param point – the point or its name
    :param x – new X coordinate
    :param y – new Y coordinate
    :param run_time – duration of the animation
    """
    to_point(_scene, point).move(x, y, run_time=run_time)


@on_scene
def move_randomly(point: str | Point | tuple[int | float, int | float],
                  run_time=2):
    """
    Move point to a random position
    :param point – the point or its name
    :param run_time – duration of the movement
    """
    move(point, uniform(-3, 3), uniform(-3, 3), run_time=run_time)


@on_scene
def move_along_circle(point: str | Point | tuple[int | float, int | float],
                      circle: str | Circle,
                      run_time=4):
    """
    Move point along the full circle
    :param point – the point or its name
    :param circle – the circle or its label
    :param run_time – time for one full animation
    """
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
    """
    Tangents from an external point to a circle
    :param circle – the circle or its label
    :param point – the external point or its name
    :param pointNames – names for the points of tangency
    :param segment_labels – labels for the tangent segments
    :return list[Point] – the two points of tangency
    """
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
    """
    Drawing a midpoint of the arc
    :param p1 – first point on the circle or its name
    :param p2 – second point on the circle or its name
    :param circle – the circle or its label
    :param pointName – name for the new midpoint
    :return Point – midpoint of the arc
    """
    p1 = to_point(_scene, p1)
    p2 = to_point(_scene, p2)
    circle = to_figure(circle)

    return Point(_scene, name=pointName, get_position=lambda: arc_midpoint_pos(p1, p2, circle))


@on_scene
def inscribed_circle(triangle: str | Triangle,
                     pointName: str = None,
                     circle_label: str = None):
    """
    Creating a new circle - incircle of a triangle
    :param triangle – the triangle or its label
    :param pointName – name for the incenter
    :param circle_label – label for the circle
    :return Circle – the inscribed circle
    """
    triangle = to_figure(triangle)

    center = Point(_scene, name=pointName,
                   get_position=lambda: incenter_and_inradius(triangle.p1, triangle.p2, triangle.p3)[0])

    return Circle(_scene, center=center,
                  get_r=lambda: incenter_and_inradius(triangle.p1, triangle.p2, triangle.p3)[0], label=circle_label)


@on_scene
def inscribed_circle_center(triangle: str | Triangle,
                            label: str = None):
    triangle = to_figure(triangle)

    return Point(_scene, name=label,
                 get_position=lambda: incenter_and_inradius(triangle.p1, triangle.p2, triangle.p3)[0])


@on_scene
def point_on_circle(circle: str | Circle, pointName=None):
    """
    Random point on a circle
    :param circle – the circle or its label
    :param pointName – name for the new point
    :return Point – the random point on the circle
    """
    circle = to_figure(circle)

    cx, cy = circle.center.x, circle.center.y

    angle = uniform(0, TAU)
    x = cx + circle.r * cos(angle)
    y = cy + circle.r * sin(angle)

    return Point(_scene, name=pointName, x=x, y=y)


@on_scene
def move_points(points, positions, run_time=2):
    """
    Animate multiple points to new positions
    :param points – list of points
    :param positions – list of coordinates (x, y)
    :param run_time – duration of the animation
    """
    _scene.play(
        *[point.x_tracker.animate.set_value(new_x) for point, (new_x, _) in zip(points, positions)],
        *[point.y_tracker.animate.set_value(new_y) for point, (_, new_y) in zip(points, positions)],
        run_time=run_time
    )


@on_scene
def recenter_camera(point_cords=None, run_time=2):
    """
    Auto-fit all points into view
    :param point_cords – list of coordinates or None
    :param run_time – duration of the zoom animation
    """
    global _new_position

    points = point_names.values()

    if point_cords is None:
        point_cords = [(p.x, p.y) for p in points if p.active]

    if settings.recenter_with_circles:
        for figure in figures.figure_names.values():
            if isinstance(figure, Circle):
                x, y, r = figure.center.x, figure.center.y, figure.r
                point_cords.append((x + r, y))
                point_cords.append((x - r, y))
                point_cords.append((x, y - r))
                point_cords.append((x, y + r))

    # min_x = min(p[0] for p in point_cords)
    # max_x = max(p[0] for p in point_cords)
    # min_y = min(p[1] for p in point_cords)
    # max_y = max(p[1] for p in point_cords)

    # screen_scale = 0.9  # size of the screen without borders (border size is 0.1 of the screen)

    # width = (max_x - min_x) / screen_scale
    # height = (max_y - min_y) / screen_scale

    # center = (
    #    min_x + width / 2,
    #    min_y + height / 2
    # )

    center = (
        sum([p[0] for p in point_cords]) / len(point_cords),
        sum([p[1] for p in point_cords]) / len(point_cords)
    )

    # scale_x = _scene.camera.frame_width / width
    # scale_y = _scene.camera.frame_height / height

    dx = max([abs(p[0] - center[0]) for p in point_cords])
    dy = max([abs(p[1] - center[1]) for p in point_cords])

    dx_new = _scene.camera.frame_width / 2
    dy_new = _scene.camera.frame_height / 2

    scale_x = dx_new / dx
    scale_y = dy_new / dy

    scale_factor = min(scale_x, scale_y)

    def new_position(x, y):
        return (
            (x - center[0]) * scale_factor,
            (y - center[1]) * scale_factor
        )

    _new_position = new_position

    if points:
        move_points(points, [new_position(point.x, point.y) for point in points],
                    run_time=run_time)


@on_scene
def mark_equals(segments: list[str | Segment]):
    """
    Mark given segments as equal with a single tick
    :param segments – list of segments or their labels
    """
    for segment in segments:
        Tick(_scene, segment, segments[0])


@on_scene
def mark_all_equal_to(segment: str | Segment):
    """
    Tick every segment equal in length to the given one
    :param segment – the base segment or its label
    """
    segment = to_figure(segment)

    for figure in figures.figure_names.values():
        if isinstance(figure, Segment) and abs(segment.length - figure.length) < 1e-12:
            Tick(_scene, segment=figure, base_segment=segment)


@on_scene
def mark_equal_angles(angles: list[list[str | Point]]):
    """
    Mark several angles as equal
    :param angles – list of triplets of points [A, O, B]
    """
    for angle in angles:
        if len(angle) != 3:
            raise ValueError(f'The angle should consist from 3 points, not {len(angle)}.')
        ArcMark(_scene, *angle)
