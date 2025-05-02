import argparse
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
{''.join([f'        {line}{nl}' for line in code_lines])}        self.wait(1)
"""
    return scene_code



parser = argparse.ArgumentParser(
    description="Generate a Manim scene script from a GeoGebra file"
)
parser.add_argument(
    'input_file',
    help='Path to the .ggb file'
)
parser.add_argument(
    '-o', '--output',
    default='generated_code_example.py',
    help='Path for the generated Python output file'
)
args = parser.parse_args()

operations = parse_xml.parse(args.input_file)

code = generate_manim_code(operations)

with open(args.output, 'w') as file:
    file.write(code)

print(f"Generated Manim code saved to '{args.output}'.")
