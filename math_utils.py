import math

from point import Point


def get_distance(A, B):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

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


def incenter_and_inradius(p1: Point, p2: Point, p3: Point):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y

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


def find_tangent_circle_intersections(circle, point):
    px, py = point.x, point.y
    cx, cy = circle.center.x, circle.center.y
    r = circle.r

    dx = px - cx
    dy = py - cy

    d_sq = dx * dx + dy * dy
    d = math.sqrt(d_sq)

    # If the point coincides with the center and radius > 0 — tangents are undefined
    if d == 0 or d < r:
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


def segment_circle_intersection_positions(segment, circle):
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

    if math.dist(intersections[0], intersections[1]) < 10 ** -9:
        intersections[1] = None

    return intersections


def circle_intersection_positions(circle1, circle2):
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

    if math.dist(intersection1, intersection2) < 10 ** -6:
        return intersection1, None

    return intersection1, intersection2


def arc_midpoint_pos(p1, p2, circle):
    cx, cy = circle.center.x, circle.center.y
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y

    d1 = math.hypot(x1 - cx, y1 - cy)
    d2 = math.hypot(x2 - cx, y2 - cy)

    if abs(d1 - circle.r) > 10 ** -6:
        raise ValueError(f'Points {p1} is not on the circle {circle}')

    if abs(d2 - circle.r) > 10 ** -6:
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


def get_orthocenter(p1: Point, p2: Point, p3: Point) -> (float, float):
    """
    Return the orthocenter (Hx, Hy) of triangle p1, p2, p3.
    Raises ValueError if the points are collinear (no unique orthocenter).
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y

    # Compute the same D and circumcenter U = (Ux, Uy) as in your function
    D = 2 * (x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    if abs(D) < 1e-9:
        raise ValueError(
            f"Triangle {p1}, {p2}, {p3} is degenerate or the points are collinear; "
            "no unique orthocenter."
        )

    Ux = ((x1**2 + y1**2)*(y2 - y3) +
          (x2**2 + y2**2)*(y3 - y1) +
          (x3**2 + y3**2)*(y1 - y2)) / D

    Uy = ((x1**2 + y1**2)*(x3 - x2) +
          (x2**2 + y2**2)*(x1 - x3) +
          (x3**2 + y3**2)*(x2 - x1)) / D

    # Orthocenter H = A + B + C - 2*O
    Hx = x1 + x2 + x3 - 2 * Ux
    Hy = y1 + y2 + y3 - 2 * Uy

    return Hx, Hy


def get_centroid(p1: Point, p2: Point, p3: Point) -> (float, float):
    """
    Return the centroid (intersection of the medians) of triangle p1,p2,p3.
    Raises ValueError if the points are collinear.
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y

    # Check for degeneracy via area = 0
    area2 = x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)
    if abs(area2) < 1e-9:
        raise ValueError(
            f"Triangle {p1}, {p2}, {p3} is degenerate or collinear; no unique centroid."
        )

    Cx = (x1 + x2 + x3) / 3.0
    Cy = (y1 + y2 + y3) / 3.0
    return Cx, Cy
