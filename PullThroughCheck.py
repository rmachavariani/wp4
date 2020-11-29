from math import pi, sqrt

debug = False


def pull_through(d_fo, d_fi, n_f, t2, t3, yield_stress_back_plate, yield_stress_vehicle_plate, list_coordinates, f_y, m_z):
    # Determining the shear yield stress
    shear_yield_stress_back_plate = yield_stress_back_plate / sqrt(3)
    shear_yield_stress_vehicle_plate = yield_stress_vehicle_plate / sqrt(3)

    # Areas
    a_shear = pi * d_fo * (t2 + t3)
    a_tension = (1 / 4) * pi * (d_fi ** 2)

    # Lists
    distances1 = []
    distances2 = []
    margin_back_plate = []
    margin_vehicle_plate = []

    # Distance between fastener and cg
    for hole in range(0, len(list_coordinates)):
        x_coord = list_coordinates[hole][0]
        z_coord = list_coordinates[hole][1]

        pythagoras1 = sqrt((x_coord ** 2) + (z_coord ** 2))
        pythagoras2 = (x_coord ** 2) + (z_coord ** 2)
        distances1.append(pythagoras1)
        distances2.append(pythagoras2)

    # Summation of the area multiplied by the distance
    summation = a_tension * sum(distances2)

    # Force in the y-direction on each fastener
    force_pi = f_y / n_f

    # Calculating the shear stress on the fastener and the sheets
    n = 0
    for i in distances1:

        # Forces on a fastener
        force_pmz = (-m_z * i * a_tension) / summation

        # Total Force and shear stress
        if list_coordinates[n][0] > 0:
            force_t = force_pi - force_pmz
            shear_stress = force_t / a_shear
        else:
            force_t = force_pi + force_pmz
            shear_stress = force_t / a_shear
        if debug:
            print('tau = ', shear_stress)

        margin_back_plate.append((shear_yield_stress_back_plate / abs(shear_stress)) - 1)
        margin_vehicle_plate.append((shear_yield_stress_vehicle_plate / abs(shear_stress)) - 1)

        n = n + 1

    if debug:
        # Easy check to see if the structure will fail
        print('Pull Through check for the back plate')
        for j in margin_back_plate:
            if j >= 0:
                print('This fastener fails!!!!!!!!!!!!!!!!!')
            else:
                print('This configuration is fine')

        print('Pull through check for the vehicle plate')
        for k in margin_vehicle_plate:
            if k >= 0:
                print('This fastener fails!!!!!!!!!!!!!!!!!')
            else:
                print('This configuration is fine')

    """
    margin is a list of the difference between shear stress and the yield stress.
    If the value is positive, if the margin is positive, then pull through occurs.
    """

    return margin_back_plate, margin_vehicle_plate

#
# # Testing:
# def test():
#     coord_list = [[0.05, 0.04], [0.05, -0.04], [-0.05, 0.04], [-0.05, -0.04]]
#     test = pull_through(0.009, 0.006, 4, 0.002, 0.003, 503000000, 503000000, coord_list, 4888, 8.2)
#     print(test)
#
#     # d_fo, d_fi, n_f, t2, t3, yield_stress_back_plate, yield_stress_vehicle_plate, list_coordinates, f_y, m_z
#     # 4, b 0.006, c 0.009, d 5.73, e 0.002, f 0.003, g 8.12, h 3000000000, i 4000000000
#     # 4, d_fi 0.006, d_fo 0.009, fy 5.73, t2 0.002, t3 0.003, mz 8.12, yield bp 3000000000, yield_vp 4000000000
#
# test()