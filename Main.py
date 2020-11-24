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
