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


operations = []


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
    # ....
    #    color = get_color()
    #    operations.append(f"{draw_bisector.__name__}('{trianle_name}', {if color is not None "color={color}" else "")")
    #...
    #    draw_median()
    #...
    #    operations.append(f"{draw_point_on_circle.__name__}('{circle_name}', '{point_name}')")

    #...
    #    operations.append(f"{animate.__name__}('A')")
def to_code():
    with open('code.py', 'w', encoding='utf-8') as file:
        file.write(f"""
from manim import *
from utils import *


class Main(Scene):
    def construct(self):
        init(scene=self)
    {'\t\t\n'.join(operations)}""")

#operations.append('move_something()')


class TrilliumScene(Scene):
    def construct(self):
        parse(root, self)
        self.wait(1)
