import Tension_Efficiency_Factors_Graphs


def stress_mode_tension(material, hole_diameter, thickness, w_over_d, force_y):

    stress_graph = 12
    margin_of_safety = 0.15
    t_list = []

    # Getting material properties
    # fill in a number for n which gets the ultimate
    sigma_ult = material.ult_stress

    # Getting the right curve
    K_tension = Tension_Efficiency_Factors_Graphs.tension_eff_graph(stress_graph, material.index_12, w_over_d)

    try:
        for i in range(5):
            w_over_d = w_over_d + 0.25
            for j in range(30):
                thickness = thickness + 0.05

                area_tension = hole_diameter * thickness * (w_over_d - 1)

                sigma_tu = force_y / (margin_of_safety * K_tension * area_tension)
                if float(sigma_ult) - float(sigma_tu) > 0:
                    t_list.append([w_over_d, thickness])
                    break

    except TypeError:
        print(f'Error occurred whilst calculating Stress Mode of the Lug; w_over_d {w_over_d}')

    return t_list



