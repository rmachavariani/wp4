import numpy as np
import time
import json
import math as m

import PullThroughCheck
import BearingCheck
import Forces
import Weight

with open('data.json', 'r+') as j:
    master_json_data = json.load(j)

for i in range(10):
    try:
        json_data = master_json_data['iterations']

        int_list = list(map(int, json_data.keys()))
        last_key = sorted(int_list)[-1]
        json_data = json_data[str(last_key)]

        input_data = json_data['input']
        spacecraft_data = input_data['spacecraft']
        lug_data = input_data['lug']
        fastener_data = input_data['fastener']
        vehicle_wall_data = input_data['vehicle_wall']

        # Spacecraft data
        mmoi = spacecraft_data['mmoi']
        mass = spacecraft_data['mass']
        angular_velocity = spacecraft_data['angular_velocity']
        body_size = spacecraft_data['body_size']
        solar_panel_com = spacecraft_data['solar_panel_com']
        torques = spacecraft_data['torques']
        launch_acceleration = 5 * 9.80665

        # Plate data
        width = float(lug_data['width_plate']) + 0.01
        height = float(lug_data['height']) + 0.01
        material = float(lug_data['material'])
        plate_thickness = float(lug_data['thickness_plate']) + 0.01
        wall_thickness = float(vehicle_wall_data['thickness']) + 0.01
        allowable_stress = float(lug_data['allowable_stress'])
        wall_allowable_stress = float(vehicle_wall_data['allowable_stress'])
        lug_thickness = float(lug_data['thickness_lug'])
        lug_length = float(lug_data['length_lug'])
        lug_density = float(lug_data['density'])
        hole_diameter = float(lug_data['hole_diameter'])

        # Fastener data
        inner_diameter = float(fastener_data['inner_diameter']) + 0.002
        outer_diameter = float(fastener_data['outer_diameter']) + 0.002
        edge_vertical = float(fastener_data['edge_vertical']) + 0.003
        horizontal_spacing = float(fastener_data['horizontal_spacing']) + 0.01
        fastener_density = float(fastener_data['density'])
        area = m.pi*((outer_diameter/2)**2)

        forces, moments = Forces.calc_forces(mmoi, mass, angular_velocity, body_size, solar_panel_com, torques, launch_acceleration)

        bearingCheck, coord_array, fastener_count = BearingCheck.bearing_check(height, outer_diameter, material, horizontal_spacing, area,
                                                               plate_thickness, wall_thickness, allowable_stress, wall_allowable_stress, forces)

        new_coordinates_array = []
        for fastener_coord in coord_array:
            new_coordinates_array.append([fastener_coord.x, fastener_coord.y])

        # Pull through check
        margin_back_plate, margin_vehicle_plate = PullThroughCheck.pull_through(outer_diameter, inner_diameter, fastener_count, plate_thickness, wall_thickness,
                                                                                allowable_stress, wall_allowable_stress, new_coordinates_array, forces[3][1], moments[3][2])

        # Weight
        weight_fastener = Weight.calc_weight_fasteners(plate_thickness, wall_thickness, outer_diameter, fastener_density)
        weight_attachment = Weight.calc_weight_attachment(plate_thickness, width, height, fastener_count, inner_diameter, lug_thickness, lug_length, hole_diameter, lug_density)

        # Update json file
        json_data['output']['bearing_check']['margins']['plate'] = bearingCheck[0]
        json_data['output']['bearing_check']['margins']['wall'] = bearingCheck[1]

        # Add pull through check
        for n, margin in enumerate(margin_back_plate):
            json_data['output']['pull_check']['margins']["plate-{}".format(n + 1)] = str(margin)

        for n, margin in enumerate(margin_vehicle_plate):
            json_data['output']['pull_check']['margins']["wall-{}".format(n + 1)] = str(margin)

        # Write back to document
        new_json_data = {}
        new_json_data[str(int(last_key) + 1)] = json_data

        master_json_data['iterations'].update(new_json_data)
    except ValueError:
        print("Error occurred, moving on to the next iteration")
        continue

with open('data_iterations.json', 'w+') as j:
    json.dump(master_json_data, j, indent=4, sort_keys=True)

