import math as m

import Graphs


# e/D equal to 1 - assumption

def check_shear_bearing(hole_diameter, lug_thickness, edge_to_center_hole_distance, lug_allowable_stress,
                        material_index, material_tensile_strength, lug_yield_strength, compressive_yield_strength_bushing):
    # 1 - shear-bearing failure
    margin_of_safety = 0.15
    material_tensile_strength = material_tensile_strength / margin_of_safety
    x_input = edge_to_center_hole_distance / hole_diameter
    K_bru = Graphs.graph(13, material_index, x_input)
    A_br = hole_diameter * lug_thickness

    P_bru = K_bru * material_tensile_strength * A_br

    # 2 - shear-bearing yield failure
    K_bry = Graphs.graph(14, material_index, x_input)
    P_bry = K_bry * material_tensile_strength * A_br

    # 3 - bushing yield
    P_bush_y = 1.85 * compressive_yield_strength_bushing * A_br

    shear_bearing_margin = lug_allowable_stress - P_bru
    shear_bearing_yield_margin = lug_yield_strength - P_bry

    return P_bru, P_bry, P_bush_y, shear_bearing_margin, shear_bearing_yield_margin


def check_bolt_pin_bending(hole_diameter, lug_thickness, lug_height, edge_to_center_hole_distance,
                           lug_allowable_stress, material_index, material_tensile_strength, lug_yield_strength,
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

    P_tu = K_tu * A_br * material_tensile_strength
    P_ty = K_ty * A_br * lug_yield_strength


    R_a = axial_load / min(ultimate_allowable_tension_load, ultimate_shear_bearing_failure)
    R_tr = transverse_load / P_tu
    margin_of_safety = 1 / pow((pow(R_a, 1.6) + pow(R_tr, 1.6)), 0.625) - 1
