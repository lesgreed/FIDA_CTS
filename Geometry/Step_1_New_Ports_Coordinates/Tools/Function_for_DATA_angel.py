import numpy as np
import os


#Read_data_in_file "/FIDA/Geometry/Input_data/data.txt" 
def read_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'data.txt')
    Phi, R_phi, Z_phi = [], [], []
    current_block_R, current_block_Z = [], []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 1:
                block_name = parts[0]
                if block_name == ".00":
                    block_name = "0"
                Phi.append(float(block_name))
                if current_block_R:
                    R_phi.append(np.array(current_block_R))
                    Z_phi.append(np.array(current_block_Z))
                    current_block_R = []
                    current_block_Z = []
            elif len(parts) == 3:
                x_val, y_val = float(parts[0]), float(parts[1])
                current_block_R.append(x_val)
                current_block_Z.append(y_val)

    # Append the last block after reaching the end of the file
    if current_block_R:
        R_phi.append(np.array(current_block_R))
        Z_phi.append(np.array(current_block_Z))

    return np.array(Phi), R_phi, Z_phi


# Find_Data_for_random_angle
def find_nearest_angles(angles, target_angle):

    while target_angle >= 72:
        target_angle = target_angle - 72
    sorted_angles = np.sort(angles)
    idx = np.abs(sorted_angles - target_angle).argmin()
    nearest_angles_1 = sorted_angles[idx]
    
    
    if idx + 1 < len(sorted_angles):
        nearest_angles_2 = sorted_angles[idx + 1]
    else:
        nearest_angles_2 = sorted_angles[0]
    
    return nearest_angles_1, nearest_angles_2 


#Step of the interpolation (Creating a new sector based on linear interpolation)
def data_for_our_angle(R_phi, Z_phi, target_angle, Phi):
    while target_angle >= 72:
        target_angle = target_angle - 72
        
    nearest_angles_1, nearest_angles_2 = find_nearest_angles(Phi, target_angle)
    idx_nearest_angles_1 = np.where(Phi == nearest_angles_1)[0][0]
    idx_nearest_angles_2 = np.where(Phi == nearest_angles_2)[0][0]
    
    R_phi_1, Z_phi_1 = R_phi[idx_nearest_angles_1], Z_phi[idx_nearest_angles_1]
    R_phi_2, Z_phi_2 = R_phi[idx_nearest_angles_2], Z_phi[idx_nearest_angles_2]
    
    l = (R_phi_2 - R_phi_1)
    m = (Z_phi_2 - Z_phi_1)
    t = (target_angle - nearest_angles_1) / (nearest_angles_2 - nearest_angles_1)

    R_phi_3 = R_phi_1 +  t* l
    Z_phi_3 = Z_phi_1+ t * m

    return R_phi_3, Z_phi_3, R_phi_1, Z_phi_1, R_phi_2, Z_phi_2


#calculation of coordinates of points for the sector in XYZ coordinate
def calculate_3d_data(R_phi_3, Z_phi_3, target_angle):
    phi_radian = np.radians(target_angle)
    R_x_all = R_phi_3 * np.cos(phi_radian)
    R_y_all = R_phi_3 * np.sin(phi_radian)
    Z_all = Z_phi_3
    return R_x_all, R_y_all, Z_all

#All points of the machine in XYZ coordinate 
def all_point(Phi):

    Phi, R_phi, Z_phi = read_data()
    target_angle = 0
    R_x_all, R_y_all, Z_all = [], [], [] 
    while target_angle <= 360:
      R_phi_3, Z_phi_3, R_phi_1, Z_phi_1, R_phi_2, Z_phi_2 = data_for_our_angle(R_phi, Z_phi, target_angle, Phi)
      R_x_list, R_y_list, Z_list = calculate_3d_data(R_phi_3, Z_phi_3, target_angle)
      
      R_x_all.append(R_x_list)
      R_y_all.append(R_y_list)
      Z_all.append(Z_list)
     
      target_angle += 1
      
    return R_x_all, R_y_all, Z_all