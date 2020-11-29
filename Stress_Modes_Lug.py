import Tension_Efficiency_Factors_Graphs


def stress_mode_tension(material, hole_diameter, thickness, w_over_d, force_y):

    stress_graph = 12
    margin_of_safety = 0.15

    # Getting material properties
    # fill in a number for n which gets the ultimate
    sigma_ult = material.ult_stress

    # Getting the right curve
    K_tension = Tension_Efficiency_Factors_Graphs.tension_eff_graph(stress_graph, material.index_12, w_over_d)

    try:
        area_tension = hole_diameter * thickness * (w_over_d - 1)

        sigma_tu = force_y / (margin_of_safety * K_tension * area_tension)
        margin = (sigma_ult / sigma_tu) - 1
        return margin

    except TypeError:
        print(f'Error occurred whilst calculating Stress Mode of the Lug; w_over_d {w_over_d}')
