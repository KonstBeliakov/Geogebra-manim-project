from random import choice
from abc import ABC, abstractmethod

from point import point_names, Point

valid_figure_labels = [chr(i) for i in range(ord('a'), ord('z') + 1)]
user_figure_labels = []
figure_names = {}


def mark_used_labels_for_figures(labels):
    global user_figure_labels
    user_figure_labels = labels


class Figure(ABC):
    def __init__(self, scene, label=None, render=True):
        if label is None:
            for l in valid_figure_labels:
                if l not in user_figure_labels:
                    label = l
            if label is None:
                label = choice(valid_figure_labels)
        if label in figure_names:
            print("DEBUG: ", user_figure_labels)
            raise ValueError(f"The name {label} is already in use")
        self.label = label
        figure_names[label] = self

        if label in valid_figure_labels:
            valid_figure_labels.remove(label)

        self.scene = scene

        if render:
            self.render()

    @abstractmethod
    def render(self):
        pass


def _segment_from_points(points: str | tuple[str, str] | list[str, str]):
    if not isinstance(points, (str, tuple, list)) or len(points) != 2:
        return None
    if not all(pt in point_names for pt in points):
        return None

    target = set(points)
    if len(target) != 2:
        return None
    for f in figure_names.values():
        if hasattr(f, 'p1') and hasattr(f, 'p2'):
            if {f.p1.name, f.p2.name} == target:
                return f
    return None


def to_figure(figure: str | Figure | Point) -> Figure | Point:
    if isinstance(figure, str):
        if figure in figure_names:
            return figure_names[figure]

        # trying to transform string like "AB" or a tuple like ("A1", "B1") into a segment
        segment = _segment_from_points(figure)

        if segment:
            return segment
        if figure in point_names:
            return point_names[figure]
        raise ValueError(f'There is no such figure with label "{figure}" or a segment with such points or a point with this name.')
    if isinstance(figure, Figure | Point):
        return figure
    raise TypeError(f'Can\'t transform type {type(figure)} to Figure.')
