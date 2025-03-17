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
                        operations.append(f"Point({x}, {y}, {z}, label = {label})") #todo

                elif element.tag == "command":

                    command_name = element.get("name")

                    if command_name == 'Segment':
                        inputs = element.find("input")
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = element.find("output").get('a0')
                        used[label] = True
                        operations.append(f"Segment({a}, {b}, {label})")
  
                    if command_name == 'Midpoint':
                        inputs = element.find("input")
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = element.find("output").get('a0')
                        used[label] = True
                        operations.append(f"Midpoint({a}, {b}, {label})")

                    if command_name == 'Polygon':
                        inputs = element.find("input")
                        outputs = element.find("output")
                        points = [inputs.get(f"a{i}") for i in range(len(inputs.attrib))]
                        labels = [outputs.get(f"a{i}") for i in range(len(outputs.attrib))]
                        for i in range(len(points)):
                            operations.append(f"Segment({points[i]}, {points[(i+1)%len(points)]}, {labels[i]})")
                            used[labels[i]] = True
    return operations

ans = parse("test1.ggb")

print(ans, sep="\n")
