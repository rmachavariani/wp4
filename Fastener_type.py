from math import pi


def Fastener_Type(thickness_backplate, thickness_vehiclewall, inner_diameter_fastener, outer_diameter_fastener, youngs_modulus_backplate, youngs_modulus_fastener,
                  youngs_modulus_vehiclewall):

    t2 = thickness_backplate
    t3 = thickness_vehiclewall
    D_fi = inner_diameter_fastener
    D_fo = outer_diameter_fastener
    Eb = youngs_modulus_backplate
    Ef = youngs_modulus_fastener
    Ev = youngs_modulus_vehiclewall

    # Determining the typical substitution length
    L_nut = 0.4 * D_fo
    L_shank = t2 + t3
    L_head = 0.4 * D_fo  # Cylindrical Head
    L_eng = 0.4 * D_fi  # Nut-tightened

    # Area of the different parts of the bolt
    A_nut = pi * ((D_fo / 2) ** 2)
    A_shank = pi * ((D_fi / 2) ** 2)
    A_head = pi * ((D_fo / 2) ** 2)
    A_eng = pi * ((D_fi / 2) ** 2)

    try:
        # Calculating the delta for the back_plate
        delta_a1 = 4 * t2 / (Eb * pi * ((D_fo ** 2) - (D_fi ** 2)))

        # Calculating the delta for the vehicle wall
        delta_a2 = 4 * t3 / (Ev * pi * ((D_fo ** 2) - (D_fi ** 2)))

        # Calculating the delta for the bolt
        delta_b = (1 / Ef) * ((L_nut / A_nut) + (L_shank / A_shank) + (L_head / A_head) + (L_eng / A_eng))

        # Force ratio
        phi = (delta_a1 + delta_a2) / (delta_b + delta_a1 + delta_a2)
    except ZeroDivisionError:
        phi = None

    return phi
