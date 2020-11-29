def lug_thermal_stress(alpha_a, alpha_b, Eb, phi):  # phi to be imported from Q4.10
    """
    :param alpha_a: thermal expansion coefficient attachment / vehicle
    :param alpha_b: thermal expansion coefficient fastener
    :param Eb: E-modulus fastener
    :param phi: from fastener_type
    :return:
    """
    sigma_max = 5.44 * (alpha_a - alpha_b) * Eb * (1-phi)
    sigma_min = -46.63 * (alpha_a - alpha_b) * Eb * (1-phi)

    return sigma_max, sigma_min


def calc_thermal_stress(material_vehicle, material_attachment, material_fastener, phi):
    # Stress vehicle with fastener
    vehicle_stress = lug_thermal_stress(material_vehicle.alpha, material_fastener.alpha, material_fastener.e, phi)

    # Stress attachment with fastener
    attachment_stress = lug_thermal_stress(material_attachment.alpha, material_fastener.alpha, material_fastener.e, phi)

    return {"vehicle_stress": vehicle_stress, "attachment_stress": attachment_stress}
