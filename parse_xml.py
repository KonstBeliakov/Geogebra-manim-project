import xml.etree.ElementTree as ET

from manim import *


tree = ET.parse('test1.xml')
root = tree.getroot()


def draw_point(scene, name, x, y, z):
    dot = Dot(point=np.array([x, y, z]), color=BLUE)
    scene.add(dot)

    point_name_text = Text(name, font_size=30)
    point_name_text.move_to((x, y + 0.3, 0))
    scene.play(Write(point_name_text))


def parse(element: ET.Element, scene):
    for obj_child in element:
        parse(obj_child, scene)
    if 'type' in element.attrib:
        if element.attrib['type'] == 'point':
            for child in element:
                if child.tag == 'coords':
                    draw_point(name=element.get('label'),
                               x=float(child.get('x')),
                               y=float(child.get('y')),
                               z=float(child.get('z'))
                               )


class TrilliumScene(Scene):
    def construct(self):
        parse(root, self)
        self.wait(1)
