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
                print(element)
                if element.tag == "element":
                    label = element.get("label")

                    if label in used:
                        continue
                    used[label] = True
                    element_type = element.get('type')

                    if element_type == 'point':
                        coords = element.find("coords")
                        x, y, z = float(coords.get("x")), float(coords.get("y")), float(coords.get("z"))
                        operations.append(f"Point({x}, {y}, {z}, label = {label})") #todo

                elif element.tag == "command":

                    command_name = element.get("name")

                    if command_name == 'Segment':
                        refs = element.find("input")
                        a, b = refs.get('a0'), refs.get('a1')
                        label = element.find("output").get('a0')
                        operations.append(f"Segment({a}, {b}, {label})")

                    if command_name == 'Midpoint':
                        refs = element.find("input")
                        a, b = refs.get('a0'), refs.get('a1')
                        label = element.find("output").get('a0')
                        operations.append(f"Midpoint({a}, {b}, {label})")

                    if command_name == 'Polygon':
                        inputs = element.find("input")
                        outputs = element.find("output")
                        points = [inputs.get(f"a{i}") for i in range(len(inputs.attrib))]
                        labels = [outputs.get(f"a{i}") for i in range(len(outputs.attrib))]
                        for i in range(len(points)):
                            operations.append(f"Segment({points[i]}, {points[(i+1)%len(points)]}, {labels[i]})")
    return operations

ans = parse("test1.ggb")

print(ans, sep="\n")
