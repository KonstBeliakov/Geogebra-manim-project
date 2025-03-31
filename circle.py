from manim import *
from figures import *
from settings import *
from point import Point, to_point


class Circle(Figure):
    def __init__(
        self,
        scene,
        center: Point | str | tuple[float, float] = None,
        r: float = 1,
        get_r=None,
        label: str = None
    ):
        """
        :param scene:  the scene where the circle will be drawn
        :param center: Point object, point name (if it doesn't exist, it will be created), or (x, y) tuple
        :param r:      radius of the circle (used only if get_r is None)
        :param get_r:  function (lambda) returning the current radius; if not None,
                       the circle will always use the radius from this function
        :param label:  label for the circle
        """
        self.scene = scene
        self.center = to_point(scene, center)

        self._get_radius = get_r

        if self._get_radius is None:
            self.r_tracker = ValueTracker(r)

        super().__init__(scene, label=label)

    @property
    def r(self) -> float:
        """
        Current radius value.
        If self._get_radius is defined, use its return value.
        Otherwise, use the value from r_tracker.
        """
        if self._get_radius is not None:
            return self._get_radius()
        return self.r_tracker.get_value()

    @r.setter
    def r(self, new_r: float):
        """
        Radius setter. Only works if _get_radius was not provided when the circle was created.
        """
        if self._get_radius is not None:
            raise ValueError("Cannot set r directly when using get_r for dynamic radius.")
        self.r_tracker.set_value(new_r)

    def render(self):
        # Create the circle with initial values
        circle = manim.Circle(
            radius=self.r,
            color=LINES_COLOR,
            fill_opacity=FIGURE_FILL_OPACITY
        )
        circle.move_to((self.center.x, self.center.y, 0))

        self.scene.play(Create(circle))
        self.scene.wait(0.3)

        # Update the circle when the center or radius changes
        def update_circle(m: manim.Circle):
            new_circle = manim.Circle(
                radius=self.r,
                color=LINES_COLOR,
                fill_opacity=FIGURE_FILL_OPACITY
            )
            new_circle.move_to((self.center.x, self.center.y, 0))
            # Merge the new circle into the old one for smooth animation
            m.become(new_circle)

        # Add the updater and return the circle to the scene
        circle.add_updater(update_circle)
        self.scene.add(circle)
