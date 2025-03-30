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
                    label = element.get("label")
                    if label in used:
                        continue
                    used[label] = True
                    element_type = element.get('type')
                    if element_type == 'point':
                        coords = element.find("coords")
                        x, y, z = float(coords.get("x")), float(coords.get("y")), float(coords.get("z"))
                        operations.append(f"Point(self, '{label}', {x}, {y})")

                elif element.tag == "command":
                    command_name = element.get("name")

                    if command_name == 'Segment':
                        inputs = element.find("input")
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = element.find("output").get('a0')
                        used[label] = True
                        # Updated to include the label in the operation
                        operations.append(f"Segment(self, '{a}', '{b}', '{label}')")

                    if command_name == 'Midpoint':
                        inputs = element.find("input")
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = element.find("output").get('a0')
                        used[label] = True
                        operations.append(f"midPoint(self, '{a}', '{b}', '{label}')")

                    if command_name == 'Polygon':
                        inputs = element.find("input")
                        outputs = element.find("output")
                        points = [inputs.get(f"a{i}") for i in range(len(inputs.attrib))]
                        labels = [outputs.get(f"a{i}") for i in range(len(outputs.attrib))]
                        for i in range(len(points)):
                            operations.append(
                                f"Segment(self, '{points[i]}', '{points[(i + 1) % len(points)]}', '{labels[i]}')"
                            )
                            used[labels[i]] = True

                    if command_name == 'Intersect':
                        inputs = element.find("input")
                        a, b, index_str = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        index = int(index_str) if index_str else None
                        outputs = element.find("output")
                        label = outputs.get('a0')
                        if label:
                            used[label] = True
                            if index is not None:
                                operations.append(f"intersect_figures('{a}', '{b}', '{label}', index={index})")
                            else:
                                operations.append(f"intersect_figures('{a}', '{b}', '{label}')")

                    if command_name == "Circle":
                        inputs = element.find("input")
                        center = inputs.get("a0")
                        radius_or_point = inputs.get("a1")
                        label = element.find("output").get("a0")

                        used[label] = True

                        try:
                            radius = float(radius_or_point)
                            # If a1 is a number, use it as the radius
                            operations.append(f"Circle(self, '{center}', {radius}, '{label}')")
                        except ValueError:
                            # If a1 is not a number, assume it's a point label (alternative case)
                            operations.append(f"Circle(self, '{center}', '{radius_or_point}', '{label}')")


    return operations