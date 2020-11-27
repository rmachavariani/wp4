import numpy as np

debug = False


def rotational(inertia, mass_object, body, torque, array_com):
    forces = np.zeros((4, 4))  # X, Y, Z, R
    moments = np.zeros((4, 4))  # X, Y, Z

    mass_solar_panels = float(mass_object['solar_panels'])
    inertia_solar_panels = inertia['solar_panel']
    inertia_total = inertia['total']
    inertia_body = inertia['body']

    v_max_x = float(torque['x']) / (float(inertia_total['x']) * 20 * (float(array_com['x']) + float(body['x'])))
    v_max_z = float(torque['z']) / (float(inertia_total['z']) * 20 * (float(array_com['x']) + float(body['x'])))

    # Forces around the x-axis:
    forces[0][1] = (mass_solar_panels * (pow(v_max_x, 2))) / (float(array_com['x']))
    forces[0][2] = (float(torque['x']) * (1 - float(inertia_body['x']) / float(inertia_total['x']) - 2 * (float(inertia_solar_panels['x']) / float(inertia_total['x'])))) / (float(body['x']))
    forces[0][3] = np.sqrt(forces[0][1] ** 2 + forces[0][2] ** 2)
    forces[0][0] = 0.1 * forces[0][3]
    # y-axis is not considered as it has no significant forces acting on it

    # Forces around the z-axis:
    forces[2][1] = (mass_solar_panels * (pow(v_max_z, 2))) / (float(array_com['x']))
    forces[2][0] = (float(torque['z']) * (1 - float(inertia_body['z']) / float(inertia_total['z']) - 2 * (float(inertia_solar_panels['z']) / float(inertia_total['z'])))) / float(body['x'])
    forces[2][3] = np.sqrt(forces[2][1] ** 2 + forces[2][0] ** 2)
    forces[2][2] = 0.1 * forces[2][3]

    # Moments around the z-axis:
    moments[2][2] = (mass_solar_panels * (float(array_com['x'])) * (float(array_com['x'])) * float(torque['z'])) / float(inertia_total['z'])

    # Total forces:
    forces[3] = np.sum(a=forces, axis=0) - forces[3]
    moments[3] = np.sum(a=moments, axis=0) - moments[3]

    if debug:
        print(forces)
        print(moments)

    return forces, moments


def launch(mass_object, launch_acceleration):
    forces = np.zeros((4, 4))  # X, Y, Z, R

    forces[3][2] = float(mass_object['solar_panels']) * launch_acceleration

    if debug:
        print(forces)

    return forces


def calc_forces(inertia, mass_object, body, torque, array_com, launch_acceleration):
    forces = np.zeros((4, 4))  # X, Y, Z, R

    """
    Resulting force an matrix matrix lay-out:
    around: | x | y | z | resultant |
    x-axis  |   |   |   |           |
    y-axis  |   |   |   |           | 
    z-axis  |   |   |   |           | 
    total   |   |   |   |           |  
    """

    rotational_forces, rotational_moments = rotational(inertia, mass_object, body, array_com, torque)
    launch_forces = launch(mass_object, launch_acceleration)

    for row in range(forces.shape[0]):
        for column in range(forces.shape[1]):
            forces[row][column] = max(rotational_forces[row][column], launch_forces[row][column])

    moments = rotational_moments
    print(forces)

    return forces, moments
