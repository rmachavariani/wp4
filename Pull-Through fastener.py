
from math import pi

def pullthrough(a,b,c,d,e,f,g,h):
    #Constants
    n_f = a             #Number of fasteners
    D_fi = b            #Inner diameter of the fastener
    D_fo = c            #Outer diameter of the fastener
    F_y = d             #Tensile Force
    t2 = e              #Thickness of the plate
    t3 = f              #Thickness of the vehicle wall
    M_z = g             #Moment of the solar panel
    yieldstress = h     #Yield stress of the plates

    #Areas
    A_shear = pi * D_fo * (t2 + t3)
    A_tension = (1/4) * pi * (D_fi**2)

    #Distance between fastener and cg
    radii = [2, 3, 4, 5, 6]
    summation = A_tension * sum(radii)

    F_pi = F_y / n_f

    for radius in radii:

        #Forces on a fastener
        F_pMz = (M_z * radius * A_tension)/summation

        #Total Force and shear stress
        F_T = F_pi + F_pMz
        shearstress = F_T / A_shear

        if (shearstress > yieldstress):
            print(shearstress, 'Pull through occurs')

        else:
            print(shearstress, 'Its good!')


    return F_T

print(pullthrough(1,2,3,4,5,6,7,8))