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
{''.join([f'        {line}{nl}' for line in code_lines])}
        self.wait(1)
"""
    return scene_code

operations = parse_xml.parse("test.ggb")

code = generate_manim_code(operations)

with open("generated_code_example.py", "w") as file:
    file.write(code)