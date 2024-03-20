from osa import Client
import numpy as np
from scipy.optimize import approx_fprime


def mag_field_find(x1, x2, x3):
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
    #epsilon = 1e-5
    #point = np.array([x1, x2, x3])
    
    #gradient_B = np.zeros_like(point)

    #for i in range(len(point)):
     #   delta = np.zeros_like(point)
      #  delta[i] = epsilon
       # gradient_B[i] = (mag_field_find(*(point + delta))[0] - mag_field_find(*(point - delta))[0]) / (2 * epsilon)

    B, Vector_B = mag_field_find(x1, x2, x3)

    #cross_products = np.cross(Vector_B, gradient_B, axis=0)
    #cross_products_lengths = np.linalg.norm(cross_products, axis=0)
    return B, Vector_B#, cross_products_lengths
