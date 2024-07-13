import numpy as np
import math

#==========================================================================Constants===================================================================================  


#===========================general constants=====================================================

 #speed of light
c = 299792458
 #mass of the hydrogen atom  in kg 
m = 1.65 * 10**(-27) 


#===========================constants for FIDA====================================================
# Delta_lambda = 0
lambda_0 = 656.1 * 10**(-9)

# Delta_lambda = 5 and 7
lambda_1 = 658.1 * 10**(-9)
lambda_2 = 663.1 * 10**(-9)

# Delta_lambda = -5 and -7
lambda_3 = 649.1 * 10**(-9)
lambda_4 = 654.1 * 10**(-9)


    #s_l  array
s_l = np.array([-220.2 , -165.2, -137.7, -110.2, -82.64, -55.1, -27.56, 0, 27.57, 55.15, 82.74, 110.3, 138.0, 165.6, 220.9]) * 10**(-18)

    #C_l array
C_l = np.array([1, 18, 16, 1681, 2304, 729, 1936, 5490, 1936, 729, 2304, 1681, 16, 18, 1])
C_f = np.sum(C_l)


#===========================constants for CTS=====================================================
   #u input
u1 =  1.5*10**6
u2 =  4.5*10**6

u3 = -4.5*10**6
u4 = -1.5*10**6
#==================================================================================================================================================================================




#==========================================================================FIDA Weight Function===================================================================================    
def prob_pi(x, y, s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B):
 probabilities_pi = np.zeros_like(x)                                                         #creating an array similar array x or y
 for i, s in enumerate(s_l):                                                                 #i is index element, and s is value of the element
     if i in [0, 3, 4, 5, 9, 10, 11, 14]:

       lambda_one = (((y * np.sin(phi_radian)) + x * np.cos(phi_radian))/c + 1 ) *(lambda_0 + s_l[i] * y * B)
       lambda_m_one = ((-(y * np.sin(phi_radian)) + x * np.cos(phi_radian))/c + 1 ) *(lambda_0 + s_l[i] * y * B)
           
       if np.any(lambda_m_one>lambda_one):
        lambda_up = np.where((lambda_m_one>lambda_2) & (lambda_one<lambda_2), lambda_2, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_m_one) ))
        lambda_down =  np.where((lambda_m_one>lambda_1) & (lambda_one<lambda_1), lambda_1, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_one) ))
       if np.any(lambda_m_one<lambda_one):
        lambda_up = np.where((lambda_one>lambda_2) & (lambda_m_one<lambda_2), lambda_2, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_one) ))
        lambda_down =  np.where((lambda_one>lambda_1) & (lambda_m_one<lambda_1), lambda_1, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_m_one) ))
    
       #arg_1
       arg1_l = (c * (lambda_down / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
       arg1_l = np.where(np.isnan(arg1_l), np.nan, np.where(arg1_l <= -1, -1, np.where(arg1_l >= 1, 1, arg1_l)))

       #arg_2
       arg2_l = (c * (lambda_up / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
       arg2_l = np.where(np.isnan(arg2_l), np.nan, np.where(arg2_l <= -1, -1, np.where(arg2_l >= 1, 1, arg2_l)))

       #gyroangle
       gyroangle_1_l = np.arccos(arg1_l)
       gyroangle_2_l = np.arccos(arg2_l)

       #gyroangle1 - gyroangle2
       minus= (gyroangle_1_l - gyroangle_2_l)/np.pi


       probabilities_pi_st = C_l[i] / C_f * ( minus - (np.sin(phi_radian)**2)/2 * ( minus - (np.sin(2 * gyroangle_1_l ) - np.sin(2 * gyroangle_2_l)) / (2 * np.pi)))
       probabilities_pi_st = np.nan_to_num(probabilities_pi_st)

       probabilities_pi += probabilities_pi_st
 return probabilities_pi
    
def prob_sigma(x, y,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B):

 probabilities_sigma = np.zeros_like(y)
 for i, s in enumerate(s_l):
    if i in [1, 2, 6, 7, 8, 12, 13]:
       lambda_one = (((y * np.sin(phi_radian)) + x * np.cos(phi_radian))/c + 1 ) *(lambda_0 + s_l[i] * y * B)
       lambda_m_one = ((-(y * np.sin(phi_radian)) + x * np.cos(phi_radian))/c + 1 ) *(lambda_0 + s_l[i] * y * B)
           
       if np.any(lambda_m_one>lambda_one):
        lambda_up = np.where((lambda_m_one>lambda_2) & (lambda_one<lambda_2), lambda_2, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_m_one) ))
        lambda_down =  np.where((lambda_m_one>lambda_1) & (lambda_one<lambda_1), lambda_1, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_one) ))
       if np.any(lambda_m_one<lambda_one):
        lambda_up = np.where((lambda_one>lambda_2) & (lambda_m_one<lambda_2), lambda_2, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_one) ))
        lambda_down =  np.where((lambda_one>lambda_1) & (lambda_m_one<lambda_1), lambda_1, np.where((lambda_m_one>lambda_2) & (lambda_one>lambda_2), np.nan, np.where((lambda_m_one<lambda_1) & (lambda_one<lambda_1), np.nan, lambda_m_one) ))
    
       #arg_1
       arg1_l = (c * (lambda_down / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
       arg1_l = np.where(np.isnan(arg1_l), np.nan, np.where(arg1_l <= -1, -1, np.where(arg1_l >= 1, 1, arg1_l)))

       #arg_2
       arg2_l = (c * (lambda_up / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
       arg2_l = np.where(np.isnan(arg2_l), np.nan, np.where(arg2_l <= -1, -1, np.where(arg2_l >= 1, 1, arg2_l)))

       #gyroangle
       gyroangle_1_l = np.arccos(arg1_l)
       gyroangle_2_l = np.arccos(arg2_l)

       #gyroangle1 - gyroangle2
       minus= (gyroangle_1_l - gyroangle_2_l)/np.pi


       probabilities_sigma_st = C_l[i] / C_f * ( minus + (np.sin(phi_radian)**2)/2 * ( minus - (np.sin(2 * gyroangle_1_l ) - np.sin(2 * gyroangle_2_l)) / (2 * np.pi)))
       probabilities_sigma_st = np.nan_to_num(probabilities_sigma_st)

       probabilities_sigma += probabilities_sigma_st

 return probabilities_sigma

def prob_st(x, y, s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B):
        
     #v_parallel and v_perp      
     v_parallel = np.sqrt(np.abs(2 * (x - B * np.abs(y)) / m)) * np.sign(y)
     v_perp = np.sqrt(np.abs(2 * B * np.abs(y) / m))
      
     #result
     rez = prob_pi(v_parallel, v_perp,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B) + prob_sigma(v_parallel, v_perp,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B) 
     rez = np.where(rez >= 0, rez, 0)
     rez = np.nan_to_num(rez)

     return rez

def weight_Function(phi, B, x, y):
    phi_radian =  np.radians(phi)

    #SI system
    x = x*(1.6*10**(-19))*10**3
    y = y*(1.6*10**(-19))*10**3
       
    x, y = np.meshgrid(x, y)
    result = np.where(x>=np.abs(y)*B, prob_st(x, y,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B ), 0) + np.where(x>=np.abs(y)*B, prob_st(x, y,  s_l, C_l, C_f, m,lambda_0, lambda_3, lambda_4, c,phi_radian, B ), 0)
    
    return result
#==================================================================================================================================================================================




#==========================================================================CTS Weight Function===================================================================================  

def CTS_wf(phi, B, x, y):
   phi_radian = np.radians(phi)

   #SI system
   x = x*(1.6*10**(-19))*10**3
   y = y*(1.6*10**(-19))*10**3
   x, y = np.meshgrid(x, y)

   #search result
   result = np.where(x>=np.abs(y)*B,CTS_WF_real(B, x, y, m, u1, u2, phi_radian), 0) + np.where(x>=np.abs(y)*B,CTS_WF_real(B, x, y, m, u3, u4, phi_radian), 0)
   return result

def CTS_WF_real(B, x, y, m, u1, u2, phi_radian):
    v_parallel = np.sqrt(np.abs(2 * (x - B * np.abs(y)) / m)) * np.sign(y)
    v_perp = np.sqrt(np.abs(2 * B * np.abs(y) / m))
    rez = np.where(v_perp!=0, WF_CTS(v_parallel,v_perp,u1, u2, phi_radian), 0)
    return rez

def WF_CTS(x,y,u1, u2, phi_radian):
    u_1 = np.round((y * np.sin(phi_radian) + x * np.cos(phi_radian)),1)
    u_m1 =  np.round((x * np.cos(phi_radian) -(y * np.sin(phi_radian))),1)
    if np.any(u_1>u_m1):
       u_up = np.where((u_1>u2) & (u_m1<u2), u2, np.where((u_1>u2) & (u_m1>u2), np.nan, np.where((u_1<u1) & (u_m1<u1), np.nan, u_1) ))
       u_down =  np.where((u_1>u1) & (u_m1<u1), u1, np.where((u_1>u2) & (u_m1>u2), np.nan, np.where((u_1<u1) & (u_m1<u1), np.nan, u_m1) ))
    if np.any(u_1<u_m1):
       u_up = np.where((u_m1>u2) & (u_1<u2), u2, np.where((u_1>u2) & (u_m1>u2), np.nan, np.where((u_1<u1) & (u_m1<u1), np.nan, u_m1) ))
       u_down =  np.where((u_m1>u1) & (u_1<u1), u1, np.where((u_1>u2) & (u_m1>u2), np.nan, np.where((u_1<u1) & (u_m1<u1), np.nan, u_1) ))
    

    #gyroangle_1
    arg_1 = (u_down - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
    arg_1_1 = np.where(arg_1 <= -1, -1, np.where(arg_1 >= 1, 1, arg_1))

    #gyroangle_1
    arg_2 = (u_up - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
    arg_2_2 =  np.where(arg_2 <= -1, -1, np.where(arg_2 >= 1, 1, arg_2))

    #gyroangle
    gyroangle_1_l = np.arccos(arg_1_1)
    gyroangle_2_l = np.arccos(arg_2_2)

    rez = 1/np.pi * (gyroangle_1_l - gyroangle_2_l)

    rez = np.nan_to_num(rez)
    return rez
#==================================================================================================================================================================================

   
     


   
   
