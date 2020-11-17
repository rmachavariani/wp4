import math as m
from shapely.geometry import LineString, Point, box


# Test Data

e_2 = 1  # Horizontal Clearance
e_1 = 1  # Vertical Clearance
d = 1  # horizontal distance from z to hole
D = 1  # Hole Diameter
A = m.pi*(D/2)**2  # Hole Area
N = 8  # Number of holes


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


coords_list = get_coord_list(N, D, d, e_1)

def cg(coords_list, area):
    sum_x = 0
    sum_y = 0
    for point in coords_list:
        sum_x = sum_x + area * point.x
        sum_y = sum_y + area * point.y

    pos_cg_x = sum_x/ (N * area)
    pos_cg_y = sum_y/ (N * area)
    return [(pos_cg_x, pos_cg_y)]


cg = cg(coords_list, A)
print(cg)


