import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from mpl_toolkits.axes_grid1 import make_axes_locatable
import Load_Final_DATA.Input_ALL_DATA as Inp
import Weight_Fuction.WF_FIDA as WF
import numpy as np
import Magnetic_Field.Mag_field as MF
import math
from datetime import datetime



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
 
        # configure window
        self.title("Ivan")
        self.geometry(f"{1520}x{900}")
        self.data_instance = Data()

        # Section 1: Sidebar
        self.create_sidebar()


        # Section 3: Textbox, Tabview, Radiobuttons, Slider, and Progressbar
        self.create_additional_widgets()

        # set default values
        self.nbi_optionmenu.set(self.nbi_options[0])
        self.logo_label.configure(text="Diagnostic.alpha")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # Initialize Port Options
        self.update_port_options(self.nbi_options[0])
         
        self.current_graph = None
        self.all_results=[]


    def pre_calculate(self):
        self.Name_Ports = ['2_1_AEA', '2_1_AEA', '2_1_AEM', '2_1_AEM', '2_1_AET', '2_1_AET'] 
        self.Name_NBI = ['NBI_7', 'NBI_8', 'NBI_7', 'NBI_8', 'NBI_7', 'NBI_8' ]
        if len(self.all_results) ==0:
         Result_array = self.create_result_array_old()  
         self.all_results = Result_array
        else:
            self.all_results = self.all_results[:6]

 
        time = datetime.now().strftime("%H:%M:%S")
        self.textbox.insert("end", f"\n\n [{time}]: Old data ready \n\n ")
        

        
        
        
    def create_sidebar(self):
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FIDA", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
       
        self.show_old_button_label= ctk.CTkLabel(self.sidebar_frame, text="Raw data:", anchor="w")    
        self.show_old_button_label.grid(row=2, column=0, padx=20, pady=(300,0))     
        self.show_old_button = ctk.CTkButton(self.sidebar_frame, text="Update data", command=lambda: self.pre_calculate())
        self.show_old_button.grid(row=2, column=0, padx=20, pady=(360,0))
        
        
        self.Diagnostics_label = ctk.CTkLabel(self.sidebar_frame, text="Diagnostics:", anchor="w")
        self.Diagnostics_label.grid(row=3, column=0, padx=20, pady=(10,0))
        self.Diagnostics_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["FIDA", "CTS"])
        self.Diagnostics_optionemenu.grid(row=4, column=0, padx=20, pady=(0, 10))
        
        

        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
      

    def create_additional_widgets(self):
        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Button to show graph
        self.show_graph_button = ctk.CTkButton(self, text="Add Port", command=lambda: self.dummy_function())

        self.show_graph_button.grid(row=1, column=1, padx=(20, 0), pady=(10, 0), sticky="w")

        # create tabview with two sections
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Section 1: "PORTS and NBI"
        self.tabview.add("PORTS and NBI")
        self.tabview.tab("PORTS and NBI").grid_columnconfigure(0, weight=1)

        # First CTkOptionMenu for NBI selection
        self.nbi_options = self.generate_nbi_options()
        self.nbi_optionmenu_label = ctk.CTkLabel(self.tabview.tab("PORTS and NBI"), text="Select NBI or Gyrotron Launcher", anchor="w")
        self.nbi_optionmenu_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.nbi_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("PORTS and NBI"), values=self.nbi_options, command=self.update_port_options)
        self.nbi_optionmenu.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # Second CTkOptionMenu for Port selection (based on NBI selection)
        self.port_options = []
        self.port_optionmenu_label = ctk.CTkLabel(self.tabview.tab("PORTS and NBI"), text="Select Port", anchor="w")
        self.port_optionmenu_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.port_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("PORTS and NBI"), values=self.port_options)
        self.port_optionmenu.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")

        # Section 2: "New Ports and NBI"
        self.tabview.add("New Ports and NBI")
        self.tabview.tab("New Ports and NBI").grid_columnconfigure(0, weight=1)

        # Canvas for displaying the graph
        self.graph_canvas = ctk.CTkCanvas(self, width=800, height=600, bg="white")
        self.graph_canvas.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def generate_nbi_options(self):
      return [f"NBI_{i}" if i <= 8 else f"CTS_{i-8}" for i in range(1, 12)]


    def generate_port_options(self, selected_nbi: str):
        nbi_index = int(selected_nbi.split("_")[1])
        if selected_nbi.startswith("CTS"):
         nbi_index = nbi_index+8
        
        nbi_index = nbi_index-1
        Ports = Inp.NBI_and_Ports()
        Ports_for_NBI_Index = Ports[nbi_index][0]
        return Ports_for_NBI_Index 

    def update_port_options(self, selected_nbi: str):
        self.port_options = self.generate_port_options(selected_nbi)

        # Configure the values directly
        self.port_optionmenu.configure(values=self.port_options)

        # Set the initial value for Select Port (if the list is not empty)
        if self.port_options:
            self.port_optionmenu.set(self.port_options[0])
            
            
    def create_result_array_for_port(self, NBI_seected_points, Point_P_2):
        Dia = self.Diagnostics_optionemenu.get()
        B,vector_B =MF.mag_field(NBI_seected_points[0], NBI_seected_points[1], NBI_seected_points[2])


        #Arrays
        Angle = []
        Result_for_NBI_Port_new = []


        #Find_angles
        if Dia =="FIDA":
         for i in range(len(NBI_seected_points[0])):
            Vector1 = (NBI_seected_points[0][i]-Point_P_2[0],   NBI_seected_points[1][i]-Point_P_2[1], NBI_seected_points[2][i]-Point_P_2[2])
            vector2 = (vector_B[0][i],vector_B[1][i], vector_B[2][i])
            Angle_1 = angle_between_vectors(Vector1, vector2)
            Angle.append(Angle_1)

        if Dia =="CTS":
         for i in range(len(NBI_seected_points[0])):
             Vector_k_s = (NBI_seected_points[0][i]-Point_P_2[0],   NBI_seected_points[1][i]-Point_P_2[1], NBI_seected_points[2][i]-Point_P_2[2])
             vector_mag = (vector_B[0][i],vector_B[1][i], vector_B[2][i])
             Vector_NBI_k_i = (NBI_seected_points[0][4]-NBI_seected_points[0][0],   NBI_seected_points[1][4]-NBI_seected_points[1][0], NBI_seected_points[2][4]-NBI_seected_points[2][0])
             Vector_k_delta = (Vector_k_s[0] - Vector_NBI_k_i[0],
                  Vector_k_s[1] - Vector_NBI_k_i[1],
                  Vector_k_s[2] - Vector_NBI_k_i[2])
             Angle_1 = angle_between_vectors(Vector_k_delta, vector_mag)
             Angle.append(Angle_1)

            

        for i in range(len(B)):
         #Obtain_result_of_WF
         if Dia =="FIDA":

            x_ev = np.linspace(10, 100, 100)
            y_ev = np.linspace(-100, 100, 100)/B[i]
            result = WF.weight_Function(Angle[i], B[i], x_ev, y_ev)
            Result_for_NBI_Port_new.append(result)
         if Dia =="CTS":
            x_ev = np.linspace(1, 6, 100)
            y_ev = np.linspace(-6, 6, 100)/B[i]
            result = WF.CTS_wf(Angle[i], B[i], x_ev, y_ev)   
            Result_for_NBI_Port_new.append(result)
        #print("len(Result) = ",len(Result_for_NBI_Port_new))
        
        
        return Result_for_NBI_Port_new
        

    def create_result_array_old(self):
        Result_array = []
        for i in range(len(self.Name_NBI)):
            n_nbi = str(self.Name_NBI[i])
            n_port = str(self.Name_Ports[i])
            NBI_seected_points, Point_P= self.data_instance.class_data(n_nbi, n_port)
            NBI_seected_points = np.array(NBI_seected_points)/100
            Result_for_NBI_Port= self.create_result_array_for_port(NBI_seected_points, Point_P)
            Result_array.append(Result_for_NBI_Port)
        
        return Result_array
        
    
    def generate_and_show_graph(self):
        #User
        selected_nbi = self.nbi_optionmenu.get()
        selected_port = self.port_optionmenu.get()
        
        #Data
        self.Name_NBI.append(selected_nbi)
        self.Name_Ports.append(selected_port)
        print(self.Name_NBI)
        NBI_seected_points, Point_P_2= self.data_instance.class_data(selected_nbi, selected_port)
        NBI_seected_points = np.array(NBI_seected_points)/100

        Result_for_NBI_Port_NEW= self.create_result_array_for_port(NBI_seected_points, Point_P_2)
    
        # Clear previous graph
        if self.current_graph:
            self.current_graph.get_tk_widget().destroy()


        self.all_results.append(Result_for_NBI_Port_NEW)
        # Draw the new graph on the canvas
        self.draw_graph_on_canvas(self.all_results)
        
        
        
        
    def dummy_function(self):
        #User 
        selected_nbi = self.nbi_optionmenu.get()
        selected_port = self.port_optionmenu.get()
        Dia = self.Diagnostics_optionemenu.get()
        
        #Time
        timestamp = datetime.now().strftime("%H:%M:%S")
          
        #Message  
        message = f"[{timestamp}]: {Dia}:\n\nSelected Port:    {selected_port}\nSelected:     {selected_nbi}\n\n"
        self.textbox.insert("end", message)


        self.generate_and_show_graph()
        
        
    def draw_graph_on_canvas(self, Result_for_NBI_Port):
        num_arrays = len(Result_for_NBI_Port)
            
        # Create a matplotlib figure
        fig, axs = plt.subplots(num_arrays, num_arrays, figsize=(8, 8))
        if num_arrays == 1:
         MATRIX = self.suummmm(Result_for_NBI_Port[0], Result_for_NBI_Port[0])
         #min_value = np.min(MATRIX)
         #max_value = np.max(MATRIX)
         im = axs.imshow(MATRIX, cmap='jet', origin='upper', aspect='auto', vmin=0.0, vmax=1.0)
         axs.set_xticks([])
         axs.set_yticks([])
        else:
         for i in range(num_arrays):
            for j in range(num_arrays):

                MATRIX = self.suummmm(Result_for_NBI_Port[i], Result_for_NBI_Port[j])
                min_value = np.min(MATRIX)
                max_value = np.max(MATRIX)
                im = axs[i, j].imshow(MATRIX, cmap='jet', origin='upper', aspect='auto', vmin=0, vmax=1.0)
                axs[i, j].set_xticks([])
                axs[i, j].set_yticks([])

        plt.subplots_adjust(wspace=0, hspace=0)
        
        
        # Add colorbar to the last subplot
        cax = fig.add_axes([0.93, 0.15, 0.02, 0.7])  # [x, y, width, height]
        plt.colorbar(im, cax=cax)


        for i in range(num_arrays):
            if num_arrays>=11:
                fonts = 6
            else:
                fonts = 9

            selected_nbi = self.Name_NBI[i]
            selected_port = self.Name_Ports[i]
            if selected_nbi[0] == 'N':
               name = 'S'
            else:
               name = 'C'
            axs[num_arrays-1, i].set_xlabel(f'{selected_port[0]}{selected_port[2]}{selected_port[4:]}.{name}{selected_nbi[4]}', fontsize=fonts)
            axs[i, 0].set_ylabel(f'{selected_port[0]}{selected_port[2]}{selected_port[4:]}.{name}{selected_nbi[4]}', fontsize=fonts)



        

        #plt.title('FIDA')
        plt.close('all')

        # Embed the matplotlib figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

        # Update the current graph reference
        self.current_graph = canvas
        
        
    
            
    def suummmm(self,array_1, array_2):
            MATRIX = np.zeros((len(array_1), len(array_2)))
            for i in range(len(array_1)):
                for j in range(len(array_2)):
                    MATRIX[i, j] = np.sum(array_1[i] * array_2[j])
            MATRIX = MATRIX/np.max(MATRIX)

            return MATRIX





class Data:
    def class_data(self, selected_nbi, selected_port):
        
        #input data 
        Ports_For_NBI = Inp.NBI_and_Ports()
        
        #input select
        index_NBI, index_Port = self.find_data(selected_nbi, selected_port, Ports_For_NBI)
        
        #DATA
        P_1, P_2_new = Inp.new_Ports()
        NBI_start, NBI_end = Inp.new_NBI()
        index_Port_in_general = int(Ports_For_NBI[index_NBI][3][index_Port])

        
        #NBI_data
        NBI_points = self.points_on_line_NBI(NBI_start, NBI_end)
        
        
        #Find Points_of_LIne
              
        NBI_Points_start = [NBI_points[0][index_NBI][int(Ports_For_NBI[index_NBI][1][index_Port])], NBI_points[1][index_NBI][int(Ports_For_NBI[index_NBI][1][index_Port])], NBI_points[2][index_NBI][int(Ports_For_NBI[index_NBI][1][index_Port])]]      
        NBI_Points_end = [NBI_points[0][index_NBI][int(Ports_For_NBI[index_NBI][2][index_Port])], NBI_points[1][index_NBI][int(Ports_For_NBI[index_NBI][2][index_Port])], NBI_points[2][index_NBI][int(Ports_For_NBI[index_NBI][2][index_Port])]]
        NBI_seected_points = self.Points_on_NBI(NBI_Points_start, NBI_Points_end, 103)
        
        #Ports_input_P_2
        
        Point_p_2 = (P_2_new[0][index_Port_in_general], P_2_new[1][index_Port_in_general], P_2_new[2][index_Port_in_general])
    
        return NBI_seected_points, Point_p_2

    def find_data(self, selected_nbi, selected_port, Ports_For_NBI):
        # Find index selected value
        index_NBI = int(int(selected_nbi.split('_')[1]) - 1)
        if selected_nbi.startswith("CTS"):
         index_NBI = index_NBI+8

        index_Port = Ports_For_NBI[index_NBI][0].index(selected_port)
        return index_NBI, index_Port

    def POints_find(self, index_NBI,  index_Port, Ports_For_NBI):
        Arr_index=[]
        n = Ports_For_NBI[index_NBI][2][index_Port] -Ports_For_NBI[index_NBI][1][index_Port]
        for i in range(int(n)+1):
            index = Ports_For_NBI[index_NBI][1][index_Port] + i
            Arr_index.append(index)
        
        return Arr_index

    def points_on_line_NBI(self, NBI_start, NBI_end):

         X_point_on_NBI = [np.array([]) for _ in range(len(NBI_start[0]))]
         Y_point_on_NBI = [np.array([]) for _ in range(len(NBI_start[0]))]
         Z_point_on_NBI = [np.array([]) for _ in range(len(NBI_start[0]))]
         
         for i in range(len(NBI_end[0])):
             k_x = (NBI_end[0][i] - NBI_start[0][i])
             k_y = (NBI_end[1][i] - NBI_start[1][i])
             k_z = (NBI_end[2][i] - NBI_start[2][i])


             for j in range(21):

                 x_k = NBI_start[0][i] + k_x * (j / 20)
                 y_k = NBI_start[1][i] + k_y * (j / 20)
                 z_k = NBI_start[2][i] + k_z * (j / 20)
                 
                 
                 if j !=0 and j != 20:
                  X_point_on_NBI[i] = np.append(X_point_on_NBI[i], x_k)
                  Y_point_on_NBI[i] = np.append(Y_point_on_NBI[i], y_k)
                  Z_point_on_NBI[i] = np.append(Z_point_on_NBI[i], z_k)

         NBI_points = np.array([X_point_on_NBI, Y_point_on_NBI, Z_point_on_NBI])
         return NBI_points 
    
    def Points_on_NBI(self, NBI_Points_start, NBI_Points_end, N):

         X_point_on_NBI = np.array([])
         Y_point_on_NBI = np.array([])
         Z_point_on_NBI = np.array([])
         
         
         k_x = (NBI_Points_end[0] - NBI_Points_start[0])
         k_y = (NBI_Points_end[1] - NBI_Points_start[1])
         k_z = (NBI_Points_end[2] - NBI_Points_start[2])


         for j in range(N):

                 x_k = NBI_Points_start[0] + k_x * (j / (N-1))
                 y_k = NBI_Points_start[1] + k_y * (j / (N-1))
                 z_k = NBI_Points_start[2] + k_z * (j / (N-1))
                 
                 
                 
                 X_point_on_NBI = np.append(X_point_on_NBI, x_k)
                 Y_point_on_NBI = np.append(Y_point_on_NBI, y_k)
                 Z_point_on_NBI = np.append(Z_point_on_NBI, z_k)

         NBI_points = np.array([X_point_on_NBI, Y_point_on_NBI, Z_point_on_NBI])
         return NBI_points

    def find_point_on_NBI(self, Array_points_on_selected_NBI_and_Port, NBI_points, index_NBI):
        NBI_seected_points = [[],[],[]]
        for i in range(len(Array_points_on_selected_NBI_and_Port)):
            j = int(Array_points_on_selected_NBI_and_Port[i])
            NBI_seected_points[0].append(NBI_points[0][index_NBI][j])
            NBI_seected_points[1].append(NBI_points[1][index_NBI][j])
            NBI_seected_points[2].append(NBI_points[2][index_NBI][j])
        return NBI_seected_points
    
def angle_between_vectors(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    norm1 = math.sqrt(sum(a**2 for a in vector1))
    norm2 = math.sqrt(sum(b**2 for b in vector2))

    cosine_theta = dot_product / (norm1 * norm2)
    angle_in_radians = math.acos(cosine_theta)


    angle_in_degrees = math.degrees(angle_in_radians)

    return angle_in_degrees

if __name__ == "__main__":
    app = App()
    app.mainloop()
