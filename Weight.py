"""Total Weight  Attachment"""
import math as m

def WeightFasteners (t_2,t_3,D_fo,D_fi,rho):
    l           = t_2 + t_3                               #minimum length bolt
    height_nut  = D_fo/2                                  #arbitrary
    volume_nut  = (m.pi*D_fo**2)/4*height_nut
    volume_bolt = (m.pi*D_fi**2)/4*l
    total_volume = volume_bolt + 2*volume_nut             #volume nut counted twice as there is one on either side

    weight_fastener = rho*total_volume

    return weight_fastener

def WeightAttachment (t_1,t_2,n_fasteners,n_lugs,w,l,h_lug,D_1,D_2,rho):

    volume_backupplate  = t_2*w*l - n_fasteners*(m.pi*D_2**2)/4*t_2
    volume_lug          = t_1*w*(h_lug-(w-D_1)/2-D_1/2) + t_1*(m.pi*w**2)/8 - t_1*(m.pi*D_1**2)/4

    total_volume        = volume_backupplate + n_lugs*volume_lug

    weight_attachment   = rho*total_volume

    return weight_attachment






