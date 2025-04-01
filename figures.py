from random import choice
from abc import ABC, abstractmethod

valid_figure_labels = [chr(i) for i in range(ord('a'), ord('z') + 1)]
figure_names = {}


class Figure(ABC):
    def __init__(self, scene, label=None):
        if label is None:
            label = choice(valid_figure_labels)
        if label in figure_names:
            raise ValueError(f"The name {label} is already in use")
        self.label = label
        figure_names[label] = self

        if label in valid_figure_labels:
            valid_figure_labels.remove(label)

        self.scene = scene

        self.render()

    @abstractmethod
    def render(self):
        pass


def to_figure(figure: str | Figure):
    if isinstance(figure, str) and figure not in figure_names:
        raise ValueError(f'There is no such figure with label "{figure}".')
    if isinstance(figure, Figure):
        return figure
    return figure_names[figure]
