import xml.etree.ElementTree as ET
import zipfile

def parse(ggb_file):
    with zipfile.ZipFile(ggb_file, 'r') as z:
        with z.open('geogebra.xml') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot().find("construction")

            operations = []
            used = {}

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
                        operations.append(f"Point(self, '{label}', {x}, {y})")
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
                        operations.append(f"Segment(self, '{a}', '{b}', '{label}')")

                    elif command_name == 'Midpoint':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"midPoint(self, '{a}', '{b}', '{label}')")

                    elif command_name == 'Polygon':
                        points = [inputs.get(f"a{i}") for i in range(len(inputs.attrib))]
                        labels = [outputs.get(f"a{i}") for i in range(len(outputs.attrib))]
                        for i in range(len(points)):
                            operations.append(
                                f"Segment(self, '{points[i]}', '{points[(i + 1) % len(points)]}', '{labels[i]}')"
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
                            operations.append(f"Circle(self, '{center}', {radius}, '{label}')")
                        except ValueError:
                            operations.append(f"Circle.from_three_points(self, '{center}', '{radius_or_point}', '{label}')")

                    elif command_name == "Alt":
                        a, b, c = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        d = outputs.get('a0')
                        operations.append(f"height('{a + b + c}', '{a + d}')")
                        used[d] = True

                    # todo
                    elif command_name == 'Line':
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"Line(self, '{a}', '{b}', '{label}')")

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


    return operations