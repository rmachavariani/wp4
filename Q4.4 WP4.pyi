#Determing the required quantity of fasteners. Main things to determine: number of fasteners and their spacing
#Things to keep in mind: type of material -> Two types of materials. If metal 2-3; if composite 4-5.

def fastener_selection(w,e1,d2,material): #Width, Edge1, Diameter of Hole, Material Type
    #1 indicates metal, 2 indicates composite
    if material == 1:
        fastener_spacing = 2
    elif material == 2:
        fastener_spacing = 4
    else:
        return print("Please indicate the material type")
    usable_length = w - 2*e1 #determining the length where the fasteners can be
    fastener_count = int(((usable_length/d2)-1)/fastener_spacing)+1
    spacing = (w-2*e1-d2)/(fastener_count-1)
    return fastener_count,spacing #number of fastener and spacing between them