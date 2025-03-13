from random import randrange

from manim import *
from utils import *
from utils import _scene


class MultiplePointsAndScaling(MovingCameraScene):
    def construct(self):
        init(self)

        for i in range(1, 10):
            point('ABCDEFGHIJ'[i], randrange(-10 * i, 10 * i), randrange(-10 * i, 10 * i))
            recenter_camera(self)

        self.wait(1)


