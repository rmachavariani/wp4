import numpy as np

debug = True


def rotational(inertia, mass_object, a_velocity, body, torque, array_com):
    forces = np.zeros((4, 4))  # X, Y, Z, R
    moments = np.zeros((4, 4))  # X, Y, Z

    mass_solar_panels = float(mass_object['solar_panels'])
    inertia_solar_panels = float(inertia['solar_panel'])
    inertia_total = float(inertia['total'])
    inertia_body = float(inertia['body'])

    # Forces around the x-axis:
    forces[0][1] = (mass_solar_panels * (float(a_velocity['y']) ** 2)) / (0.5 * float(array_com['x']))
    forces[0][2] = (float(torque['z']) * (1 - inertia_body / inertia_total - 2 * (inertia_solar_panels / inertia_total))) / (float(body['x']))
    forces[0][3] = np.sqrt(forces[0][1] ** 2 + forces[0][2] ** 2)
    forces[0][0] = 0.1 * forces[0][3]
    # y-axis is not considered as it has no significant forces acting on it

    # Forces around the z-axis:
    forces[2][1] = (mass_solar_panels * (pow(float(a_velocity['y']), 2))) / (0.5 * float(array_com['x']))
    forces[2][0] = (float(torque['y']) * (1 - inertia_body/inertia_total - 2 * (inertia_solar_panels/inertia_total))) / float(body['x'])
    forces[2][3] = np.sqrt(forces[2][1] ** 2 + forces[2][0] ** 2)
    forces[2][2] = 0.1 * forces[2][3]

    # Moments around the z-axis:
    moments[2][2] = (mass_solar_panels * (0.5 * float(array_com['x'])) * ((0.5 * float(array_com['x'])) + (0.5 * float(body['z']))) * float(torque['y'])) / inertia_total

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


def calc_forces(inertia, mass_object, a_velocity, body, torque, array_com, launch_acceleration):
    forces = np.zeros((4, 4))  # X, Y, Z, R

    """
    Resulting force an matrix matrix lay-out:
    around: | x | y | z | resultant |
    x-axis  |   |   |   |           |
    y-axis  |   |   |   |           | 
    z-axis  |   |   |   |           | 
    total   |   |   |   |           |  
    """

    rotational_forces, rotational_moments = rotational(inertia, mass_object, a_velocity, body, array_com, torque)
    launch_forces = launch(mass_object, launch_acceleration)

    for row in range(forces.shape[0]):
        for column in range(forces.shape[1]):
            forces[row][column] = max(rotational_forces[row][column], launch_forces[row][column])

    moments = rotational_moments

    return forces, moments
