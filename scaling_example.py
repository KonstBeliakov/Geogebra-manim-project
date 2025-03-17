from manim import *
from utils import *


class MultiplePointsAndScaling(MovingCameraScene):
    def construct(self):
        init(self)

        for i in range(1, 10):
            point('ABCDEFGHIJ'[i], i * 10, i * 10)
            recenter_camera()

        self.wait(1)


