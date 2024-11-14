import xml.etree.ElementTree as ET


def read_kml(kml_path):
    with open(kml_path, "r", encoding='utf-8') as f:  #打开文本
        kml_data = f.read()   #读取文本

    root = ET.fromstring(kml_data)
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    coordinates = root.find('.//kml:coordinates', namespace)
    coordinates_list = [tuple(map(float, coord.split(','))) for coord in coordinates.text.split()]
    return coordinates_list


def is_in_poly(p, poly):
    """
    :param p: [x, y]
    :param poly: [(x, y), (x, y), ( , ), (), ...]
    :return:
    """
    px, py = p
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        if len(corner) == 3:
            x1, y1, _ = corner
            x2, y2, _ = poly[next_i]
        else:
            x1, y1 = corner
            x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = not is_in
    return is_in