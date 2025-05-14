import argparse
import sys

import parse_xml

def generate_manim_code(operations, _cords, _labels):
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
        recenter_camera({_cords})
        mark_used_labels_for_points({_labels})
        mark_used_labels_for_figures({_labels})
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

sys.stdout.reconfigure(encoding="utf-8")

args = parser.parse_args()

operations, labels = parse_xml.parse(args.input_file)

cords = parse_xml.get_coordinates(args.input_file)

code = generate_manim_code(operations, cords, labels)

with open(args.output, 'w', encoding='utf-8') as file:
    file.write(code)

print(f"Generated Manim code saved to '{args.output}'.")
