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

def parse_global_info(tree):
    root = tree.getroot()

    ev = root.find(".//euclidianView")
    size = ev.find("size")
    width = float(size.get("width"))
    height = float(size.get("height"))

    cs = ev.find("coordSystem")

    scaleX = float(cs.get("scale"))
    scaleY = float(cs.get("yscale"))

    xZero  = float(cs.get("xZero"))
    yZero  = float(cs.get("yZero"))

    return {
            "width": width, "height": height,
            "scaleX": scaleX, "scaleY": scaleY,
            "xZero": xZero, "yZero": yZero
    }

def compute_screen_coords(view, x_geo, y_geo):
    """
    GeoGebra maps math‐coords (x_geo,y_geo) to screen pixels by:
      x_screen = xZero + x_geo * scaleX
      y_screen = yZero - y_geo * scaleY
    (screen‐y grows DOWN, so we subtract)
    """
    x_s = view["xZero"] + x_geo * view["scaleX"]
    y_s = view["yZero"] - y_geo * view["scaleY"]
    return x_s, y_s

def parse(ggb_file):
    with zipfile.ZipFile(ggb_file, 'r') as z:
        with z.open('geogebra.xml') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot().find("construction")

            view = parse_global_info(tree)


            operations = []
            used = {}
            triangle_heights = {}
            triangle_short_name = {}

            def parse_point(element):
                label = element.get("label").replace("'", "\\'")
                coords = element.find("coords")
                show = element.find("show")
                label_offset = element.find("labelOffset")

                x, y, z = float(coords.get("x")), float(coords.get("y")), float(coords.get("z"))

                x /= z
                y /= z

                show_label = show.get("label") == "true"
                x_geo_lab, y_geo_lab = None, None
                if label_offset is not None:
                    x_offset, y_offset = float(label_offset.get("x")), float(label_offset.get("y"))
                    x_s, y_s = compute_screen_coords(view, x, y)
                    x_label = x_s + x_offset
                    y_label = y_s + y_offset
                    x_geo_lab = (x_label - view["xZero"]) / view["scaleX"]
                    y_geo_lab = (view["yZero"] - y_label) / view["scaleY"]

                return {
                    "label" : label,
                    "x" : x,
                    "y" : y,
                    "show_label": show_label,
                    "x_offset": x_geo_lab,
                    "y_offset": y_geo_lab,
                }

            def procces_label_for_point(info):
                if info['show_label']:
                    operations.append(f"show_label('{info['label']}')")
                if info['x_offset'] or info['y_offset']:
                    operations.append(f"move_label('{info['label']}', {info['x_offset']}, {info['y_offset']})")

            for it in range(len(root)):
                element = root[it]
                if element.tag == "element":
                    label = element.get("label").replace("'", "\\'")
                    element_type = element.get('type')
                    if label in used:
                        if element_type == 'point':
                            info = parse_point(element)
                            procces_label_for_point(info)
                        continue
                    used[label] = True
                    if element_type == 'point':
                        info = parse_point(element)
                        operations.append(f"point('{label}', {info['x']}, {info['y']}, label_x={info['x_offset']}, label_y={info['y_offset']}, show_label={info['show_label']})")

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
                        continue

                    elif command_name == 'Polygon':
                        points = [inputs.get(f"a{i}") for i in range(len(inputs.attrib))]
                        labels = [outputs.get(f"a{i}") for i in range(len(outputs.attrib))]
                        if len(points) == 3:
                            operations.append(f"triangle('{points[0] + points[1] + points[2]}', '{labels[0]}', ['{labels[1]}', '{labels[2]}', '{labels[3]}'] )")
                            triangle_short_name[points[0] + points[1] + points[2]] = labels[0]
                            triangle_short_name[points[1] + points[2] + points[0]] = labels[0]
                            triangle_short_name[points[2] + points[0] + points[1]] = labels[0]
                            continue
                        for i in range(len(points)):
                            operations.append(
                                f"segment('{points[i]}', '{points[(i + 1) % len(points)]}', '{labels[i + 1]}')"
                            )
                            used[labels[i]] = True

                    elif command_name == 'Intersect':
                        a, b, index_str = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        labels = (outputs.get("a0"), outputs.get("a1"))
                        if len(labels) == 1:
                            labels = tuple(labels[0], None)
                        for label in labels:
                            if label:
                                used[label] = True
                        operations.append(f"intersect_figures('{a}', '{b}', {labels})")

                    elif command_name == "Circle":
                        center = inputs.get("a0")
                        radius_or_point = inputs.get("a1")
                        p = inputs.get("a2")
                        label = outputs.get('a0')
                        used[label] = True
                        try:
                            radius = float(radius_or_point)
                            operations.append(f"circle('{center}', {radius}, '{label}')")
                        except ValueError:
                            if not p:
                                operations.append(f"circle_from_two_points('{center}', '{radius_or_point}', '{label}')")
                            else:
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
                        continue

                    elif command_name == "Median":
                        a, b, c = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        point_name, x, y, median_name = outputs.get('a0'), outputs.get('a1'), outputs.get('a2'), outputs.get('a3')
                        used[point_name] = used[x] = used[y] = used[median_name] = True
                        operations.append(f"median('{a + b + c}', '{a + point_name}')")

                    elif command_name == "Bisector":
                        a, b, c = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        point_name, x, y, median_name = outputs.get('a0'), outputs.get('a1'), outputs.get('a2'), outputs.get('a3')
                        used[point_name] = used[x] = used[y] = used[median_name] = True
                        operations.append(f"bisector('{a + b + c}', '{a + point_name}')")

                    elif command_name == "TriangleCenter":
                        a, b, c, center_type = inputs.get('a0'), inputs.get('a1'), inputs.get('a2'), inputs.get('a3')
                        label = outputs.get('a0')
                        if center_type == "1":
                            continue
                            operations.append(f"inscribed_circle_center('{triangle_short_name[a + b + c]}', '{label}')")
                            used[label] = True
                            continue

                        if center_type == "4":
                            operations.append(f"triangle_orthocenter('{triangle_short_name[a + b + c]}', '{label}')")
                            used[label] = True
                            continue
                        if center_type != "4":  # todo
                            continue

                    elif command_name == "Mirror":
                        a, b = inputs.get('a0'), inputs.get('a1')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"reflect_point_about_line('{a}', '{b}', '{label}')")
                        continue

                    elif command_name == "Incircle":
                        a, b, c = inputs.get('a0'), inputs.get('a1'), inputs.get('a2')
                        label = outputs.get('a0')
                        used[label] = True
                        operations.append(f"inscribed_circle('{triangle_short_name[a + b + c]}', circle_label='{label}')")


    return operations, list(used.keys())
