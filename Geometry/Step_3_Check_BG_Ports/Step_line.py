import numpy as np
import Tools.Function_for_DATA_angel as FuD 
import coordinate_output_NBI_and_ports as Cout
import Tools.tools_translate_and_find_min_distance as tool

def step(R_1 , Phi_1, dx_0, dz_0, z_1, dy_0):
    x_1, y_1 = tool.to_normal_translate_coordinates(R_1 , Phi_1)
    x_1 = x_1 + dx_0
    y_1 = y_1 + dy_0
    z_1 = z_1 + dz_0
    R_1 , Phi_1 = tool.translate_coordinates(x_1, y_1)
    return R_1 , Phi_1, z_1  
      

def point(R_x_all, R_y_all, Z_all, Phi, R_phi, Z_phi , x_0, y_0, z_0,dx_0, dz_0, dy_0):
    
    
    R_0, Phi_0 = tool.translate_coordinates(x_0, y_0)
    R_0 , Phi_0, z_0 = step(R_0 , Phi_0, dx_0, dz_0, z_0, dy_0)
    #step
    x_1 = x_0 + dx_0*10
    y_1 = y_0 + dy_0*10
    z_1 = z_0 + dz_0*10

    R_1 , Phi_1 = tool.translate_coordinates(x_1, y_1)
    R_1 , Phi_1, z_1 = step(R_1 , Phi_1, dx_0, dz_0, z_1, dy_0)

    min_distance = tool.find_min_disnace(R_1 , Phi_1,  z_1)
          
    while min_distance > 0.1:
      if min_distance > 15:
          dx_1 = dx_0/10
          dz_1 = dz_0/10
          dy_1 = dy_0/10
      if min_distance > 1 and min_distance <= 15:
          dx_1 = dx_0/100
          dz_1 = dz_0/100
          dy_1 = dy_0/100

      if min_distance > 0.01 and min_distance <=  1: 
          dx_1 = dx_0/1000
          dz_1 = dz_0/1000
          dy_1 = dy_0/1000
      R_1 , Phi_1, z_1 =step(R_1 , Phi_1, dx_1, dz_1, z_1, dy_1)
      min_distance = tool.find_min_disnace(R_1 , Phi_1,  z_1)

    R_phi_3, Z_phi_3, R_phi_1, Z_phi_1, R_phi_2, Z_phi_2 = FuD.data_for_our_angle(R_phi, Z_phi, Phi_1, Phi)

    
    x_1, y_1 = tool.to_normal_translate_coordinates(R_1 , Phi_1) 
    return x_1, y_1, z_1
