from manim import *
from point import *
from segment import *
from utils import *

class MyScene(Scene):
    def construct(self):
        Point(self, 'A', -14.947803120349704, 13.312261154757058)
        Point(self, 'B', -18.722496317277116, 1.7784763863677011)
        Point(self, 'C', -4.4625442399957835, 1.7784763863677011)
        Segment(self, 'A', 'B', 't1')
        Segment(self, 'B', 'C', 'c')
        Segment(self, 'C', 'A', 'a')
        Circle.from_three_points(self, 'A', 'E', 'd')
        intersect_figures('d', 'a', ('F', 'G'))
        Point(self, 'G', 7.765263787272861, 1.7784763863677007)
        Segment(self, 'H', 'D', 'h')
        Segment(self, 'D', 'H'', 'i')
        Segment(self, 'F', 'C', 'j')
        Segment(self, 'C', 'G', 'k')

        self.wait(1)
