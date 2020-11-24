"""Total Weight  Attachment"""
import math as m
import json


def calc_weight_fasteners():
    with open('data.json', 'r') as j:
        json_data = json.load(j)["input"]

    # Data sets
    back_plate = json_data["back_plate"]
    vehicle_wall = json_data["vehicle_wall"]
    fastener = json_data["fastener"]

    length = float(back_plate["thickness"]) + float(vehicle_wall["thickness"])  # minimum length bolt
    height_nut = float(fastener["outer_diameter"]) / 2  # arbitrary
    volume_nut = (m.pi * float(fastener["outer_diameter"]) ** 2) / 4 * height_nut
    volume_bolt = (m.pi * float(fastener["inner_diameter"]) ** 2) / 4 * length
    total_volume = volume_bolt + 2 * volume_nut  # volume nut counted twice as there is one on either side

    weight_fastener = float(fastener["density"]) * total_volume

    return weight_fastener


def calc_weight_attachment():
    with open('data.json', 'r') as j:
        json_data = json.load(j)["input"]

    # Data sets
    back_plate = json_data["back_plate"]
    lug = json_data["lug"]
    fastener = json_data["fastener"]

    volume_backup_plate = float(back_plate["thickness"]) * float(back_plate["width"]) * float(back_plate["height"]) \
                          - fastener["number"] * (m.pi * fastener["inner_diameter"] ** 2) / 4 * back_plate["thickness"]
    volume_lug = lug["thickness"] * lug["width"] * (lug["height"] - (lug["width"] - lug["hole_diameter"]) / 2 - lug["hole_diameter"] / 2) \
                 + lug["thickness"] * (m.pi * lug["width"] ** 2) / 8 - lug["width"] * (m.pi * lug["hole_diameter"] ** 2) / 4

    total_volume = volume_backup_plate + lug["number"] * volume_lug

    weight_attachment = lug["density"] * total_volume

    return weight_attachment


print(calc_weight_attachment())
print(calc_weight_fasteners())
