#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path


def main():
    tests_dir  = Path('tests')
    output_dir = Path('test_output')
    output_dir.mkdir(parents=True, exist_ok=True)

    for ggb_file in sorted(tests_dir.glob('*.ggb')):
        name    = ggb_file.stem
        py_file = output_dir / f"{name}.py"

        # 1) generate the .py from the .ggb
        subprocess.run([
            sys.executable,                    # same Python interpreter
            'manim_code_generator.py',
            '-o', str(py_file),
            str(ggb_file)
        ], check=True)

        # 2) run Manim on the generated file
        #    capitalise first letter of name and append "Scene"
        scene_name = f"{name.capitalize()}Scene"
        subprocess.run([
            'manim',
            '-ql',                             # quick low-quality render
            str(py_file),
            scene_name,
            '-o', str(output_dir)
        ], check=True)


if __name__ == '__main__':
    main()
