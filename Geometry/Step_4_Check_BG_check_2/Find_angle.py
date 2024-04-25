import numpy as np
import coordinate_output_NBI_and_ports as Cout
import Tools.Function_for_DATA_angel as FuD 
import Step_line as StL
import Tools.tools_translate_and_find_min_distance as tool
import math




#Create Full DATA poinst in XYZ coordinate
Phi, R_phi, Z_phi = FuD.read_data('Tools/data.txt')
R_x_all, R_y_all, Z_all = FuD.all_point(Phi)


#Download data coordinates of ports and NBIs
P_1, P_2_new = Cout.new_Ports()
NBI_start, NBI_end = Cout.new_NBI()



#Downloand Good_ports
Good_PN = Cout.good_ports_1()

def angle():
    
    NBI_points = points_on_line_NBI()
    angle_NBI_port = Ports_to_point_on_line_NBI_abgle(NBI_points, Good_PN)
    return angle_NBI_port

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







def Ports_to_point_on_line_NBI_abgle(NBI_points, Good_PN):
    
    #Create array with Number_Ports, NBI and angles
    angle_NBI_port = [np.array([]) for _ in range(4)]
    
    
    for i in range(len(Good_PN[0])):
        Line=[]
        Number_ports = int(Good_PN[0][i]-1)
        Number_NBI = int(Good_PN[1][i]-1)
        print("Number_ports =", Number_ports,"Number_NBI =", Number_NBI )
        
        x_1 = P_2_new[0][Number_ports] 
        y_1 = P_2_new[1][Number_ports] 
        z_1 = P_2_new[2][Number_ports] 
        
        
        X_point_on_NBI = NBI_points[0]
        Y_point_on_NBI = NBI_points[1]
        Z_point_on_NBI = NBI_points[2]
        
        for j in range(len(NBI_points[0][1])):
         k_x = (X_point_on_NBI[Number_NBI][j] - x_1)
         k_y = (Y_point_on_NBI[Number_NBI][j] - y_1)
         k_z = (Z_point_on_NBI[Number_NBI][j] - z_1)
        
        
        
         x_1 = P_2_new[0][Number_ports ] + 4*k_x/( np.sqrt(k_x**2 + k_y**2 + k_z**2))
         y_1 = P_2_new[1][Number_ports ] + 4*k_y/( np.sqrt(k_x**2 + k_y**2 + k_z**2))
         z_1 = P_2_new[2][Number_ports ] + 4*k_z/( np.sqrt(k_x**2 + k_y**2 + k_z**2))

         
         l_ka = step_for_ports(x_1, y_1, z_1, X_point_on_NBI[Number_NBI][j], Y_point_on_NBI[Number_NBI][j], Z_point_on_NBI[Number_NBI][j], k_x, k_y, k_z)
         
         if l_ka == 1:
             
             un_Port_to_NBI_x = (X_point_on_NBI[Number_NBI][j] - x_1)
             un_Port_to_NBI_y = (Y_point_on_NBI[Number_NBI][j] - y_1)
             un_Port_to_NBI_z = (Z_point_on_NBI[Number_NBI][j] - z_1)
                     
             un_Port_to_NBI = (un_Port_to_NBI_x,un_Port_to_NBI_y, un_Port_to_NBI_z)
             
             
             un_Ports_x = x_1-P_1[0][Number_ports]
             un_Ports_y = y_1-P_1[1][Number_ports]
             un_Ports_z = z_1-P_1[2][Number_ports]
             
             un_Ports=(un_Ports_x, un_Ports_y, un_Ports_z)
             
             angle = angle_between_vectors(un_Ports, un_Port_to_NBI)
             
             if angle > 85:
                 l=0
             else: 
                l = 1
         else:
              l=0
         Line.append(l)
        print(Line)
        
        if sum(Line)>=15:

         Start_Angle_index, Last_Angle_index = find_longest_sequence(Line)
        
        
    
        
         print("The following is good:")
         angle_NBI_port[0] = np.append(angle_NBI_port[0], Number_ports+1)
         angle_NBI_port[1] = np.append(angle_NBI_port[1], Number_NBI+1)
         angle_NBI_port[2] = np.append(angle_NBI_port[2], Start_Angle_index)
         angle_NBI_port[3] = np.append(angle_NBI_port[3], Last_Angle_index)
        print("Start_Angle_index=", Start_Angle_index, "Last_Angle_index=", Last_Angle_index)
        
    return np.array(angle_NBI_port)
        
        
        
        
        
        
        




def step_for_ports(x_0, y_0, z_0, x_1, y_1, z_1, dx, dy, dz):
              
              

              p=0
              x_step, y_step, z_step = real_step(x_0, y_0, z_0, x_1, y_1, z_1,p)
              R_1 , Phi_1 = tool.translate_coordinates(x_step, y_step)
              min_distance = tool.find_min_disnace(R_1 , Phi_1,  z_step)
              
              
              while not p == 10000:

                if min_distance <= 0.1:
                    break
                if min_distance >= 30:
                    dp  = 20
                if min_distance > 15 and  min_distance < 30:
                    dp  = 10
                if min_distance > 2 and min_distance <= 15:
                    dp  = 5
                if min_distance > 1 and min_distance <= 2:
                    dp  = 2
                if min_distance > 0.1 and min_distance <=  1: 
                    dp  = 1
                if p >=9900: 
                    dp = 1

                
                p = p + dp
                x_step, y_step, z_step = real_step(x_0, y_0, z_0, x_1, y_1, z_1,p)
                R_1_1_1 , Phi_1 = tool.translate_coordinates(x_step, y_step)
                min_distance = tool.find_min_disnace(R_1_1_1 , Phi_1,  z_step)
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



def find_longest_sequence(arr):
    max_count = 0
    current_count = 0
    start_index = None
    end_index = None
    current_start_index = None

    for i, num in enumerate(arr):
        if num == 1:
            current_count += 1
            if current_count == 1:
                current_start_index = i
        else:
            if current_count > max_count:
                max_count = current_count
                start_index = current_start_index
                end_index = i - 1
            current_count = 0

    if current_count > max_count:
        start_index = current_start_index
        end_index = len(arr) - 1

    if start_index is not None and end_index is not None:
        return start_index, end_index
    else:
        return None



def angle_between_vectors(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    norm1 = math.sqrt(sum(a**2 for a in vector1))
    norm2 = math.sqrt(sum(b**2 for b in vector2))

    cosine_theta = dot_product / (norm1 * norm2)
    angle_in_radians = math.acos(cosine_theta)


    angle_in_degrees = math.degrees(angle_in_radians)

    return angle_in_degrees