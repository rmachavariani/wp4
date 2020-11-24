import numpy as np
from numba import njit
import time

import Calculations

# Starting values
# lug: [w, D_1, D_2, t_1, t_2, t_3]
lug = np.array([0, 0, 0, 0, 0, 0])

# fastener: [D_fo, D_fi, N]
fastener = np.array([0, 0, 0])

# fastener_grid: [[x1, y1], [x2, y2]]
fastener_gird = np.array([[0, 0], [0, 0]])


# Initialize calculation file
calculate = Calculations
calculate.singe_iteration(lug)


@njit()
def test_jit(variable):
    for i in range(len(variable)):
        for j in range(500):
            variable[i] += np.sqrt(1)
            variable[i] = np.sum(variable)

    return variable


def test(variable):
    for i in range(len(variable)):
        for j in range(50000):
            variable[i] += np.sqrt(500)

    return variable


# start_time = time.time()
# print(test(lug), time.time() - start_time)
start_time = time.time()
print(test_jit(lug), time.time() - start_time)
start_time = time.time()
print(test_jit(lug), time.time() - start_time)

