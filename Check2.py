import math as m

import Graphs

# e/D equal to 1 - assumption

def check_shear_bearing( hole_diameter, lug_thickness, edge_to_center_hole_distance,
                        material_index, material_tensile_strength, ultimate_tensile_strength, ultimate_compressive_strength):

    # 1 - shear-bearing failure
    margin_of_safety = 0.15
    ultimate_tensile_strength = ultimate_tensile_strength / margin_of_safety
    x_input = edge_to_center_hole_distance / hole_diameter
    K_bru = Graphs.graph(13, material_index, x_input)
    A_br = hole_diameter * lug_thickness

    P_bru = K_bru * ultimate_tensile_strength * A_br

    # 2 - shear-bearing yield failure
    K_bry = Graphs.graph(14, material_index, x_input)
    P_bry = K_bry * ultimate_tensile_strength * A_br

    # 3 - bushing yield
    P_bush_y = 1.85 * ultimate_compressive_strength * A_br

    shear_bearing_margin = P_bru - material_tensile_strength
    shear_bearing_yield_margin = P_bry - material_yield_strength
    bushing_margin = P_bush_y - material_yield_strength

    return P_bru, P_bry, P_bush_y, shear_bearing_margin, shear_bearing_yield_margin, bushing_margin


def check_bolt_pin_bending(hole_diameter, lug_thickness, lug_height, edge_to_center_hole_distance,
                            material_index, material_tensile_strength, lug_yield_strength,
                           axial_load, transverse_load, ultimate_allowable_tension_load,
                           ultimate_shear_bearing_failure):

    A1 = (lug_height - hole_diameter / m.sqrt(hole_diameter)) * lug_thickness
    A2 = (lug_height - hole_diameter / 2) * lug_thickness
    A3 = (edge_to_center_hole_distance - hole_diameter / 2) * lug_thickness
    A4 = A1

    A_br = hole_diameter * lug_thickness
    A_av = 6 / (3 / A1 + 1 / A2 + 1 / A3 + 1 / A4)
    x_input = A_av / A_br

    K_tu = Graphs.graph(15, material_index, x_input)
    K_ty = Graphs.graph(15, material_index, x_input)

    R_a = axial_load / min(ultimate_allowable_tension_load, ultimate_shear_bearing_failure)
    R_tr = pow((1 - pow(R_a, 1.6)), 0.8)
    margin_of_safety = 1 / pow((pow(R_a, 1.6) + pow(R_tr, 1.6)), 0.625) - 1

    P_tu_transverse = margin_of_safety * K_tu * A_br * transverse_load
    P_ty_transverse = margin_of_safety * K_ty * A_br * transverse_load

    ultimate_transverse_margin = material_tensile_strength - P_tu_transverse
    ultimate_transverse_yield_margin = material_yield_strength - P_ty_transverse

    return P_tu_transverse, P_ty_transverse, ultimate_transverse_margin, ultimate_transverse_yield_margin