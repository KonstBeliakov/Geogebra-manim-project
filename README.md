# GeoGebra-Manim Project Setup & Run Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/KonstBeliakov/Geogebra-manim-project.git
   cd Geogebra-manim-project
   ```

2. **Create & activate a virtual environment**  
   - **Unix / macOS**  
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (PowerShell)**  
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

4. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the code generator**  
   ```bash
   python manim_code_generator.py path/to/input.ggb -o path/to/your/generated_code.py
   ```

6. **Render your Manim scene**  
   ```bash
   manim -pql generated_scene.py MyScene
   ```

### How to automatically create animated solutions for problems using this project?
1. Put file `open_ai_key` with your chatGpt API key in the folder of cloned repository.
2. Run file `gpt_solving_problems.py`.
3. Open directory `generation_attempt`. There will be a file `prompt.md` with prompt to gpt and file `solution.py` with generated manim code.
4. Run file `solution.py` to create and open the animation.
---




# Geometry in manim
Implementation of the main Geogebra methods in the python manim library
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
Example of usage of methods of `Triangle`:
```python
from manim import *
from triangle import Triangle


class Main(Scene):
    def construct(self):
        t = Triangle(self, 'A1', 'B1', 'C1')
        t.bisector('A1', 'B')
        t.median('A1', 'M')
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
### Circles
Creating a circle:
```python
from manim import Scene
from point import Point
from circle import Circle


class Main(Scene):
    def construct(self):
        A = Point(self, 'A', 0, 0)

        Circle(self, 'A')

        # The circle moves when we move its center
        A.move(1, 1)

        self.wait(1)
```