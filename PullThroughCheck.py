from math import pi, sqrt, sum

with open('data.json', 'r') as p:
    input = json.load(p)

def pullthrough(input):
    plate_data = input['plate']
    fastener_data = input['fastener']
    quantaties = input['output']
    fastener_quantaties =
def pullthrough(fastener_count,b,c,d,e,f,g,h,i,j):
    #Variables
    n_f = fastener_count        #Number of fasteners
    D_fi = b                    #Inner diameter of the fastener
    D_fo = c                    #Outer diameter of the fastener
    F_y = d                     #Tensile Force
    t2 = e                      #Thickness of the plate
    t3 = f                      #Thickness of the vehicle wall
    M_z = g                     #Moment of the solar panel
    yieldstress_backplate = h             #Yield stress of the plates
    yieldstress_vehicleplate = i
    listcoordinates = j


    #Determining the shear yield stress
    shearyieldstress_backplate = yieldstress_backplate/sqrt(3)
    shearyieldstress_vehicleplate = yieldstress_vehicleplate/sqrt(3)

    #Areas
    A_shear = pi * D_fo * (t2 + t3)
    A_tension = (1/4) * pi * (D_fi**2)

    #Lists
    distances = []
    margin_backplate = []
    margin_vehicleplate = []

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

    #Calculating the shear stress on the fastener and the sheets
    n = 0
    for i in distances:

        # Forces on a fastener
        F_pMz = (-M_z * i * A_tension) / summation

        # Total Force and shear stress
        if (listcoordinates[n][0] > 0):
            F_T = F_pi - F_pMz
            shearstress = F_T / A_shear
        else:
            F_T = F_pi + F_pMz
            shearstress = F_T / A_shear
        n = n + 1

        difference_backplate = shearstress - shearyieldstress_backplate
        difference_vehicleplate = shearstress - shearyieldstress_vehicleplate

        margin_backplate.append(difference_backplate)
        margin_vehicleplate.append(difference_vehicleplate)

    # Easy check to see if the structure will fail
    print('Pull Through check for the backplate')
    for j in margin_backplate:
        if (j >= 0):
            print('This fastener fails!!!!!!!!!!!!!!!!!')
        else:
            print('This configuration is fine')

    print('Pull through check for the vehicleplate')
    for k in margin_vehicleplate:
        if (k >= 0):
            print('This fastener fails!!!!!!!!!!!!!!!!!')
        else:
            print('This configuration is fine')

    return margin_vehicleplate, margin_backplate       #margin is a list of the difference between shear stress and the yield stress. If the value is positive, if the margin is positive, then pull through occurs