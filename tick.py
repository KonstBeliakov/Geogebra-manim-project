from manim import *

from figures import to_figure
from segment import Segment
from settings import *


def tick_marker_position(s: Segment, base_segment: Segment = None):
    start_point = np.array((s.p1.x, s.p1.y, 0))
    end_point = np.array((s.p2.x, s.p2.y, 0))

    point = start_point + (end_point - start_point) * 0.5

    segment_vector = end_point - start_point
    norm = np.linalg.norm(segment_vector)
    if norm == 0:
        raise ValueError("The segment has zero length (p1 equals p2).")
    direction = segment_vector / norm

    # Compute the perpendicular vector (for 2D, z=0)
    perpendicular = np.array([-direction[1], direction[0], 0])

    if base_segment is not None and abs(s.length - base_segment.length) > 10**-12:
        return None

    return (point - (tick_length / 2) * perpendicular,
            point + (tick_length / 2) * perpendicular)


class Tick:
    def __init__(self, scene, segment: str | Segment, base_segment: str | Segment = None):
        self.scene = scene
        self.segment = to_figure(segment)
        self.base_segment = to_figure(base_segment)

        self.render()

    def render(self):
        def get_tick_line():
            positions = tick_marker_position(self.segment, self.base_segment)
            if positions is None:
                return VGroup()
            return Line(*positions, color=LINES_COLOR)

        line = always_redraw(get_tick_line)
        self.scene.play(Create(line))
