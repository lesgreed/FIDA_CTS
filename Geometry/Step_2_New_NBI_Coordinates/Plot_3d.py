import numpy as np
import Tools.Function_for_DATA_angel as FuD 
import matplotlib.pyplot as plt
import Tools.tools_translate_and_find_min_distance as tool
import Ports_and_point_on_line_NBI as Port
import coordinate_output_NBI_and_ports as Cout



def plot_3d(R_x_all, R_y_all, Z_all, P_1, P_2_new):
    Phi, R_phi, Z_phi = FuD.read_data("data.txt")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    i=0
    while i<=360:
       ax.plot(R_x_all[i], R_y_all[i], Z_all[i], marker='o', linestyle='-', alpha=0.5, markersize=1)
       #ax.scatter(R_x_all[i], R_y_all[i], Z_all[i], alpha=0.1, s=10)

       i=i+5

    #Points_line_NBI
    
    for i in range(len(P_1[0])):
       ax.plot([P_1[0][i], P_2_new[0][i]], [P_1[1][i], P_2_new[1][i]], [P_1[2][i], P_2_new[2][i]],  color='blue')
       ax.scatter(P_1[0][i], P_1[1][i], P_1[2][i],  color='red', s=10, marker='o')
    
    
    
    
    for i in range(len(P_2_new[0])):
   
      x_i = P_1[0][i]
      y_i = P_1[1][i]
      z_i = P_1[2][i]
      
      x_last_i = P_2_new[0][i]
      y_last_i = P_2_new[1][i]
      z_last_i = P_2_new[2][i]
      
      
            
      
      #Graph_Last_Pint_NBI
      Angel_1 = np.arctan( y_i/x_i)

      if x_i<0:
         Angel_1 = Angel_1 + np.pi
      Angel_1 = np.degrees(Angel_1)
      if Angel_1<0:
        Angel_1 = Angel_1 + 360 
      else: 
        Angel_1 = Angel_1


      R_phi_3, Z_phi_3, R_phi_1, Z_phi_1, R_phi_2, Z_phi_2 = FuD.data_for_our_angle(R_phi, Z_phi, Angel_1, Phi)
      R_x_list, R_y_list, Z_list = FuD.calculate_3d_data(R_phi_3, Z_phi_3, Angel_1)
      

      
      #Graph_Zero_Pint_NBI
      Angel_0 =  np.arctan(y_last_i/x_last_i)
      if x_last_i<0:
          Angel_0 = Angel_0 + np.pi
      Angel_0 = np.degrees(Angel_0)
      if Angel_0<0:
          Angel_0 = Angel_0 + 360 
      else: 
          Angel_0 = Angel_0

      R_phi_4, Z_phi_4, R_phi_1, Z_phi_1, R_phi_2, Z_phi_2 = FuD.data_for_our_angle(R_phi, Z_phi, Angel_0, Phi)
      R_x_list_1, R_y_list_1, Z_list_1 = FuD.calculate_3d_data(R_phi_4, Z_phi_4, Angel_0)
      
      ax.plot(R_x_list, R_y_list, Z_list,  marker='o', color='red', linestyle='-', alpha=0.5, markersize=1)
      ax.plot(R_x_list_1, R_y_list_1, Z_list_1,  marker='o', color='red', linestyle='-', alpha=0.5, markersize=1)
    

    ax.set_xlabel('R_x')
    ax.set_ylabel('R_y')
    ax.set_zlabel('Z')
    ax.set_title('3D Plot with Contour Lines')
    
    
    
    plt.show()