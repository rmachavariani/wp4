import numpy as np
import time

import PullThroughCheck
import BearingCheck
import BearingCheckJit


def singe_iteration(lug):
    pass


# testing
"""
Variables
lug: [0-w, 1-D_1, 2-D_2, 3-t_1, 4-t_2, 5-t_3]
fastener: [0-D_fo, 1-D_fi, 2-N]
fastener_grid: [0-[x1, y1], 1-[x2, y2]]
material: [0-YieldStress_BackPlate, 1-YieldStress_VehiclePlate]
"""

# Test Values
lug_test = np.array([2, 2, 2, 2, 2, 2])
fastener_test = np.array([3, 3, 3])
fastener_grid_test = np.array([[2, 3], [4, 5]])

forces_test = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
moments_test = np.array([[50, 60, 70], [90, 100, 110], [130, 140, 150], [170, 180, 190]])

print(forces_test)
print(moments_test)

material_test = np.array([200, 300])

# Initialize PullThroughCheck
pull_through = PullThroughCheck.pull_through(lug_test, fastener_test, fastener_grid_test, forces_test, moments_test, material_test)
pull_through_jit = PullThroughCheck.pull_through_jit(lug_test, fastener_test, fastener_grid_test, forces_test, moments_test, material_test)

# Test functions
start_time = time.time()
margin_1, margin_2 = pull_through
print("Normal", margin_1, margin_2, f"in {time.time() - start_time} sec")

start_time = time.time()
margin_1, margin_2 = pull_through_jit
print("Jit", margin_1, margin_2, f"in {time.time() - start_time} sec")

# Initialize BearingCheck
bearing_check_jit = BearingCheckJit.bearing_check(lug_test, fastener_test, fastener_grid_test, forces_test, moments_test, material_test)

# Test functions
start_time = time.time()
margin_1, margin_2 = bearing_check_jit
print("Normal", margin_1, margin_2, f"in {time.time() - start_time} sec")
