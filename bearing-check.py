import math as m

# Test Data
L = 2  # length of the backup plate
H = 2  # height of the backup plate
c_h = 1  # Horizontal Clearence
c_v = 1  # Vertical Clearence
R = 1  # Hole Radius
A = m.pi * pow(R, 2)

# Coordinates of a center of each fastener
x_1 = (L / 2) - (R / 2) - c_h
z_1 = (H / 2) - (R / 2) - c_v
x_2 = x_1
z_2 = -z_1
x_3 = -x_1
z_3 = z_1
x_4 = -x_1
z_4 = -z_1

# Calculates center of gravity
def cg(pos_1, pos_2, pos_3, pos_4, Area):
    pos_cg = (pos_1 + pos_2 + pos_3 + pos_4) * Area / (pos_1 + pos_2 + pos_3 + pos_4)
    return pos_cg


cg_x = cg(x_1, x_2, x_3, x_4, A)
cg_z = cg(z_1, z_2, z_3, z_4, A)
