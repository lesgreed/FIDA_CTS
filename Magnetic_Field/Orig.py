# pip install osa

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:49:10 2019
 
@author: tya
"""
 
from osa import Client
import numpy as np
client = Client('http://esb:8280/services/Mag3dProxy?wsdl')
cl_coilDB=Client('http://esb.ipp-hgw.mpg.de:8280/services/CoilsDB?wsdl')
 
#config = client.types.MagneticConfiguration()
#tracer = Client('http://esb.ipp-hgw.mpg.de:8280/services/FieldLineProxy?wsdl')
 
#config = tracer.types.MagneticConfig()
#config.configIds = [17]   # CAD J, 2.5 Tget
config=cl_coilDB.service.getMagneticConfiguration(6)
 
 
#config=16
"""
circuit1 = client.types.SerialCircuit()
ring = client.types.CircularFilament()
ring.centre.x = 0.0
ring.centre.y = 0.0
ring.centre.z = 0.0
ring.normal.x = 0.0
ring.normal.y = 0.0
ring.normal.z = 1.0
ring.radius = 1.5
circuit1.currentCarrier = [ring]
circuit1.current = 10000.
config.circuit = [circuit1]
"""
R = 5.3
phi = 16.
z = 0.2
 
x = R*np.cos(phi*np.pi/180)
y = R*np.sin(phi*np.pi/180)
 
points = client.types.Points3D()
points.x1 = np.loadtxt('x1.txt')
points.x2 = np.loadtxt('x2.txt')
points.x3 = np.loadtxt('x3.txt')
 
 
""
ret = client.service.magneticField(config,points)
 
B = np.sqrt(np.square(ret.x1)+np.square(ret.x2)+np.square(ret.x3))
 
np.savetxt('B.txt',B)
