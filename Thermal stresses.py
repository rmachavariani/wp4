"""Thermal Stresses"""

def Thermalstress(DeltaT,alpha_a,alpha_b,E,delta_a,delta_b):
    sigma = DeltaT * (alpha_a-alpha_b) * E * (delta_b/(delta_b+delta_a))

    return sigma