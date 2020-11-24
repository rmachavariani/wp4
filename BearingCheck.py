# This is master file for bearing check
import json
import math as m
import numpy as np
from shapely.geometry import LineString, Point, box


def bearing_check():
    with open('data.json', 'r') as j:
        json_data = json.load(j)

    # Data sets
    json_input = json_data['input']
    back_plate_data = json_input['back_plate']
    vehicle_wall_data = json_input['vehicle_wall']
    fastener_data = json_input['fastener']

    width = float(back_plate_data['width'])
    edge_vertical = float(fastener_data['edge_vertical'])
    diameter = float(fastener_data['inner_diameter'])
    material = float(back_plate_data['material'])
    horizontal_spacing = float(fastener_data['horizontal_spacing'])
    area = m.pi*((diameter/2)**2)
    thickness = float(back_plate_data['thickness'])
    wall_thickness = float(back_plate_data['wall_thickness'])
    allowable_stress = float(back_plate_data['allowable_stress'])
    wall_allowable_stress = float(vehicle_wall_data['allowable_stress'])

    # Forces
    F_x = 200
    F_z = 200

    # Determining the required quantity of fasteners. Main things to determine: number of fasteners and their spacing
    # Things to keep in mind: type of material -> Two types of materials. If metal 2-3; if composite 4-5.
    fasteners = fastener_selection(width, edge_vertical, diameter, material)
    coordinates_array = get_coord_list(fasteners.fastener_count, diameter, horizontal_spacing, fasteners.spacing)
    cg = get_cg(coordinates_array, area, fasteners.fastener_count)

    # Update json file
    json_data['input']['fastener']['coord_list'] = str(coordinates_array)
    with open('data.json', 'w') as j:
        json.dump(json_input, j)

    for fastener_coord in coordinates_array:
        inplane_forces = get_inplane_forces(fasteners.fastener_count,
                                            fastener_coord.x,
                                            fastener_coord.y,
                                            cg[0], cg[1], F_x, F_z,
                                            coordinates_array)

        is_check_passed = get_stress_check(inplane_forces[0], inplane_forces[2], inplane_forces[1], diameter, thickness, wall_thickness, allowable_stress, wall_allowable_stress)
        return is_check_passed, coordinates_array


def fastener_selection(w, e1, d2, material):  # Width, Edge1, Diameter of Hole, Material Type
    # 1 indicates metal, 2 indicates composite
    if material == 1:
        fastener_spacing = 2
    elif material == 2:
        fastener_spacing = 4
    else:
        quit("Please indicate the material type")

    class output:
        def __init__(self):
            self.usable_length = w - 2 * e1  # determining the length where the fasteners can be
            print("Usable plate length: " + str(self.usable_length))
            self.fastener_count = int(((self.usable_length / d2) - 1) / fastener_spacing) + 1
            if self.fastener_count < 2:
                quit("Fastener count is less than 2. Process terminated.")
            print("Selected number of fasteners: " + str(self.fastener_count))
            self.spacing = (w - 2 * e1 - d2) / (self.fastener_count - 1)  # Final spacing between holes
            print("Distance between fasteners: " + str(self.spacing))

    return output()  # number of fastener and spacing between them


def get_coord_list(N, D, d, e_1):
    if (N % 2) == 0:
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

        for i, point in enumerate(coords_list):
            print("Fastener " + str(i + 1) + " coordinate: " + str(point.x) + "," + str(point.y))

        return coords_list
    else:
        quit("Number of fastener is not even. Please insert an even number.")


def get_cg(coords_list, area, N):
    sum_x = 0
    sum_y = 0
    for point in coords_list:
        sum_x = sum_x + area * point.x
        sum_y = sum_y + area * point.y

    pos_cg_x = sum_x/ (N * area)
    pos_cg_y = sum_y/ (N * area)

    print("Center of gravity position: " + str(pos_cg_x) + "," + str(pos_cg_y))

    return [pos_cg_x, pos_cg_y]


def SumR_Squared (coo,cg_x,cg_z): # is the sum of the square distances of each fastener to the c.g. of the fasteners
    R = []
    for i in coo:
        r_squared = (float(i[0])-cg_x)**2+(float(i[1])-cg_z)**2
        R.append(r_squared)
        S = sum(R)
    return S


def get_inplane_forces (n, x, z, cg_x, cg_z, F_x, F_z, coo):  #Required Variables: number of fast., coo single fast., S: see above, coo cg(4.5), force components (4.1)
    #check whether resultant of F_x and F_z acts through the cg of the fasteners
    F_inplane_x = F_x / n
    F_inplane_z = F_z / n

    new_coordinates_array = []
    for fastener_coord in coo:
        new_coordinates_array.append([fastener_coord.x, fastener_coord.y])

    coo = new_coordinates_array

    if cg_x == 0 and cg_z == 0:
        F_inplane_M = 0

    else: # the following vectors are treated as if they were in a regular x-y plane , the variables are however different: x -> z, y -> x (see drawing reference system)
        d = np.array([cg_z,cg_x]) # vector representing moment arm                              #     ^ x
        F = np.array([F_z,F_x]) # vector representing resultant force vector                    #     |
                                                                                                #     |
        M = abs(np.cross(d,F))
        r = m.sqrt((z-cg_z)**2+(x-cg_x)**2)
        S = SumR_Squared(coo,cg_x,cg_z)
        F_inplane_M = (M*r)/S    # looking at Eq 4.4 in the manual a more general version is represented, however since all cross-sectional areas will bes the same, this eqaution can be simplified by putting the area outside the summation, and thus cancelling out

    forces = np.array([F_inplane_x,F_inplane_z ,F_inplane_M])
    print("Inplane X Force: " + str(F_inplane_x) + "N")
    print("Inplane Z Force: " + str(F_inplane_z) + "N")
    print("Inplane Moment Force: " + str(F_inplane_M) + "N")

    return forces


def getResultant(F_x, F_y, F_z):
    R = m.sqrt(pow(F_x, 2) + pow(F_z, 2) + pow(F_y, 2))
    return R


def getBearingStress(P, D, t):
    sigma = P / (D * t)
    return sigma #1.5 margin of safety removed, and to be included in WP4.13


def isAllowable(sigma_allowable, sigma_bearing):
    result = sigma_allowable >= sigma_bearing
    if result:
        print("Allowable bearing stress check passed with bearing stress of " + str(sigma_bearing) + " Pa and allowable stress of " + str(sigma_allowable) + " Pa")
        return result
    else:
        print("Allowable bearing stress check not passed with bearing stress of " + str(sigma_bearing) + " Pa and allowable stress of " + str(sigma_allowable) + " Pa")
        quit('Bearing stress check not passed. Process terminated. ')


def get_stress_check (F_inplane_x, F_inplane_y, F_inplane_z, D, t, t_wall, sigma_allowable, sigma_wall_allowable):
    R = getResultant(F_inplane_x, F_inplane_y, F_inplane_z)
    sigma_bearing = getBearingStress(R, D, t)
    sigma_wall_bearing = getBearingStress(R, D, t_wall)

    print("Checking plate allowable stress:")
    isPlateAllowable = isAllowable(sigma_allowable, sigma_bearing)
    print("Checking wall allowable stress:")
    isWallAllowable = isAllowable(sigma_wall_allowable, sigma_wall_bearing)

    return isPlateAllowable, isWallAllowable


