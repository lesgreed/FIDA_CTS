import numpy as np
import coordinate_output_NBI_and_ports as Cout
import Tools.Function_for_DATA_angel as FuD 
import Step_line as StL




#Create Full DATA poinst in XYZ coordinate
Phi, R_phi, Z_phi = FuD.read_data()
R_x_all, R_y_all, Z_all = FuD.all_point(Phi)


#Download data coordinates of ports and NBIs
P_1, P_2, P_3, P_unit_vector = Cout.Ports()   
NBI_X, NBI_Y, NBI_Z, NBI_uvec_X, NBI_uvec_Y, NBI_uvec_Z = Cout.NBI()




#Find new P_2 data 
def find_new_P2():
    P_2_new = [np.array([]) for _ in range(3)]
    dx = (P_2[0] - P_1[0])/100
    dy = (P_2[1] - P_1[1])/100
    dz = (P_2[2] - P_1[2])/100
    for i in range(len(P_1[1])):
     x_1, y_1, z_1 = StL.point(R_x_all, R_y_all, Z_all, Phi, R_phi, Z_phi , P_1[0][i], P_1[1][i],P_1[2][i],dx[i],dz[i] ,dy[i]) 
     x_1 = x_1 + dx[i]/(np.sqrt(dx[i]**2 + dy[i]**2 + dz[i]**2))*2
     y_1 = y_1 + dy[i]/(np.sqrt(dx[i]**2 + dy[i]**2 + dz[i]**2))*2
     z_1 = z_1 + dz[i]/(np.sqrt(dx[i]**2 + dy[i]**2 + dz[i]**2))*2
     
     P_2_new[0] = np.append(P_2_new[0], x_1)
     P_2_new[1] = np.append(P_2_new[1], y_1)
     P_2_new[2] = np.append(P_2_new[2], z_1)
     print(i)

    return P_2_new
