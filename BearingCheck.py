# This is master file for bearing check
import math as m
import numpy as np
from shapely.geometry import LineString, Point, box

debug = False


def bearing_check(height, diameter, material, horizontal_spacing, area, thickness, wall_thickness, allowable_stress, wall_allowable_stress, forces, thermal_stresses):
    # Forces
    F_x = float(forces[3][0])
    F_z = float(forces[3][2])

    # Determining the required quantity of fasteners. Main things to determine: number of fasteners and their spacing
    # Things to keep in mind: type of material -> Two types of materials. If metal 2-3; if composite 4-5.
    fasteners = fastener_selection(height, diameter, material)
    coordinates_array = get_coord_list(fasteners.fastener_count, diameter, horizontal_spacing, fasteners.spacing)
    cg = get_cg(coordinates_array, area, fasteners.fastener_count)

    for fastener_coord in coordinates_array:
        inplane_forces = get_inplane_forces(fasteners.fastener_count,
                                            fastener_coord.x,
                                            fastener_coord.y,
                                            cg[0], cg[1], F_x, F_z,
                                            coordinates_array)

        margins = get_stress_check(inplane_forces[0], inplane_forces[2], inplane_forces[1], diameter, thickness, wall_thickness, allowable_stress,
                                   wall_allowable_stress, thermal_stresses)

        return margins, coordinates_array, fasteners.fastener_count


def fastener_selection(h, d2, material):  # height, Edge1, Diameter of Hole, Material Type
    # 1 indicates metal, 2 indicates composite
    e1 = 1.5 * d2
    if material == 1:
        fastener_spacing = 2
    elif material == 2:
        fastener_spacing = 4
    else:
        raise ValueError("Please indicate the material type")

    class output:
        def __init__(self):
            self.usable_length = h - 2 * e1  # determining the length where the fasteners can be
            if debug:
                print("Usable plate length: " + str(self.usable_length))
            self.fastener_count = 2 * (int(((self.usable_length / d2) - 1) / fastener_spacing) + 1)
            if self.fastener_count < 2:
                raise ValueError("Fastener count is less than 2. Process terminated.")
            if debug:
                print("Selected number of fasteners: " + str(self.fastener_count))
            self.spacing = (h - 2 * e1 - d2) / (self.fastener_count - 1)  # Final spacing between holes
            if debug:
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
        horizontal_splitters = [LineString([(minx, miny + i * dy), (maxx, miny + i * dy)]) for i in range(int(ny))]  # TEMP FIX
        coords_list = list()

        for splitter in horizontal_splitters:
            intersection = polygon.exterior.intersection(splitter)
            if intersection.is_empty:
                raise ValueError("Intersection failed. Process Terminated.")
            elif intersection.geom_type.startswith('Multi') or intersection.geom_type == 'GeometryCollection':
                for shp in intersection:
                    coords_list.append(shp)
            else:
                for i in intersection.coords:
                    coords_list.append(Point(i))

        for i, point in enumerate(coords_list):
            if debug:
                print("Fastener " + str(i + 1) + " coordinate: " + str(point.x) + "," + str(point.y))

        return coords_list
    else:
        raise ValueError("Number of fastener is not even. Please insert an even number.")


def get_cg(coords_list, area, N):
    sum_x = 0
    sum_y = 0
    for point in coords_list:
        sum_x = sum_x + area * point.x
        sum_y = sum_y + area * point.y

    pos_cg_x = sum_x/ (N * area)
    pos_cg_y = sum_y/ (N * area)

    if debug:
        print("Center of gravity position: " + str(pos_cg_x) + "," + str(pos_cg_y))

    return [pos_cg_x, pos_cg_y]


def SumR_Squared (coo,cg_x,cg_z): # is the sum of the square distances of each fastener to the c.g. of the fasteners
    R = []
    for i in coo:
        r_squared = (float(i[0])-cg_x)**2+(float(i[1])-cg_z)**2
        R.append(r_squared)
        S = sum(R)
    return S


def get_inplane_forces (n, x, z, cg_x, cg_z, F_x, F_z, coo):  # Required Variables: number of fast., coo single fast., S: see above, coo cg(4.5), force components (4.1)
    # Check whether resultant of F_x and F_z acts through the cg of the fasteners
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
        F_inplane_M = (M*r)/S  # Looking at Eq 4.4 in the manual a more general version is represented, however since all cross-sectional areas will bes the same, this eqaution can be simplified by putting the area outside the summation, and thus cancelling out

    forces = np.array([F_inplane_x,F_inplane_z ,F_inplane_M])
    if debug:
        print("Inplane X Force: " + str(F_inplane_x) + "N")
        print("Inplane Z Force: " + str(F_inplane_z) + "N")
        print("Inplane Moment Force: " + str(F_inplane_M) + "N")

    return forces


def getResultant(F_x, F_y, F_z):
    R = m.sqrt(pow(F_x, 2) + pow(F_z, 2) + pow(F_y, 2))
    return R


def getBearingStress(P, D, t, thermal_stress):
    # Get the maximum stress due to bearing stress and thermal stresses
    sigma = max(abs(P / (D * t) + thermal_stress[0]), abs(P / (D * t) + thermal_stress[1]))
    return sigma  # 1.5 margin of safety removed, and to be included in WP4.13


def isAllowable(sigma_allowable, sigma_bearing):
    margin = (sigma_allowable / sigma_bearing) - 1
    result = margin > 0
    if result:
        if debug:
            print("Allowable bearing stress check passed with bearing stress of " + str(sigma_bearing) + " Pa and allowable stress of " + str(sigma_allowable) + " Pa")
        return margin
    else:
        if debug:
            print("Allowable bearing stress check not passed with bearing stress of " + str(sigma_bearing) + " Pa and allowable stress of " + str(sigma_allowable) + " Pa")
        raise ValueError('Bearing stress check not passed. Process terminated. ')


def get_stress_check (F_inplane_x, F_inplane_y, F_inplane_z, D, t, t_wall, sigma_allowable, sigma_wall_allowable, thermal_stresses):
    R = getResultant(F_inplane_x, F_inplane_y, F_inplane_z)
    sigma_bearing = getBearingStress(R, D, t, thermal_stresses['attachment_stress'])
    sigma_wall_bearing = getBearingStress(R, D, t_wall, thermal_stresses['vehicle_stress'])

    if debug:
        print("Checking plate allowable stress:")

    isPlateAllowable = isAllowable(sigma_allowable, sigma_bearing)

    if debug:
        print("Checking wall allowable stress:")

    isWallAllowable = isAllowable(sigma_wall_allowable, sigma_wall_bearing)

    return isPlateAllowable, isWallAllowable


