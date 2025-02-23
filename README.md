
##### Triangles
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
[triangle_examples.mp4](triangle_examples.mp4)
##### Segments
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

        # If points are not specified, they will be generated randomly
        s2 = Segment(self)

        self.wait(1)
```
[segment_examples.mp4](segment_examples.mp4)