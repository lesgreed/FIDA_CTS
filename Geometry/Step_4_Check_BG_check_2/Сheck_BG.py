import numpy as np
import coordinate_output_NBI_and_ports as Cout
import Tools.Function_for_DATA_angel as FuD 
import Step_line as StL
import Tools.tools_translate_and_find_min_distance as tool



#Create Full DATA poinst in XYZ coordinate
Phi, R_phi, Z_phi = FuD.read_data('Tools/data.txt')
R_x_all, R_y_all, Z_all = FuD.all_point(Phi)


#Download data coordinates of ports and NBIs
P_1, P_2_new = Cout.new_Ports()
NBI_start, NBI_end = Cout.new_NBI()


def check():
    NBI_points  = points_on_line_NBI()
    Good_Ports  = Ports_to_point_on_line_NBI(NBI_points)
    return Good_Ports

    
    

def points_on_line_NBI():

    X_point_on_NBI = [np.array([]) for _ in range(len(NBI_start[0]))]
    Y_point_on_NBI = [np.array([]) for _ in range(len(NBI_start[0]))]
    Z_point_on_NBI = [np.array([]) for _ in range(len(NBI_start[0]))]
    
    for i in range(len(NBI_end[0])):
        k_x = (NBI_end[0][i] - NBI_start[0][i])
        k_y = (NBI_end[1][i] - NBI_start[1][i])
        k_z = (NBI_end[2][i] - NBI_start[2][i])


        for j in range(21):

            x_k = NBI_start[0][i] + k_x * (j / 20)
            y_k = NBI_start[1][i] + k_y * (j / 20)
            z_k = NBI_start[2][i] + k_z * (j / 20)
            
            
            if j !=0 and j != 20:
             X_point_on_NBI[i] = np.append(X_point_on_NBI[i], x_k)
             Y_point_on_NBI[i] = np.append(Y_point_on_NBI[i], y_k)
             Z_point_on_NBI[i] = np.append(Z_point_on_NBI[i], z_k)

    NBI_points = np.array([X_point_on_NBI, Y_point_on_NBI, Z_point_on_NBI])
    return NBI_points 






def Ports_to_point_on_line_NBI(NBI_points):
    
    X_point_on_NBI = NBI_points[0]
    Y_point_on_NBI = NBI_points[1]
    Z_point_on_NBI = NBI_points[2]
    

    X_point_on_NBI_line = [np.array([]) for _ in range(5)]
    Y_point_on_NBI_line = [np.array([]) for _ in range(5)]
    Z_point_on_NBI_line = [np.array([]) for _ in range(5)]

    for i in range(len(P_2_new[1])):
        #print(i)
        for k in range(len(X_point_on_NBI)):
            kawai = 0
            for j in range(len(X_point_on_NBI[1])):  
              #print("j=", j)

              dx = (P_2_new[0] - P_1[0])
              dy = (P_2_new[1] - P_1[1])
              dz = (P_2_new[2] - P_1[2])
              
              
              x_1 = P_2_new[0][i] 
              y_1 = P_2_new[1][i] 
              z_1 = P_2_new[2][i] 
              
              k_x = (X_point_on_NBI[k][j] - x_1)
              k_y = (Y_point_on_NBI[k][j] - y_1)
              k_z = (Z_point_on_NBI[k][j] - z_1)
              
              x_1 = P_2_new[0][i] + 2*k_x/( np.sqrt(k_x**2 + k_y**2 + k_z**2))
              y_1 = P_2_new[1][i] + 2*k_y/( np.sqrt(k_x**2 + k_y**2 + k_z**2))
              z_1 = P_2_new[2][i] + 2*k_z/( np.sqrt(k_x**2 + k_y**2 + k_z**2))
              
              
              l = step_for_ports(x_1, y_1, z_1, X_point_on_NBI[k][j], Y_point_on_NBI[k][j], Z_point_on_NBI[k][j], k_x, k_y, k_z)
              kawai = kawai + l
              if j ==10:
                  kawai = kawai + 2
              #print(kawai)
              

            if kawai >= 10:
                  X_point_on_NBI_line[0] = np.append(X_point_on_NBI_line[0], i+1)
                  Y_point_on_NBI_line[0] = np.append(Y_point_on_NBI_line[0], i+1)
                  Z_point_on_NBI_line[0] = np.append(Z_point_on_NBI_line[0], i+1) 
                  
                
                  X_point_on_NBI_line[1] = np.append(X_point_on_NBI_line[1], k+1)
                  Y_point_on_NBI_line[1] = np.append(Y_point_on_NBI_line[1], k+1)
                  Z_point_on_NBI_line[1] = np.append(Z_point_on_NBI_line[1], k+1) 
                  

                  print("Port ", i, "is kawai) for {", k, "} NBI")
            else:
                print("Port ", i, "is not kawai( for {", k, "} ")
                
    Good_Ports = [X_point_on_NBI_line, Y_point_on_NBI_line, Z_point_on_NBI_line]
        
    return Good_Ports




def step_for_ports(x_0, y_0, z_0, x_1, y_1, z_1, dx, dy, dz):
              
              

              p=0
              x_step, y_step, z_step = real_step(x_0, y_0, z_0, x_1, y_1, z_1,p)
              R_1 , Phi_1 = tool.translate_coordinates(x_step, y_step)
              min_distance = tool.find_min_disnace(R_1 , Phi_1,  z_step)
              
              
              while not p == 10000:

                if min_distance <= 0.1:
                    break
                if min_distance >= 30:
                    dp  = 50
                if min_distance > 15 and  min_distance < 30:
                    dp  = 20
                if min_distance > 1 and min_distance <= 15:
                    dp  = 10
                if min_distance > 0.1 and min_distance <=  1: 
                    dp  = 1
                if p >=9900: 
                    dp = 1

                
                p = p + dp
                x_step, y_step, z_step = real_step(x_0, y_0, z_0, x_1, y_1, z_1,p)
                R_1 , Phi_1 = tool.translate_coordinates(x_step, y_step)
                min_distance = tool.find_min_disnace(R_1 , Phi_1,  z_step)
              print("p =", p)
              if p == 10000: 
                 local = 1
              else: 
                 local = 0
              return local


def real_step(x_0, y_0, z_0, x_1, y_1, z_1,p):
    x_step = p * (x_1 -x_0)/10000 + x_0
    y_step = p * (y_1 -y_0)/10000 + y_0
    z_step = p * (z_1 -z_0)/10000 + z_0
    return x_step, y_step, z_step


















#Find new NBI_start
#def find_new_NBI_start():
#    NBI_new_start = [np.array([]) for _ in range(3)]
#    for i in range(len(NBI_X)):
#
#     dx = NBI_uvec_X[i]
#     dy = NBI_uvec_Y[i]
#     dz = NBI_uvec_Z[i] 

     #dx = dx/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     #dy = dy/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     #dz = dz/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     

#     x_1, y_1, z_1 = StL.point(R_x_all, R_y_all, Z_all, Phi, R_phi, Z_phi , NBI_X[i], NBI_Y[i], NBI_Z[i], dx, dz, dy) 
     
     

#     x_1 = x_1 + dx/(np.sqrt(dx**2 + dy**2 + dz**2))*2
#     y_1 = y_1 + dy/(np.sqrt(dx**2 + dy**2 + dz**2))*2
#     z_1 = z_1 + dz/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     
#     NBI_new_start[0] = np.append(NBI_new_start[0], x_1)
#     NBI_new_start[1] = np.append(NBI_new_start[1], y_1)
#     NBI_new_start[2] = np.append(NBI_new_start[2], z_1)
#     print(i)

#    return NBI_new_start
                                                                                                                                                               


#Find new NBI_end
#def find_new_NBI_end(NBI_new_start):
#    NBI_new_end = [np.array([]) for _ in range(3)]
#    for i in range(len(NBI_X)):
     
#     dx = NBI_uvec_X[i]
#     dy = NBI_uvec_Y[i]
#     dz = NBI_uvec_Z[i]  
     
     #dx = dx/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     #dy = dy/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     #dz = dz/(np.sqrt(dx**2 + dy**2 + dz**2))*2
     
     
#     NBI_new_start[0][i] = NBI_new_start[0][i] + 2*dx
#     NBI_new_start[1][i] = NBI_new_start[1][i] + 2*dy
#     NBI_new_start[2][i] = NBI_new_start[2][i] + 2*dz
        
#     x_1, y_1, z_1 = StL.point(R_x_all, R_y_all, Z_all, Phi, R_phi, Z_phi , NBI_new_start[0][i], NBI_new_start[1][i], NBI_new_start[2][i], dx, dz, dy) 
     
     
#     NBI_new_end[0] = np.append(NBI_new_end[0], x_1)
#     NBI_new_end[1] = np.append(NBI_new_end[1], y_1)
#     NBI_new_end[2] = np.append(NBI_new_end[2], z_1)
#     print(i)

#    return NBI_new_end