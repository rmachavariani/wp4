import numpy as np
import time
import json
import math as m

import PullThroughCheck
import BearingCheck
import Forces


def singe_iteration(lug):
    pass

with open('data.json', 'r') as j:
    input = json.load(j)['input']

spacecraft_data = input['spacecraft']
plate_data = input['plate']
fastener_data = input['fastener']

#spacecraft data
mmoi = spacecraft_data['mmoi']
mass = spacecraft_data['mass']
angular_velocity = spacecraft_data['angular_velocity']
body_size = spacecraft_data['body_size']
solar_panel_com = spacecraft_data['solar_panel_com']
torques = spacecraft_data['torques']
launch_acceleration = 5 * 9.80665

# plate data
width = float(plate_data['width'])
material = float(plate_data['material'])
thickness = float(plate_data['thickness'])
wall_thickness = float(plate_data['wall_thickness'])
allowable_stress = float(plate_data['allowable_stress'])
wall_allowable_stress = float(plate_data['wall_allowable_stress'])

# fastener data
edge_vertical = float(fastener_data['edge_vertical'])
diameter = float(fastener_data['diameter'])
horizontal_spacing = float(fastener_data['horizontal_spacing'])
area = m.pi*((diameter/2)**2)

forces = Forces.calc_forces(mmoi, mass, angular_velocity, body_size, solar_panel_com, torques, launch_acceleration)
print(forces)


# # Initialize PullThroughCheck
# pull_through = PullThroughCheck.pull_through(lug_test, fastener_test, fastener_grid_test, forces_test, moments_test, material_test)
# pull_through_jit = PullThroughCheck.pull_through_jit(lug_test, fastener_test, fastener_grid_test, forces_test, moments_test, material_test)
#
# # Test functions
# start_time = time.time()
# margin_1, margin_2 = pull_through
# print("Normal", margin_1, margin_2, f"in {time.time() - start_time} sec")
#
# start_time = time.time()
# margin_1, margin_2 = pull_through_jit
# print("Jit", margin_1, margin_2, f"in {time.time() - start_time} sec")
#
# # Initialize BearingCheck
# bearing_check_jit = BearingCheckJit.bearing_check(lug_test, fastener_test, fastener_grid_test, forces_test, moments_test, material_test)
#
# # Test functions
# start_time = time.time()
# margin_1, margin_2 = bearing_check_jit
# print("Normal", margin_1, margin_2, f"in {time.time() - start_time} sec")
