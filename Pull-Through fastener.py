from math import pi, sqrt

def pullthrough(fastener_count,b,c,d,e,f,g,h,i):
    #Variables
    n_f = fastener_count        #Number of fasteners
    D_fi = b                    #Inner diameter of the fastener
    D_fo = c                    #Outer diameter of the fastener
    F_y = d                     #Tensile Force
    t2 = e                      #Thickness of the plate
    t3 = f                      #Thickness of the vehicle wall
    M_z = g                     #Moment of the solar panel
    yieldstress = h             #Yield stress of the plates
    listcoordinates = i         #List of the coordinates of the fasteners

    #Determining the shear yield stress
    shearyieldstress = yieldstress/sqrt(3)

    #Areas
    A_shear = pi * D_fo * (t2 + t3)
    A_tension = (1/4) * pi * (D_fi**2)

    #Lists
    distances = []
    margin = []

    #Distance between fastener and cg
    for radius in range(0, len(listcoordinates)):
        x_coord = listcoordinates[radius][0]
        z_coord = listcoordinates[radius][1]

        pythagoras = sqrt((x_coord**2) + (z_coord**2))
        distances.append(pythagoras)

    #Summation of the area multiplied by the distance
    summation = A_tension * sum(distances)

    #Force in the y-direction on each fastener
    F_pi = F_y / n_f

    #Calculating the shear stress on the fastener and the sheets.
    for i in range(len(distances)):

        # Forces on a fastener
        F_pMz = (M_z * i * A_tension) / summation

        # Total Force and shear stress
        F_T = F_pi + F_pMz
        shearstress = F_T / A_shear

        difference = shearstress - shearyieldstress
        margin.append(difference)

    # Easy check to see if the structure will fail
    for j in range(len(margin)):
        if (j >= 0):
            print('There is a fastener where failure occurs')
        else:
            print('This configuration is fine')


    return margin       #margin is a list of the difference between shear stress and the yield stress. If the value is positive, if the margin is positive, then pull through occurs


