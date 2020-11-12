#Determing the required quantity of fasteners. Main things to determine: number of fasteners and their spacing
#Things to keep in mind: type of material -> Two types of materials. If metal 2-3; if composite 4-5.

def fastener_selection(w,e1,e2,d2,material): #Width, Edge1, Edge2, Diameter of Hole, Material Type
    #1 indicates metal, 2 indicates composite
    fastener_count = 2
    if material == 1:
        fastener_spacing = 2
    elif material == 2:
        fastener_spacing = 4
    else:
        return print("Please indicate the material type")
    usable_length = w - e1 - e2 #determining the length where the fasteners can be
    while usable_length > (fastener_spacing*2 - d2):
        fastener_count += 1
        usable_length -= fastener_spacing
    spacing = (w-e1-e2-d2)/(fastener_count-1)
    return fastener_count,spacing #number of fastener and spacing between them