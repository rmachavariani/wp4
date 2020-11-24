from math import pi, sqrt
import json


def pull_through(forces, moments):
    with open('data.json', 'r') as j:
        json_input = json.load(j)['input']

    fastener = json_input['fastener']
    back_plate = json_input['back_plate']
    vehicle_wall = json_input['vehicle_wall']
    d_fo = fastener['outer_diameter']  # Outer diameter of the fastener
    d_fi = fastener['inner_diameter']  # Inner diameter of the fastener
    n_f = fastener['number']  # Number of fasteners
    t2 = back_plate['thickness']  # Thickness of the plate
    t3 = vehicle_wall['thickness']  # Thickness of the vehicle wall
    m_z = moments[3][1]  # Moment of the solar panel
    yield_stress_back_plate = back_plate['allowable_stress']  # Yield stress of the plates
    yield_stress_vehicle_plate = vehicle_wall['allowable_stress']
    list_coordinates = fastener['coord_list']

    f_y = forces[3][0]  # Tensile Force

    # Determining the shear yield stress
    shear_yield_stress_back_plate = yield_stress_back_plate / sqrt(3)
    shear_yield_stress_vehicle_plate = yield_stress_vehicle_plate / sqrt(3)

    # Areas
    a_shear = pi * d_fo * (t2 + t3)
    a_tension = (1 / 4) * pi * (d_fi ** 2)

    # Lists
    distances = []
    margin_back_plate = []
    margin_vehicle_plate = []

    # Distance between fastener and cg
    for hole in range(0, len(list_coordinates)):
        x_coord = list_coordinates[hole][0]
        z_coord = list_coordinates[hole][1]

        pythagoras = sqrt((x_coord ** 2) + (z_coord ** 2))
        distances.append(pythagoras)

    # Summation of the area multiplied by the distance
    summation = a_tension * sum(distances)

    # Force in the y-direction on each fastener
    force_pi = f_y / n_f

    # Calculating the shear stress on the fastener and the sheets
    n = 0
    for i in distances:

        # Forces on a fastener
        force_pmz = (-m_z * i * a_tension) / summation

        # Total Force and shear stress
        if list_coordinates[n][0] > 0:
            force_t = force_pi - force_pmz
            shear_stress = force_t / a_shear
        else:
            force_t = force_pi + force_pmz
            shear_stress = force_t / a_shear
        n = n + 1

        difference_back_plate = shear_stress - shear_yield_stress_back_plate
        difference_vehicle_plate = shear_stress - shear_yield_stress_vehicle_plate

        margin_back_plate.append(difference_back_plate)
        margin_vehicle_plate.append(difference_vehicle_plate)

    # Easy check to see if the structure will fail
    # print('Pull Through check for the back plate')
    # for j in margin_back_plate:
    #     if j >= 0:
    #         print('This fastener fails!!!!!!!!!!!!!!!!!')
    #     else:
    #         print('This configuration is fine')
    #
    # print('Pull through check for the vehicle plate')
    # for k in margin_vehicle_plate:
    #     if k >= 0:
    #         print('This fastener fails!!!!!!!!!!!!!!!!!')
    #     else:
    #         print('This configuration is fine')

    """
    margin is a list of the difference between shear stress and the yield stress.
    If the value is positive, if the margin is positive, then pull through occurs.
    """

    return margin_vehicle_plate, margin_back_plate
