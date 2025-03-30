from random import choice
from abc import ABC, abstractmethod

valid_figure_labels = [chr(i) for i in range(ord('a'), ord('z') + 1)]
figure_names = {}


def get_figure(label):
    if label not in figure_names:
        raise ValueError(f'There is no such figure with label "{label}".')
    return figure_names[label]


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
