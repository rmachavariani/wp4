import math as m
import sys

# Test Data
F_inplane_x = 1
F_inplane_z = 1
F_inplane_My = 1
R = 1
D = 1
t = 1
t_wall = 1
sigma_allowable = 1
sigma_wall_allowable = 1



def getResultant(F_x, F_y, F_z):
    R = m.sqrt(pow(F_x, 2) + pow(F_z, 2) + pow(F_y, 2))
    return R


def getBearingStress(P, D, t):
    sigma = P / (D * t)
    return 1.5*sigma #1.5 margin of safety


def isAllowable(sigma_allowable, sigma_bearing):
    result = sigma_allowable >= sigma_bearing
    if result:
        print("Allowable bearing stress check passed with bearing stress of" + str(sigma_bearing) + "Pa and allowable stress of" + str(sigma_allowable) + "Pa")
        return result
    else:
        print("Allowable bearing stress check not passed with bearing stress of " + str(sigma_bearing) + " Pa and allowable stress of " + str(sigma_allowable) + " Pa")
        sys.exit('Bearing stress check not passed. Process terminated. ')


def bearingCheck (F_inplane_x, F_inplane_y, F_inplane_z, D, t, t_wall, sigma_allowable, sigma_wall_allowable):
    P = getResultant(F_inplane_x, F_inplane_y, F_inplane_z)
    sigma_bearing = getBearingStress(P, D, t)
    sigma_wall_bearing = getBearingStress(R, D, t_wall)

    isPlateAllowable = isAllowable(sigma_allowable, sigma_bearing)
    isWallAllowable = isAllowable(sigma_wall_allowable, sigma_wall_bearing)

    return isPlateAllowable, isWallAllowable


bearingCheck(F_inplane_x, F_inplane_My, F_inplane_z, D, t, t_wall, sigma_allowable, sigma_wall_allowable)