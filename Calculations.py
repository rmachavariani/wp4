import numpy as np
import time
import json
import math as m

import PullThroughCheck
import BearingCheck
import Forces


with open('data.json', 'r') as j:
    input_data = json.load(j)['input']

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
width = float(lug_data['width_plate'])
material = float(lug_data['material'])
thickness = float(lug_data['thickness_plate'])
wall_thickness = float(vehicle_wall_data['thickness'])
allowable_stress = float(lug_data['allowable_stress'])
wall_allowable_stress = float(vehicle_wall_data['allowable_stress'])

# Fastener data
edge_vertical = float(fastener_data['edge_vertical'])
diameter = float(fastener_data['outer_diameter'])
horizontal_spacing = float(fastener_data['horizontal_spacing'])
area = m.pi*((diameter/2)**2)

forces = Forces.calc_forces(mmoi, mass, angular_velocity, body_size, solar_panel_com, torques, launch_acceleration)

input_data['input']['forces'] = forces
with open('data.json', 'w') as j:
    json.dump(input_data, j)

