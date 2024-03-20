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

        P_1_X = df.iloc[4:, 4].tolist() #4 row 3 colum 
        P_1_Y = df.iloc[4:, 5].tolist() #4 row 4 colum 
        P_1_Z = df.iloc[4:, 6].tolist() #4 row 5 colum
        
        P_1_X = [float(value) for value in P_1_X]
        P_1_Y = [float(value) for value in P_1_Y]
        P_1_Z = [float(value) for value in P_1_Z]
            

            
        P_1 = [P_1_X, P_1_Y, P_1_Z]
        P_1 = np.array(P_1)   
        
        
        
        return P_1, P_2_new
    

def new_NBI():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..','Geometry','Step_2_New_NBI_Coordinates', 'Result_NBI', 'New_coordinate_NBI_GT.xlsx')
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
    



#def good_ports_1():
 #   current_dir = os.path.dirname(os.path.abspath(__file__))
  #  file_path = os.path.join(current_dir, 'Result_BG_Ports', 'Number_Good_Ports_and_NBI.xlsx')
   # df = pd.read_excel(file_path)
    
    # Good_Ports
    
   # Good_ports = df.iloc[4:, 4].tolist() #4 row 5 colum 
   # Good_NBI = df.iloc[4:, 5].tolist() #4 row 5 colum 

   # Good_PN = [Good_ports, Good_NBI]   
    
   # return np.array(Good_PN)




def result_angle_check():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir,'..','Geometry','Step_4_Check_BG_check_2', 'Result_Angle', 'Number_Good_Ports_and_NBI_AND_INDEX_15_80.xlsx')
    df = pd.read_excel(file_path)
    
    Good_ports = df.iloc[4:, 4].tolist() #4 row 5 colum 
    Good_NBI = df.iloc[4:, 5].tolist() #4 row 5 colum 
    Angle_Start_for_NBI_Port = df.iloc[4:, 6].tolist()
    Angle_END_for_NBI_Port = df.iloc[4:, 7].tolist()
    
    Geometry = [Good_ports, Good_NBI,Angle_Start_for_NBI_Port, Angle_END_for_NBI_Port ]
    return Geometry

def Name_of_Port():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'Input_data', 'Ports_Coordinates.xlsx')
    df = pd.read_excel(file_path)
    
    Port_type = df.iloc[2:, 1].tolist() #4 row 5 colum 
    Port_Module = df.iloc[2:, 2].tolist() #4 row 5 colum 
    Port_SubModule = df.iloc[2:, 3].tolist()

    
    Ports = [Port_type, Port_Module,Port_SubModule ]
    
    return Ports


def correct_Port():
    Ports = Name_of_Port()
    
    for i in range(len(Ports[2])):
        if Ports[2][i] == "rotation":
            Ports[2][i] = 1

    Ports_name = [ str(int(Ports[1][i])) + "_" + str(int(Ports[2][i])) + "_" + Ports[0][i][2:]  for i in range(len(Ports[0]))]

    
    return Ports_name
    

def NBI_and_Ports():
    Ports_name = correct_Port()
    Geometry = result_angle_check()
    
    
    Ports_For_NBI = [[[],[],[],[]] for _ in range(11)]
    
    
    for i in range(len(Geometry[0])):
        j= int(Geometry[0][i])
        k = int(Geometry[1][i]-1)
        Ports_For_NBI[k][0].append(Ports_name[j-1])
        Ports_For_NBI[k][1].append(Geometry[2][i])
        Ports_For_NBI[k][2].append(Geometry[3][i])
        Ports_For_NBI[k][3].append(j-1)
    
    return Ports_For_NBI
    
           
            
            
            
            
    