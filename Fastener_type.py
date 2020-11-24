from math import pi

def Fastener_Type(thickness_backplate, inner_diameter_fastener, outer_diameter_fastener, youngs_modulus_backplate, youngs_modulus_fastener):
    t = thickness_backplate
    D_fi = inner_diameter_fastener
    D_fo = outer_diameter_fastener
    Eb = youngs_modulus_backplate
    Ef = youngs_modulus_fastener

    #Determining the typical substitution length
    L_nut = 0.4 * D_fo
    L_shank = 0.4 * D_fi
    L_head = 0.5 * D_fo         #Hexagonal Head
    L_eng = 0.4 * D_fi

    #Area of the different parts of the bolt
    A_nut = pi * ((D_fo/2)**2)
    A_shank = pi * ((D_fi/2)**2)
    A_head = pi * ((D_fo/2)**2)
    A_eng = pi * ((D_fi/2)**2)

    # Calculating the delta for the backplate
    delta_a = 4 * t / (Eb * pi * ((D_fo ** 2) - (D_fi ** 2)))

    #Calculating the delta for the bolt
    delta_b = (1/Ef)*((L_nut/A_nut) + (L_shank/A_shank) + (L_head/A_head)) + (L_eng/(A_eng*Ef))

    #Force ratio
    phi = delta_a/(delta_b + delta_a)

    return phi
