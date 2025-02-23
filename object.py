from abc import abstractmethod


class Object:
    def __init__(self, scene):
        self.scene = scene
        self.dependent_objects = []

    def update(self):
        self.transform()
        for obj in self.dependent_objects:
            obj.update()

    def add_dependent(self, obj):
        self.dependent_objects.append(obj)

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def transform(self):
        pass
