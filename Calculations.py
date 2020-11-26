import numpy as np
import time
import json
import math as m

import PullThroughCheck
import BearingCheck
import Forces
import Weight

with open('data.json', 'r+') as j:
    json_data = json.load(j)

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

# Lug data
width = float(lug_data['width_plate'])
height = float(lug_data['height'])
material = float(lug_data['material'])
plate_thickness = float(lug_data['thickness_plate'])
wall_thickness = float(vehicle_wall_data['thickness'])
lug_thickness = float(lug_data['thickness_lug'])
lug_length = float(lug_data['length_lug'])
hole_diameter = float(lug_data['hole_diameter'])
lug_density = float(lug_data['density'])
allowable_stress = float(lug_data['allowable_stress'])
wall_allowable_stress = float(vehicle_wall_data['allowable_stress'])

# Fastener data
inner_diameter = float(fastener_data['inner_diameter'])
outer_diameter = float(fastener_data['outer_diameter'])
number = float(fastener_data['number'])
edge_vertical = float(fastener_data['edge_vertical'])
diameter = float(fastener_data['outer_diameter'])
horizontal_spacing = float(fastener_data['horizontal_spacing'])
fastener_density = float(fastener_data['density'])
area = m.pi * ((diameter / 2) ** 2)

# Get forces
forces, moments = Forces.calc_forces(mmoi, mass, angular_velocity, body_size, solar_panel_com, torques, launch_acceleration)

# Checks
# Bearing checks
bearingCheck, coord_array = BearingCheck.bearing_check(width, edge_vertical, diameter, material, horizontal_spacing, area,
                                                       plate_thickness, wall_thickness, allowable_stress, wall_allowable_stress, forces)

new_coordinates_array = []
for fastener_coord in coord_array:
    new_coordinates_array.append([fastener_coord.x, fastener_coord.y])

# Pull through check
margin_back_plate, margin_vehicle_plate = PullThroughCheck.pull_through(outer_diameter, inner_diameter, number, plate_thickness, wall_thickness,
                                                                        allowable_stress, wall_allowable_stress, new_coordinates_array, forces[3][1], moments[3][2])

# Weight
weight_fastener = Weight.calc_weight_fasteners(plate_thickness, wall_thickness, outer_diameter, fastener_density)
weight_attachment = Weight.calc_weight_attachment(plate_thickness, width, height, number, inner_diameter, lug_thickness, lug_length, hole_diameter, lug_density)

# Update json file
# Add forces
print(forces)
for force in forces[-1]:
    print(force)

# Add bearing check
json_data['output']['bearing_check']['margins']['plate'] = str(bearingCheck[0])
json_data['output']['bearing_check']['margins']['wall'] = str(bearingCheck[1])

# Add pull through check
for i, margin in enumerate(margin_back_plate):
    json_data['output']['pull_check']['margins'][f'plate-{i + 1}'] = str(margin)

for i, margin in enumerate(margin_vehicle_plate):
    json_data['output']['pull_check']['margins'][f'wall-{i + 1}'] = str(margin)

# Write back to document
with open('data.json', 'w+') as j:
    json.dump(json_data, j)
