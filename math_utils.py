import math

from point import Point


def get_circumscribed_pos_r(p1: Point, p2: Point, p3: Point):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y

    D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    if abs(D) < 1e-9:
        raise ValueError(
            f"Triangle {p1}{p2}{p3} is degenerate or the points are collinear - cannot define a circumscribed circle.")

    Ux = ((x1 ** 2 + y1 ** 2) * (y2 - y3) +
          (x2 ** 2 + y2 ** 2) * (y3 - y1) +
          (x3 ** 2 + y3 ** 2) * (y1 - y2)) / D

    Uy = ((x1 ** 2 + y1 ** 2) * (x3 - x2) +
          (x2 ** 2 + y2 ** 2) * (x1 - x3) +
          (x3 ** 2 + y3 ** 2) * (x2 - x1)) / D

    r = math.sqrt((x1 - Ux) ** 2 + (y1 - Uy) ** 2)

    return (Ux, Uy), r
