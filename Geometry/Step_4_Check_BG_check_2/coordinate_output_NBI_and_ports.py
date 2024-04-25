import numpy as np
import pandas as pd
import os


def new_Ports():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'Result_NBI_and_Ports', 'New_coordinate_step_1.xlsx')
        df = pd.read_excel(file_path)
    
    
    # P_2_new

        P_new_2_X = df.iloc[4:, 7].tolist() #4 row 5 colum 
        P_new_2_Y = df.iloc[4:, 8].tolist() #4 row 6 colum 
        P_new_2_Z = df.iloc[4:, 9].tolist() #4 row 7 colum
        
        P_new_2_X = [float(value) for value in P_new_2_X]
        P_new_2_Y = [float(value) for value in P_new_2_Y]
        P_new_2_Z = [float(value) for value in P_new_2_Z]
        

        
        P_2_new = [P_new_2_X, P_new_2_Y, P_new_2_Z]
        P_2_new = np.array(P_2_new)
    
    
    #P_1 OLD

        P_1_X_old = df.iloc[4:, 4].tolist() #4 row 3 colum 
        P_1_Y_old = df.iloc[4:, 5].tolist() #4 row 4 colum 
        P_1_Z_old = df.iloc[4:, 6].tolist() #4 row 5 colum
        
        P_1_X_old = [float(value) for value in P_1_X_old]
        P_1_Y_old = [float(value) for value in P_1_Y_old]
        P_1_Z_old = [float(value) for value in P_1_Z_old]
            

            
        P_1_old = [P_1_X_old, P_1_Y_old, P_1_Z_old]
        P_1_old = np.array(P_1_old)   
        
        
        
        return P_1_old, P_2_new
    

def new_NBI():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'Step_2_New_NBI_Coordinates','Result_NBI', 'New_coordinate_NBI_GT.xlsx')
        df = pd.read_excel(file_path)
    
    
    
    # NBI_start 

        NBI_start_X = df.iloc[4:, 4].tolist() #4 row 5 colum 
        NBI_start_Y = df.iloc[4:, 5].tolist() #4 row 6 colum 
        NBI_start_Z = df.iloc[4:, 6].tolist() #4 row 7 colum
        
        NBI_start_X = [float(value) for value in NBI_start_X]
        NBI_start_Y = [float(value) for value in NBI_start_Y]
        NBI_start_Z = [float(value) for value in NBI_start_Z]
        

        
        NBI_start = [NBI_start_X, NBI_start_Y, NBI_start_Z]
        NBI_start= np.array(NBI_start)
    
    
    #NBI_end

        NBI_end_X = df.iloc[4:, 7].tolist() #4 row 3 colum 
        NBI_end_Y = df.iloc[4:, 8].tolist() #4 row 4 colum 
        NBI_end_Z = df.iloc[4:, 9].tolist() #4 row 5 colum
        
        NBI_end_X = [float(value) for value in NBI_end_X]
        NBI_end_Y = [float(value) for value in NBI_end_Y]
        NBI_end_Z = [float(value) for value in NBI_end_Z]
            

            
        NBI_end = [NBI_end_X, NBI_end_Y, NBI_end_Z]
        NBI_end = np.array(NBI_end)   
        
        
        
        return NBI_start, NBI_end
    



def good_ports_1():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'Step_3_Check_BG_Ports','Result_BG_Ports', 'Number_Good_Ports_and_NBI_14_03.xlsx')
    # file_path = os.path.join(current_dir, '..', 'Step_4_Check_BG_check_2','Result_Angle', 'Step_4_15_85_23.04.xlsx')
    df = pd.read_excel(file_path)
    
    # Good_Ports
    
    Good_ports = df.iloc[4:, 4].tolist() #4 row 5 colum 
    Good_NBI = df.iloc[4:, 5].tolist() #4 row 5 colum 

    Good_PN = [Good_ports, Good_NBI]   
    
    return np.array(Good_PN)

