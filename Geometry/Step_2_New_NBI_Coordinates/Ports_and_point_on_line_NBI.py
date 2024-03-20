import numpy as np
import coordinate_output_NBI_and_ports as Cout
import Tools.Function_for_DATA_angel as FuD 
import Step_line as StL
import os



#Create Full DATA poinst in XYZ coordinate




Phi, R_phi, Z_phi = FuD.read_data(1)
R_x_all, R_y_all, Z_all = FuD.all_point(Phi)


#Download data coordinates of ports and NBIs
P_1, P_2, P_3, P_unit_vector = Cout.Ports()   
NBI_X, NBI_Y, NBI_Z, NBI_uvec_X, NBI_uvec_Y, NBI_uvec_Z = Cout.NBI()




#Find new NBI_start
def find_new_NBI_start():
    NBI_new_start = [np.array([]) for _ in range(3)]
    for i in range(len(NBI_X)):
     if i<=7:
       dx = NBI_uvec_X[i]
       dy = NBI_uvec_Y[i]
       dz = NBI_uvec_Z[i] 
     

       x_1, y_1, z_1 = StL.point(R_x_all, R_y_all, Z_all, Phi, R_phi, Z_phi , NBI_X[i], NBI_Y[i], NBI_Z[i], dx, dz, dy) 
     
     

       x_1 = x_1 + dx/(np.sqrt(dx**2 + dy**2 + dz**2))*2
       y_1 = y_1 + dy/(np.sqrt(dx**2 + dy**2 + dz**2))*2
       z_1 = z_1 + dz/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     
       NBI_new_start[0] = np.append(NBI_new_start[0], x_1)
       NBI_new_start[1] = np.append(NBI_new_start[1], y_1)
       NBI_new_start[2] = np.append(NBI_new_start[2], z_1)
     else:
       NBI_new_start[0] = np.append(NBI_new_start[0], NBI_X[i])
       NBI_new_start[1] = np.append(NBI_new_start[1], NBI_Y[i])
       NBI_new_start[2] = np.append(NBI_new_start[2], NBI_Z[i])
     
     print(i)

    return NBI_new_start
                                                                                                                                                               


#Find new NBI_end
def find_new_NBI_end(NBI_new_start):
    NBI_new_end = [np.array([]) for _ in range(3)]
    for i in range(len(NBI_X)):
     
     dx = NBI_uvec_X[i]
     dy = NBI_uvec_Y[i]
     dz = NBI_uvec_Z[i]  
     
     
     NBI_new_start[0][i] = NBI_new_start[0][i] + 2*dx
     NBI_new_start[1][i] = NBI_new_start[1][i] + 2*dy
     NBI_new_start[2][i] = NBI_new_start[2][i] + 2*dz
        
     x_1, y_1, z_1 = StL.point(R_x_all, R_y_all, Z_all, Phi, R_phi, Z_phi , NBI_new_start[0][i], NBI_new_start[1][i], NBI_new_start[2][i], dx, dz, dy) 
     
     
     NBI_new_end[0] = np.append(NBI_new_end[0], x_1)
     NBI_new_end[1] = np.append(NBI_new_end[1], y_1)
     NBI_new_end[2] = np.append(NBI_new_end[2], z_1)
     print(i)

    return NBI_new_end