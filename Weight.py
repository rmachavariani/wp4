"""Total Weight Attachment"""
import math as m


def calc_mass_fasteners(plate_thickness, wall_thickness, outer_diameter, fastener_density):
    length = plate_thickness + wall_thickness  # minimum length bolt
    height_nut = outer_diameter / 2  # arbitrary
    volume_nut = (m.pi * outer_diameter ** 2) / 4 * height_nut
    volume_bolt = (m.pi * outer_diameter ** 2) / 4 * length
    total_volume = volume_bolt + 2 * volume_nut  # volume nut counted twice as there is one on either side

    weight_fastener = fastener_density * total_volume

    return weight_fastener


def calc_mass_attachment(plate_thickness, width, height, number, inner_diameter, lug_thickness, lug_length, hole_diameter, lug_density):
    volume_backup_plate = plate_thickness * width * height - number * (m.pi * inner_diameter ** 2) / 4 * plate_thickness
    volume_lug = (lug_thickness * m.pi * height ** 2) / 4 + 2 * (lug_length - height) * height * lug_thickness - (lug_thickness * m.pi * hole_diameter ** 2) / 8

    total_volume = volume_backup_plate + number * volume_lug

    print(f"mass {total_volume} {lug_density}")
    weight_attachment = lug_density * total_volume

    return weight_attachment
