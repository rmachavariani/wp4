from math import pi, sqrt
from numba import njit
import numpy as np
import time


@njit()
def pull_through_jit(lug, fastener, fastener_grid, forces, moments, material):
    """
    Variables
    lug: [0-w, 1-D_1, 2-D_2, 3-t_1, 4-t_2, 5-t_3]
    fastener: [0-D_fo, 1-D_fi, 2-N]
    fastener_grid: [0-[x1, y1], 1-[x2, y2]]
    material: [0-YieldStress_BackPlate, 1-YieldStress_VehiclePlate]
    """

    # Determining the shear yield stress
    shear_yield_stress_back_plate = material[0] / sqrt(3)
    shear_yield_stress_vehicle_plate = material[1] / sqrt(3)

    # Areas
    # Area shear = pi * D_fo * (t2 + t3)
    a_shear = pi * fastener[0] * (lug[4] + lug[4])
    # Area tension = (1/4) * pi * (D_fi**2)
    a_tension = (1 / 4) * pi * (fastener[1] ** 2)

    # Lists
    distances = np.zeros(len(fastener_grid))
    margin_back_plate = np.zeros(len(fastener_grid))
    margin_vehicle_plate = np.zeros(len(fastener_grid))

    # Distance between fastener and cg
    for radius in range(len(fastener_grid)):
        x_coord = fastener_grid[radius][0]
        z_coord = fastener_grid[radius][1]

        pythagoras = sqrt((x_coord ** 2) + (z_coord ** 2))
        distances[radius] = pythagoras

    # Summation of the area multiplied by the distance
    summation = a_tension * np.sum(distances)

    # Force in the y-direction on each fastener
    force_pi = forces[3][0] / fastener[2]

    # Calculating the shear stress on the fastener and the sheets
    n = 0
    for i in range(len(distances)):

        # Forces on a fastener
        force_mpz = (-moments[3][1] * distances[i] * a_tension) / summation

        # Total Force and shear stress
        if fastener_grid[n][0] > 0:
            f_t = force_pi - force_mpz
            shear_stress = f_t / a_shear
        else:
            f_t = force_pi + force_mpz
            shear_stress = f_t / a_shear
        n = n + 1

        difference_back_plate = shear_stress - shear_yield_stress_back_plate
        difference_vehicle_plate = shear_stress - shear_yield_stress_vehicle_plate

        margin_back_plate[i] = difference_back_plate
        margin_vehicle_plate[i] = difference_vehicle_plate

    # Easy check to see if the structure will fail
    print('Pull Through check for the back-plate')
    for j in margin_back_plate:
        if j >= 0:
            print('This fastener fails!!!!!!!!!!!!!!!!!')
        else:
            print('This configuration is fine')

    print('Pull through check for the vehicleplate')
    for k in margin_vehicle_plate:
        if k >= 0:
            print('This fastener fails!!!!!!!!!!!!!!!!!')
        else:
            print('This configuration is fine')

    """
    margin is a list of the difference between shear stress and the yield stress.
    If the value is positive, if the margin is positive, then pull through occurs.
    """

    return margin_vehicle_plate, margin_back_plate


def pull_through(lug, fastener, fastener_grid, forces, moments, material):
    """
    Variables
    lug: [0-w, 1-D_1, 2-D_2, 3-t_1, 4-t_2, 5-t_3]
    fastener: [0-D_fo, 1-D_fi, 2-N]
    fastener_grid: [0-[x1, y1], 1-[x2, y2]]
    material: [0-YieldStress_BackPlate, 1-YieldStress_VehiclePlate]
    """

    n_f = fastener[2]  # Number of fasteners
    D_fi = fastener[1]  # Inner diameter of the fastener
    D_fo = fastener[0]  # Outer diameter of the fastener
    F_y = forces[3][0]  # Tensile Force
    t2 = lug[4]  # Thickness of the plate
    t3 = lug[5]  # Thickness of the vehicle wall
    M_z = moments[3][1]  # Moment of the solar panel
    yieldstress_backplate = material[0]  # Yield stress of the plates
    yieldstress_vehicleplate = material[1]
    listcoordinates = fastener_grid

    # Determining the shear yield stress
    shearyieldstress_backplate = yieldstress_backplate / sqrt(3)
    shearyieldstress_vehicleplate = yieldstress_vehicleplate / sqrt(3)

    # Areas
    A_shear = pi * D_fo * (t2 + t3)
    A_tension = (1 / 4) * pi * (D_fi ** 2)

    # Lists
    distances = []
    margin_backplate = []
    margin_vehicleplate = []

    # Distance between fastener and cg
    for radius in range(0, len(listcoordinates)):
        x_coord = listcoordinates[radius][0]
        z_coord = listcoordinates[radius][1]

        pythagoras = sqrt((x_coord ** 2) + (z_coord ** 2))
        distances.append(pythagoras)

    # Summation of the area multiplied by the distance
    summation = A_tension * sum(distances)

    # Force in the y-direction on each fastener
    F_pi = F_y / n_f

    # Calculating the shear stress on the fastener and the sheets
    n = 0
    for i in distances:

        # Forces on a fastener
        F_pMz = (-M_z * i * A_tension) / summation

        # Total Force and shear stress
        if (listcoordinates[n][0] > 0):
            F_T = F_pi - F_pMz
            shearstress = F_T / A_shear
        else:
            F_T = F_pi + F_pMz
            shearstress = F_T / A_shear
        n = n + 1

        difference_backplate = shearstress - shearyieldstress_backplate
        difference_vehicleplate = shearstress - shearyieldstress_vehicleplate

        margin_backplate.append(difference_backplate)
        margin_vehicleplate.append(difference_vehicleplate)

    # Easy check to see if the structure will fail
    print('Pull Through check for the backplate')
    for j in margin_backplate:
        if j >= 0:
            print('This fastener fails!!!!!!!!!!!!!!!!!')
        else:
            print('This configuration is fine')

    print('Pull through check for the vehicleplate')
    for k in margin_vehicleplate:
        if k >= 0:
            print('This fastener fails!!!!!!!!!!!!!!!!!')
        else:
            print('This configuration is fine')

    """
    margin is a list of the difference between shear stress and the yield stress.
    If the value is positive, if the margin is positive, then pull through occurs.
    """

    return margin_vehicleplate, margin_backplate
