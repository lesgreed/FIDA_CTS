import numpy as np
import math



    
    
    
    
    
def prob_pi(x, y, s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B):
 probabilities_pi = np.zeros_like(x)                                                         #creating an array similar array x or y
 for i, s in enumerate(s_l):                                                                 #i is index element, and s is value of the element
     if i in [0, 3, 4, 5, 9, 10, 11, 14]:

               #numerator_1
       arg1_l = c * (lambda_1 / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian)

       #denominator
       denominator = y * np.sin(phi_radian)

       arg_1_l = arg1_l / denominator
       arg_1_l = np.where((arg_1_l >= -1) & (arg_1_l <= 1), arg_1_l, np.nan)



       #numerator_2
       arg2_l = c * (lambda_2 / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian)

       #argument inside arccos
       arg_2_l = arg2_l / denominator



       arg_2_l = np.where((arg_2_l >= -1) & (arg_2_l <= 1), arg_2_l, np.nan)

       #gyroangle
       gyroangle_1_l = np.arccos(arg_1_l)
       gyroangle_2_l = np.arccos(arg_2_l)

       #gyroangle1 - gyroangle2
       minus= (gyroangle_1_l - gyroangle_2_l)/np.pi


       #prob_func[i]
       probabilities_pi_st = np.where((arg_1_l >= -1) & (arg_1_l <= 1) & (arg_2_l >= -1) & (arg_2_l <= 1), C_l[i] / C_f * ( minus - (np.sin(phi_radian)**2)/2 * ( minus - (np.sin(2 * gyroangle_1_l ) - np.sin(2 * gyroangle_2_l)) / (2 * np.pi))), 0)

       probabilities_pi += probabilities_pi_st

 return probabilities_pi
   
    
   
def prob_sigma(x, y,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B):

 probabilities_sigma = np.zeros_like(y)
 for i, s in enumerate(s_l):
    if i in [1, 2, 6, 7, 8, 12, 13]:

               #numerator_1
       arg1_l = c * (lambda_1 / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian)

       #denominator
       denominator = y * np.sin(phi_radian)

       arg_1_l = arg1_l / denominator
       
       arg_1_l = np.where((arg_1_l >= -1) & (arg_1_l <= 1), arg_1_l, np.nan)
       


       #numerator_2
       arg2_l = c * (lambda_2 / (lambda_0 + s_l[i] * y * B) - 1) - x * np.cos(phi_radian)

       #argument inside arccos
       arg_2_l = arg2_l / denominator



       arg_2_l = np.where((arg_2_l >= -1) & (arg_2_l <= 1), arg_2_l, np.nan)

       #gyroangle
       gyroangle_1_l = np.arccos(arg_1_l)
       gyroangle_2_l = np.arccos(arg_2_l)

       #gyroangle1 - gyroangle2
       minus= (gyroangle_1_l - gyroangle_2_l)/np.pi


       #prob_func[i]
       probabilities_sigma += np.where((arg_1_l >= -1) & (arg_1_l <= 1) & (arg_2_l >= -1) & (arg_2_l <= 1), C_l[i] / C_f * ( minus + (np.sin(phi_radian)**2)/2 * ( minus - (np.sin(2 * gyroangle_1_l ) - np.sin(2 * gyroangle_2_l)) / (2 * np.pi))), 0)


 return probabilities_sigma




def prob_st(x, y, s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B, cross_V_val):
        
     #v_parallel and v_perp      
    
     v_parallel = np.sqrt(np.abs(2 * (x - B * np.abs(y)) / m)) * np.sign(y)
     v_perp = np.sqrt(np.abs(2 * B * np.abs(y) / m))
     
     K_perp = (1/2)*m*v_perp**2
     
    

     
     


        
     rez = prob_pi(v_parallel, v_perp,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B) + prob_sigma(v_parallel, v_perp,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B)

 
     
     
     rez = np.where(rez >= 0, rez, 0)
     rez = np.nan_to_num(rez)

     return rez


def weight_Function(phi, B, x, y, cross_V):
    phi_radian =  np.pi - np.pi*phi/180
    
    # constant 
    lambda_0 = 656.1 * 10**(-9)
    lambda_1 = 658.1 * 10**(-9)
    lambda_2 = 663.1 * 10**(-9)


    lambda_3 = 649.1 * 10**(-9)
    lambda_4 = 654.1 * 10**(-9)
    c = 299792458
    
    
    #mass of the hydrogen atom  in kg 
    m = 3.3 * 10**(-27) 
    
   
    
    #s_l  array
    s_l = np.array([-220.2 , -165.2, -137.7, -110.2, -82.64, -55.1, -27.56, 0, 27.57, 55.15, 82.74, 110.3, 138.0, 165.6, 220.9]) * 10**(-18)

    #C_l array
    C_l = np.array([1, 18, 16, 1681, 2304, 729, 1936, 5490, 1936, 729, 2304, 1681, 16, 18, 1])
    C_f = np.sum(C_l)

    
    #x and y new 
    x = x*(1.6*10**(-19))*10**3
    y = y*(1.6*10**(-19))*10**3

    #where x - E and y - \mu

    


       
    x, y = np.meshgrid(x, y)
    
    result = np.where(x>=np.abs(y)*B, prob_st(x, y,  s_l, C_l, C_f, m,lambda_0, lambda_1, lambda_2, c,phi_radian, B,cross_V ), 0) + np.where(x>=np.abs(y)*B, prob_st(x, y,  s_l, C_l, C_f, m,lambda_0, lambda_3, lambda_4, c,phi_radian, B,cross_V ), 0)
    
    return result







def CTS_wf(phi, B, x, y):
   phi_radian =   np.pi*phi/180

   # u input
   u1 = -0.1*10**6
   u2 =  0.1*10**6
   #mass of the hydrogen atom  in kg
   m = 3.3 * 10**(-27)


   


   x = x*(1.6*10**(-19))*10**3
   y = y*(1.6*10**(-19))*10**3
   x, y = np.meshgrid(x, y)




   result = np.where(x>=np.abs(y)*B,CTS_WF_real(B, x, y, m, u1, u2, phi_radian), 0)
   result = np.nan_to_num(result)
   return result




def CTS_WF_real(B, x, y, m, u1, u2, phi_radian):
    v_parallel = np.sqrt(np.abs(2 * (x - B * np.abs(y)) / m)) * np.sign(y)
    v_perp = np.sqrt(np.abs(2 * B * np.abs(y) / m))
    rez = WF_CTS(v_parallel,v_perp,u1, u2, phi_radian)
    return rez

def WF_CTS(x,y,u1, u2, phi_radian):

    #gyroangle_1
    arg_1 = (u1 - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
    arg_1_1 = np.where((arg_1 >= -1) & (arg_1 <= 1), arg_1, np.nan)


    #gyroangle_1
    arg_2 = (u2 - x * np.cos(phi_radian))/(y * np.sin(phi_radian))
    arg_2_2 = np.where((arg_2 >= -1) & (arg_2 <= 1), arg_2, np.nan)



    #gyroangle
    gyroangle_1_l = np.arccos(arg_1_1)
    gyroangle_2_l = np.arccos(arg_2_2)



    rez = 1/np.pi * (gyroangle_1_l - gyroangle_2_l)

    result = np.where(rez >= 0, rez, np.nan)
    

    return result
    
   

   
     


   
   
