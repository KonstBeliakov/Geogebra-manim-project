import parse_xml


def generate_manim_code(operations):
    code_lines = []
    for op in operations:
        op_clean = ' '.join(op.split())
        code_lines.append(op_clean)
    nl = '\n'
    scene_code = f"""from manim import *
from point import *
from segment import *
from utils import *

class MyScene(Scene):
    def construct(self):
        init(self)
        recenter_camera()
{''.join([f'        {line}{nl}' for line in code_lines])}
        self.wait(1)
"""
    return scene_code

input_file = "usamo2025.ggb"
output_file = "generated_code_example"


operations = parse_xml.parse(input_file)

code = generate_manim_code(operations)

with open(output_file, "w") as file:
    file.write(code)