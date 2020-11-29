import math as m

import Shear_Bearing_Graphs
import Tension_Efficiency_Factors_Graphs

# e/D equal to 1 - assumption

def check_shear_bearing( hole_diameter, lug_thickness, edge_to_center_hole_distance,
                         tensile_load, material_ultimate_tensile_strength,
                         material_ultimate_compressive_strength):

    # 1 - shear-bearing failure
    margin_of_safety = 0.15
    material_ultimate_tensile_strength = material_ultimate_tensile_strength / margin_of_safety
    material_ultimate_compressive_strength = material_ultimate_compressive_strength / margin_of_safety
    x_input = edge_to_center_hole_distance / hole_diameter
    K_bru = Shear_Bearing_Graphs.shear_bearing_graph(13, hole_diameter/lug_thickness, x_input)
    A_br = hole_diameter * lug_thickness

    P_bru = K_bru * material_ultimate_tensile_strength * A_br

    # 2 - shear-bearing yield failure
    K_bry = Shear_Bearing_Graphs.shear_bearing_graph(14, hole_diameter/lug_thickness, x_input)
    P_bry = K_bry * material_ultimate_tensile_strength * A_br

    # 3 - bushing yield
    P_bush_y = 1.85 * material_ultimate_compressive_strength * A_br

    shear_bearing_margin = (P_bru/tensile_load) - 1
    shear_bearing_yield_margin = (P_bry/tensile_load) - 1
    bushing_margin = (P_bush_y/tensile_load) - 1

    return P_bru, P_bry, P_bush_y, shear_bearing_margin, shear_bearing_yield_margin, bushing_margin


def check_bolt_pin_bending(hole_diameter, lug_thickness, lug_height, edge_to_center_hole_distance,
                           material, transverse_load, axial_load, material_ultimate_tensile_strength,
                           ultimate_shear_bearing_failure):

    A1 = abs((lug_height - hole_diameter / m.sqrt(hole_diameter)) * lug_thickness)
    A2 = abs((lug_height - hole_diameter / 2) * lug_thickness)
    A3 = abs((edge_to_center_hole_distance - hole_diameter / 2) * lug_thickness)
    A4 = A1

    A_br = hole_diameter * lug_thickness
    A_av = 6 / (3 / A1 + 1 / A2 + 1 / A3 + 1 / A4)
    x_input = A_av / A_br

    K_tu = Tension_Efficiency_Factors_Graphs.tension_eff_graph(15, material.index_15, x_input)
    K_ty = Tension_Efficiency_Factors_Graphs.tension_eff_graph(15, material.index_15, x_input)
    K_tu_12 = Tension_Efficiency_Factors_Graphs.tension_eff_graph(12, material.index_12, x_input)

    ultimate_allowable_tension_load = 0.15 * K_tu_12 * A_br * material_ultimate_tensile_strength

    R_a = axial_load / min(ultimate_allowable_tension_load, ultimate_shear_bearing_failure)
    R_tr = pow((1 - pow(R_a, 1.6)), 0.8)
    margin_of_safety = 1 / pow((pow(R_a, 1.6) + pow(R_tr, 1.6)), 0.625) - 1

    P_tu_transverse = margin_of_safety * K_tu * A_br * material_ultimate_tensile_strength
    P_ty_transverse = margin_of_safety * K_ty * A_br * material_ultimate_tensile_strength

    ultimate_transverse_margin = (P_tu_transverse/transverse_load) - 1
    ultimate_transverse_yield_margin = (P_ty_transverse/transverse_load) - 1

    return P_tu_transverse, P_ty_transverse, ultimate_transverse_margin, ultimate_transverse_yield_margin