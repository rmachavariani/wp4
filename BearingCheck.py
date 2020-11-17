# This is master file for bearing check
import json
import math as m
from shapely.geometry import LineString, Point, box



with open('data.json', 'r') as j:
    input = json.load(j)['input']


def bearing_check(input):
    plate_data = input['plate']
    fastener_data = input['fastener']

    fasteners = fastener_selection(int(plate_data['width']),
                                   int(fastener_data['edge_vertical']),
                                   int(fastener_data['diameter']),
                                   int(plate_data['material']))
    coordinates_array = get_coord_list(fasteners.fastener_count,
                                       int(fastener_data['diameter']),
                                       int(fastener_data['horizontal_spacing']),
                                       fasteners.spacing)
    cg = get_cg(coordinates_array,
                m.pi*(int(fastener_data['diameter']/2)**2),
                fasteners.fastener_count)



#
# Determing the required quantity of fasteners. Main things to determine: number of fasteners and their spacing
# Things to keep in mind: type of material -> Two types of materials. If metal 2-3; if composite 4-5.
def fastener_selection(w, e1, d2, material):  # Width, Edge1, Diameter of Hole, Material Type
    # 1 indicates metal, 2 indicates composite
    if material == 1:
        fastener_spacing = 2
    elif material == 2:
        fastener_spacing = 4
    else:
        return print("Please indicate the material type")

    class output:
        def __init__(self):
            self.usable_length = w - 2 * e1 # determining the length where the fasteners can be
            self.fastener_count = int(((self.usable_length / d2) - 1) / fastener_spacing) + 1
            self.spacing = (w - 2 * e1 - d2) / (self.fastener_count - 1)  # Final spacing between holes

    return output()  # number of fastener and spacing between them

def get_coord_list(N, D, d, e_1):
    if (N % 2) == 0 and N != 0:
        x_max = D / 2 + d
        z_max = ((N / 2 - 1) * D + (N / 2 - 1) * e_1) / 2

        polygon = box(-x_max, -z_max, x_max, z_max)
        ny = N / 2

        minx, miny, maxx, maxy = polygon.bounds

        dy = D + e_1
        horizontal_splitters = [LineString([(minx, miny + i * dy), (maxx, miny + i * dy)]) for i in range(int(ny))]
        coords_list = list()

        for splitter in horizontal_splitters:
            intersection = polygon.exterior.intersection(splitter)
            if intersection.is_empty:
                quit("Intersection failed. Process Terminated.")
            elif intersection.geom_type.startswith('Multi') or intersection.geom_type == 'GeometryCollection':
                for shp in intersection:
                    coords_list.append(shp)
            else:
                for i in intersection.coords:
                    coords_list.append(Point(i))
        return coords_list
    else:
        quit("Number of fastener is not even or equal to 0. Please insert an even number.")

def get_cg(coords_list, area, N):
    sum_x = 0
    sum_y = 0
    for point in coords_list:
        sum_x = sum_x + area * point.x
        sum_y = sum_y + area * point.y

    pos_cg_x = sum_x/ (N * area)
    pos_cg_y = sum_y/ (N * area)
    return [(pos_cg_x, pos_cg_y)]









check = bearing_check(input)
print(check)

# with open('data.json', 'r+') as file:
#     json_data = json.load(file)
#
#
#     json.dump(array, file)