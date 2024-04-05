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
    return B, Vector_B
