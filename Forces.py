import numpy as np


def rotational(inertia, mass_object, a_velocity, body, torque, array_com):
    forces = np.zeros((4, 4))  # X, Y, Z, R
    moments = np.zeros((3, 4))  # X, Y, Z, R

    # x-axis is not considered as it has no significant forces acting on it

    # Forces around the y-axis:
    forces[1][0] = (mass_object['SolarPanels'] * (a_velocity[1] ** 2)) / (0.5 * array_com[0])
    forces[1][2] = (torque[1] * (1 + (4 * mass_object['SolarPanels'] * (0.5 * array_com[0]) * ((0.5 * array_com[0]) + (0.5 * body[2]))
                                      - inertia['Body'] - 2 * inertia["SolarPanelToCenter"]) / inertia['Total'])) / body[0]
    forces[1][3] = np.sqrt(forces[1][0] ** 2 + forces[1][2] ** 2)
    forces[1][1] = 0.1 * forces[1][3]

    # Moments around the y-axis:
    moments[1][1] = (mass_object['SolarPanels'] * (0.5 * array_com[1]) * ((0.5 * array_com[0]) + (0.5 * body[2])) * torque[1]) / inertia['Total']

    # Forces around the z-axis:
    forces[2][0] = (mass_object['SolarPanels'] * (a_velocity[1] ** 2)) / (0.5 * array_com[0])
    forces[2][1] = (torque[2] * (1 - inertia['Body'] / inertia['Total'] - 2 * (inertia['SolarPanelToCenter'] / inertia['Total']))) / (body[0])
    forces[2][3] = np.sqrt(forces[2][0] ** 2 + forces[2][1] ** 2)
    forces[2][2] = 0.1 * forces[2][3]

    # Total forces:
    forces[3] = np.sum(a=forces, axis=0) - forces[3]

    return forces, moments


def launch(mass_object, launch_acceleration):
    forces = np.zeros((4, 4))  # X, Y, Z, R

    forces[3][1] = mass_object['SolarPanels'] * launch_acceleration

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

    rotational_forces, rotational_moments = rotational(inertia, mass_object, a_velocity, body, torque, array_com)
    launch_forces = launch(mass_object, launch_acceleration)

    for row in range(forces.shape[0]):
        for column in range(forces.shape[1]):
            forces[row][column] = max(rotational_forces[row][column], launch_forces[row][column])

    print(rotational_forces)
    print(launch_forces)
    print(forces)


mass_moment_inertia = {'Body': 200.303, 'Total': 3502.037, 'SolarPanelToCenter': 1652.484}  # in kgm^2
masses = {'SolarPanels': 2 * 49.86, 'Body': 663.978}  # in kg
angular_velocity = np.array([1, 1, 1])
body_size = np.array([1.6, 2.3, 1.6])
solar_panel_com = np.array([6.8, 0, 0])
torques = np.array([20.125, 20.125, 20.125])

# Testing
calc_forces(mass_moment_inertia, masses, angular_velocity, body_size, torques, solar_panel_com, launch_acceleration=(5 * 9.80665))
