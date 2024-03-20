import numpy as np
import Tools.Function_for_DATA_angel as FuD 

#Translate_in_cylindrical_coordinates
def translate_coordinates(x_1, y_1):
    R_1 = np.sqrt(x_1**2 + y_1**2)
    Phi_1 = np.arctan(y_1/x_1)
    if x_1<0:
        Phi_1 = Phi_1 + np.pi
    Phi_1 = np.degrees(Phi_1)
    if Phi_1<0:
        Phi_1 = Phi_1 + 360 
    else: 
        Phi_1 = Phi_1

    return R_1, Phi_1
  
  
#Translate_in_cartesian_coordinates
def to_normal_translate_coordinates(x_1, y_1):
    t = np.radians(y_1)
    x_2 = x_1 * np.cos(t)
    y_2 = x_1 * np.sin(t)
    return x_2, y_2


#Find_min_distance 
def find_min_disnace(R_1 , Phi_1, z_1):
       Phi, R_phi, Z_phi = FuD.read_data("data.txt")
       R_phi_3, Z_phi_3, R_phi_1, Z_phi_1, R_phi_2, Z_phi_2 = FuD.data_for_our_angle(R_phi, Z_phi, Phi_1, Phi)
       point_0 = np.array([R_1, z_1])
       min_distance = find_mindistance_to_segments( point_0, R_phi_3, Z_phi_3) 
       return  min_distance  

def find_mindistance_to_segments(new_point, x_coords, y_coords):
    distances = []
    for i in range(len(x_coords)):
        x1, y1 = x_coords[i], y_coords[i]
        if i == len(x_coords) - 1:
            x2, y2 = x_coords[0], y_coords[0]
        else:
            x2, y2 = x_coords[i + 1], y_coords[i + 1]
        
        # Calculate the direction vector of the line segment
        dx, dy = x2 - x1, y2 - y1
        
        # Calculate the vector from point1 to the new point
        qx, qy = new_point[0] - x1, new_point[1] - y1
        
        # Calculate the dot product between the vectors
        dot_product = qx * dx + qy * dy
        
        # If dot_product is negative, the closest point is point1
        if dot_product <= 0:
            distance = np.sqrt(qx**2 + qy**2)
        else:
            # Calculate the squared length of the line segment
            squared_length = dx**2 + dy**2
            
            # If dot_product is greater than the squared length, the closest point is point2
            if dot_product >= squared_length:
                qx, qy = new_point[0] - x2, new_point[1] - y2
                distance = np.sqrt(qx**2 + qy**2)
            else:
                # The closest point lies on the line segment
                distance = np.abs(qx * dy - qy * dx) / np.sqrt(squared_length)
                
        distances.append(distance)
    
    return min(distances) 


#Create array with 100 points based on line from (x_0, y_0, z_0) to (x_1, y_1, z_1)
def line_NBI(x_0, y_0, z_0, x_1, y_1, z_1):
    x_line_NBI, y_line_NBI, z_line_NBI = [], [], []
    i=1
    k_x = (x_1 - x_0)
    k_y = (y_1 - y_0)
    k_z = (z_1 - z_0)
    while i<101:
        x_k = x_0 + k_x * i/101
        y_k = y_0 + k_y * i/101
        z_k = z_0 + k_z * i/101
        x_line_NBI.append(x_k)
        y_line_NBI.append(y_k)
        z_line_NBI.append(z_k)
        i = i+1 
    
    return np.array(x_line_NBI),  np.array(y_line_NBI), np.array(z_line_NBI)