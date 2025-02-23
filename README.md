
### Triangles
Creating triangles:
```python
from manim import *
from triangle import Triangle
from point import Point


class Main(Scene):
    def construct(self):
        Point(self, 'A', 0, 0)
        B = Point(self, 'B', 1, 1)
        C = Point(self, 'C', 1, 0)

        # we can draw a triangle by using existing points or their names
        Triangle(self, 'A', B, C)
        
        # if there is no such point, one it will be created
        Triangle(self, 'B', 'C', 'D')
        
        # we can specify only some of the points, and remaining will be generated (with random names)
        Triangle(self, 'D')
        
        self.wait(1)
```
### Segments
Creating segments:
```python
from manim import *
from point import Point
from segment import Segment


class Main(Scene):
    def construct(self):
        A = Point(self, 'A', 0, 0)
        Point(self, 'B', 1, 1)

        # We can create a segment using existing points or their names
        s1 = Segment(self, A, 'B')

        # If points are not specified (or there is no such point), they will be generated randomly
        s2 = Segment(self, 'T')

        # We can get a middle of the segment:
        M = s1.middle(name='M')

        # When we move the point A the point M will move too :)
        A.move(-1, 0)

        self.wait(1)
```
Intersection of the segments:
```python
from manim import *
from point import Point, get_point_by_name
from segment import Segment


class Main(Scene):
    def construct(self):
        Point(self, 'A', 0, 0)
        Point(self, 'B', 2, 2)

        Point(self, 'C', 2, 0)
        Point(self, 'D', 0, 2)

        s1 = Segment(self, 'A', 'B')
        s2 = Segment(self, 'C', 'D')

        X = s1.intersect(s2, 'X')

        get_point_by_name('A').move(0, 1.0)

        self.wait(1)
```