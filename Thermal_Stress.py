def lug_thermal_stress(alpha_a, alpha_b, Eb, phi):  # phi to be imported from Q4.10
    sigma_max = 5.44 * (alpha_a - alpha_b) * Eb * (1-phi)
    sigma_min = -46.63 * (alpha_a - alpha_b) * Eb * (1-phi)
    return sigma_max, sigma_min
