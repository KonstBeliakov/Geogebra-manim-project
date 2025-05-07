import xml.etree.ElementTree as ET
import zipfile


def get_coordinates(ggb_file):
    with zipfile.ZipFile(ggb_file, 'r') as z:
        with z.open('geogebra.xml') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot().find("construction")

            coordinates = []

            eps = 1e-9

            for element in root:
                if element.tag == "element":
                    element_type = element.get('type')
                    if element_type == 'point':
                        coords = element.find("coords")
                        x, y, z = float(coords.get("x")), float(coords.get("y")), float(coords.get("z"))
                        if abs(z) < eps:
                            continue
                        coordinates.append((x / z, y / z))

            return coordinates


def parse(ggb_file):
    with zipfile.ZipFile(ggb_file, 'r') as z:
        with z.open('geogebra.xml') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot().find("construction")

            operations = []
            used = {}
            triangle_heights = {}

            for element in root:
                if element.tag == "element":
                    label = element.get("label").replace("'", "\\'")
                    if label in used:
                        continue
                    used[label] = True
                    element_type = element.get('type')
                    if element_type == 'point':
                        coords = element.find("coords")
                        x, y, z = float(coords.get("x")), float(coords.get("y")), float(coords.get("z"))
                        operations.append(f"point('{label}', {x}, {y})")
                    elif element_type == 'vector':
                        coords = element.find("coords")
                        x, y, z = float(coords.get("x")), float(coords.get("y")), float(coords.get("z"))
                        operations.append(f"Vector(self, '{label}', {x}, {y})")

                elif element.tag == "command":
                    command_name = element.get("name")
                    inputs = element.find("input")
                    outputs = element.find("output")

                    for attr in inputs.attrib:
                        inputs.attrib[attr] = inputs.attrib[attr].replace("'", "\\'")

                    for attr in outputs.attrib:
                        outputs.attrib[attr] = outputs.attrib[attr].replace("'", "\\'")

                    if command_name == 'Segment':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"segment('{a}', '{b}', '{label}')")

                    elif command_name == 'Midpoint':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"midPoint('{a}', '{b}', '{label}')")

                    elif command_name == 'Polygon':
                        points = [inputs.get(f"a{i}") for i in range(len(inputs.attrib))]
                        labels = [outputs.get(f"a{i}") for i in range(len(outputs.attrib))]
                        for i in range(len(points)):
                            operations.append(
                                f"segment('{points[i]}', '{points[(i + 1) % len(points)]}', '{labels[i + 1]}')"
                            )
                            used[labels[i]] = True

                    elif command_name == 'Intersect':
                        a, b, index_str = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        labels = tuple(outputs.get(f'a{i}', None) for i in range(2))
                        for label in labels:
                            used[label] = True
                        operations.append(f"intersect_figures('{a}', '{b}', {labels})")

                    elif command_name == "Circle":
                        center = inputs.get("a0")
                        radius_or_point = inputs.get("a1")
                        label = outputs.get('a0')
                        used[label] = True
                        try:
                            radius = float(radius_or_point)
                            operations.append(f"circle('{center}', {radius}, '{label}')")
                        except ValueError:
                            p = inputs.get("a2")
                            operations.append(
                                f"circle_from_three_points('{center}', '{radius_or_point}', '{p}', '{label}')")

                    elif command_name == "Alt":
                        a, b, c = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        d = outputs.get('a0')
                        operations.append(f"height('{a + b + c}', '{a + d}')")
                        abc = [a, b, c]
                        abc.sort()
                        str = ''.join(abc)
                        if str not in triangle_heights:
                            triangle_heights[str] = []
                        triangle_heights[str].append(f'{a + d}')
                        used[d] = True

                    elif command_name == "TriangleCenter":
                        a, b, c, center_type = inputs.get('a0'), inputs.get('a1'), inputs.get('a2'), inputs.get('a3')
                        label = outputs.get('a0')
                        if center_type != "4":  # todo
                            continue
                        used[label] = True
                        abc = [a, b, c]
                        abc.sort()
                        str = ''.join(abc)
                        segments = triangle_heights.get(str)
                        operations.append(f"intersect_figures('{segments[0]}', '{segments[1]}', ('{label}'))")

                    elif command_name == "Mirror":
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"reflect_point_about_line('{a}', '{b}', '{label}')")
                    # todo
                    elif command_name == 'Line':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Line('{a}', '{b}', '{label}')")

                    elif command_name == 'Ray':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Ray(self, '{a}', '{b}', '{label}')")

                    elif command_name == 'Vector':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Vector(self, '{a}', '{b}', '{label}')")

                    elif command_name == 'PerpendicularLine':
                        point, line = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"PerpendicularLine(self, '{point}', '{line}', '{label}')")

                    elif command_name == 'ParallelLine':
                        point, line = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"ParallelLine(self, '{point}', '{line}', '{label}')")

                    elif command_name == 'Angle':
                        a, b, c = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Angle(self, '{a}', '{b}', '{c}', '{label}')")

                    elif command_name == 'Ellipse':
                        f1, f2, point = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Ellipse(self, '{f1}', '{f2}', '{point}', '{label}')")

                    elif command_name == 'Hyperbola':
                        f1, f2, point = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Hyperbola(self, '{f1}', '{f2}', '{point}', '{label}')")

                    elif command_name == 'Parabola':
                        focus, directrix = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Parabola(self, '{focus}', '{directrix}', '{label}')")

    return operations, list(used.keys())
