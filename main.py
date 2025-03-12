from manim import *
from utils import *


class Main(Scene):
    def construct(self):
        init(scene=self)

        triangle('ABC')

        median('ABC', "BM")
        bisector('ABC', 'BD')
        height('ABC', 'AH')

        move_randomly('A')
        move_randomly('B')
        move_randomly('C')

        #points(('E', -1, -1), ('F', 1, 1), ('G', -1, 1), ('I', 1, -1), 'U')

        #intersect('EF', 'GI', 'X')

        #move('E', -2, -1.2, run_time=0.5)
        #move_randomly('F', run_time=0.5)
