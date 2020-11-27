

def stressmode_tension(D, t, WD, F_y):

    stressgraph = 12
    MS = 0.15
    t_list = []

    #Getting material propeties
    #Matetial_properties = get_material():
    # fill in a number for n which gets the ultimate
    sigma_ult = material_properties[n]

    #Getting the right curve
    #K_tension = getcurve(WD):

    for i in range(5):
        WD = WD + 0.25
        for j in range(30):
            t = t + 0.05

            A_tension = D * t * (WD - 1)

            sigma_tu = F_y / (MS * K_tension * A_tension)
            if sigma_tu - sigma_ult > 0:
                t_list.append([WD, t])
                break

    return t_list


