from osa import Client
import numpy as np
from scipy.optimize import approx_fprime


def mag_field_find(point):
  x1 = point[0]
  x2 = point[1]
  x3 = point[2]
  client = Client('http://esb:8280/services/Mag3dProxy?wsdl')
  cl_coilDB=Client('http://esb.ipp-hgw.mpg.de:8280/services/CoilsDB?wsdl')
 

  config=cl_coilDB.service.getMagneticConfiguration(6)
 
  points = client.types.Points3D()
  points.x1 = x1
  points.x2 = x2
  points.x3 = x3
 
 

  ret = client.service.magneticField(config,points)
 
  B = np.sqrt(np.square(ret.x1)+np.square(ret.x2)+np.square(ret.x3))
  
  Vector_B = [ret.x1,ret.x2,  ret.x3]

  return B, Vector_B


def mag_field(x1, x2, x3):
    points = np.array([x1, x2, x3])  

    B, Vector_B = mag_field_find(points) 

   
    grad = calculate_gradient_of_magnetic_field(points, delta=1e-6)


    
    Vector_B_np = np.array(Vector_B)
    grad = np.array(grad)
    cross_V = np.zeros_like(Vector_B)

    for i in range(len(Vector_B_np[0])):
        cross_V[:, i] = np.cross(Vector_B_np[:, i], grad[:, i])
    cross_V_val = np.sqrt(cross_V[0]**2 + cross_V[1]**2 + cross_V[2]**2)
    print(cross_V_val/B**2)

    return B, Vector_B, cross_V_val


def calculate_gradient_of_magnetic_field(points, delta=1e-6):
    gradients = np.zeros_like(points)  

    delta_points = points.copy()  
    for i in range(len(points)):
        delta_points[i] += delta

    delta_points_2 = points.copy()  
    for i in range(len(points)):
        delta_points_2[i] -= delta

    _, B_delta = mag_field_find(delta_points)
    _, B_norm = mag_field_find(delta_points_2)

    B_delta = np.array(B_delta) 
    B_norm = np.array(B_norm)    

    gradients = (B_delta - B_norm) / (2*delta)

    return gradients
