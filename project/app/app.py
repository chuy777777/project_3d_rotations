import numpy as np
import customtkinter  as ctk
import tkinter as tk

from components.create_frame import CreateFrame
from components.create_scrollable_frame import CreateScrollableFrame
from components.grid_frame import GridFrame
from components.frame_graphic_3D import FrameGraphic3D
from components.text_validator import TextValidator
import components.utils as utils

class FrameApplication(CreateFrame):
    def __init__(self, master, name, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(1,2), arr=None), **kwargs)
        self.factor_degree_to_radian=np.pi / 180
        self.R=np.eye(3)
        self.angle_rad_x=0
        self.angle_rad_y=0
        self.angle_rad_z=0
        self.is_active=False

        self.frame_graphic_3D=FrameGraphic3D(master=self, name="FrameGraphic3D", square_size=1.2, width=700, height=700)
        
        frame_container=CreateScrollableFrame(master=self, name="FrameContainer", grid_frame=GridFrame(dim=(12,3), arr=np.array([["0,0","0,0","0,0"],["1,0","1,1","1,2"],["2,0","2,1","2,2"],["3,0","3,0","3,0"],["4,0","4,0","4,0"],["5,0","5,0","5,0"],["6,0","6,0","6,0"],["7,0","7,0","7,0"],["8,0","8,0","8,0"],["9,0","9,0","9,0"],["10,0","10,0","10,0"],["11,0","11,0","11,0"]])), orientation="vertical")
        label_info=ctk.CTkLabel(master=frame_container, wraplength=200, text="Rotaciones positivas en sentido antihorario\n\nAngulo en grados (°)")
        label_angle_x=ctk.CTkLabel(master=frame_container, text="Angulo X")
        label_angle_y=ctk.CTkLabel(master=frame_container, text="Angulo Y")
        label_angle_z=ctk.CTkLabel(master=frame_container, text="Angulo Z")
        self.var_angle_x=ctk.StringVar(value="0.00")
        self.var_angle_y=ctk.StringVar(value="0.00")
        self.var_angle_z=ctk.StringVar(value="0.00")
        entry_angle_x=ctk.CTkEntry(master=frame_container, width=70, corner_radius=10, textvariable=self.var_angle_x)
        entry_angle_y=ctk.CTkEntry(master=frame_container, width=70, corner_radius=10, textvariable=self.var_angle_y)
        entry_angle_z=ctk.CTkEntry(master=frame_container, width=70, corner_radius=10, textvariable=self.var_angle_z)
        self.var_rotation=ctk.IntVar(value=0)
        radio_button_rxryrz=ctk.CTkRadioButton(master=frame_container, text="RxRyRz", variable=self.var_rotation, value=0)
        radio_button_rzryrx=ctk.CTkRadioButton(master=frame_container, text="RzRyRx", variable=self.var_rotation, value=1)
        label_time=ctk.CTkLabel(master=frame_container, text="Tiempo por rotacion (s)")
        self.var_time=ctk.StringVar(value="1.00")
        entry_time=ctk.CTkEntry(master=frame_container, width=70, corner_radius=10, textvariable=self.var_time)
        self.var_planes=ctk.IntVar(value=1)
        self.var_planes.trace_add("write", self.trace_planes)
        check_box_planes=ctk.CTkCheckBox(master=frame_container, text="Mostrar planos", variable=self.var_planes, onvalue=1, offvalue=0)
        button_init=ctk.CTkButton(master=frame_container, text="Inicializar", text_color="black", fg_color="LightPink1", hover_color="LightPink2", command=self.init)
        button_start=ctk.CTkButton(master=frame_container, text="Comenzar", text_color="black", fg_color="OliveDrab1", hover_color="OliveDrab2", command=self.start)
        button_restart_graphic=ctk.CTkButton(master=frame_container, text="Restaurar grafico", text_color="white", fg_color="MediumPurple1", hover_color="MediumPurple2", command=self.restart_graphic)
        self.var_status=ctk.StringVar(value="")
        label_status=ctk.CTkLabel(master=frame_container, text="", textvariable=self.var_status, wraplength=400, font=ctk.CTkFont(size=18, weight="bold"))
        frame_container.insert_element(cad_pos="0,0", element=label_info, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="1,0", element=label_angle_x, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="1,1", element=label_angle_y, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="1,2", element=label_angle_z, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="2,0", element=entry_angle_x, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="2,1", element=entry_angle_y, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="2,2", element=entry_angle_z, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="3,0", element=radio_button_rxryrz, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="4,0", element=radio_button_rzryrx, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="5,0", element=label_time, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="6,0", element=entry_time, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="7,0", element=check_box_planes, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="8,0", element=button_init, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="9,0", element=button_start, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="10,0", element=button_restart_graphic, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="11,0", element=label_status, padx=5, pady=5, sticky="")

        self.insert_element(cad_pos="0,0", element=self.frame_graphic_3D, padx=5, pady=5, sticky="nsew")
        self.insert_element(cad_pos="0,1", element=frame_container, padx=5, pady=5, sticky="nsew")

        self.init()

    def trace_planes(self, var, index, mode):
        self.plot_coordinate_system()

    def plot_coordinate_system(self):
        self.frame_graphic_3D.clear() 
        if self.var_planes.get():
            square_size=self.frame_graphic_3D.square_size
            verts_list=[
                np.array([[-square_size,-square_size,0],[-square_size,square_size,0],[square_size,square_size,0],[square_size,-square_size,0]]),
                np.array([[0,-square_size,square_size],[0,square_size,square_size],[0,square_size,-square_size],[0,-square_size,-square_size]]),
                np.array([[square_size,0,square_size],[-square_size,0,square_size],[-square_size,0,-square_size],[square_size,0,-square_size]])
            ]
            for verts in verts_list:
                self.frame_graphic_3D.plot_polygon(verts, alpha=0.1, facecolors="blue", edgecolors="black")
        self.frame_graphic_3D.plot_coordinate_system(t_list=[np.zeros((3,1))], T_list=[self.R], length=1, show_axis_text=True)
        self.frame_graphic_3D.draw()

    def individual_rotation(self, R_accum, angle_rad, rot_name, t, time):
        self.var_status.set(value="\nRotacion en {}...".format(rot_name))  
        angle=angle_rad * (t / time)
        if rot_name == "X": self.R=R_accum @ utils.Rx(psi=angle)
        if rot_name == "Y": self.R=R_accum @ utils.Ry(theta=angle)
        if rot_name == "Z": self.R=R_accum @ utils.Rz(phi=angle)
        self.plot_coordinate_system()

    def start_routine(self, time, rot, angle_rad_x, angle_rad_y, angle_rad_z, t=0):
        ms_after=50
        if rot == 0: # RxRyRz
            if time > 0:
                if t < time and angle_rad_x != 0:
                    self.individual_rotation(R_accum=np.eye(3), angle_rad=angle_rad_x, rot_name="X", t=t, time=time)
                    t=t + ms_after / 1000
                    if t > time:
                        t=0
                        angle_rad_x=0
                    self.after(ms_after, lambda: self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z, t=t))
                elif t < time and angle_rad_y != 0:
                    self.individual_rotation(R_accum=utils.Rx(psi=self.angle_rad_x), angle_rad=angle_rad_y, rot_name="Y", t=t, time=time)
                    t=t + ms_after / 1000
                    if t > time:
                        t=0
                        angle_rad_y=0
                    self.after(ms_after, lambda: self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z, t=t))
                elif t < time and angle_rad_z != 0:
                    self.individual_rotation(R_accum=utils.Rx(psi=self.angle_rad_x) @ utils.Ry(theta=self.angle_rad_y), angle_rad=angle_rad_z, rot_name="Z", t=t, time=time)
                    t=t + ms_after / 1000
                    if t > time:
                        t=0
                        angle_rad_z=0
                    self.after(ms_after, lambda: self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z, t=t))
                else:
                    self.R=utils.RxRyRz(psi=self.angle_rad_x, theta=self.angle_rad_y, phi=self.angle_rad_z)
                    self.plot_coordinate_system()
                    self.is_active=False
                    self.var_status.set(value="\nMatriz de rotacion:\n\n{}".format(np.array2string(self.R, precision=4)))
            else:
                self.R=utils.RxRyRz(psi=self.angle_rad_x, theta=self.angle_rad_y, phi=self.angle_rad_z)
                self.plot_coordinate_system()
                self.is_active=False
                self.var_status.set(value="\nMatriz de rotacion:\n\n{}".format(np.array2string(self.R, precision=4)))
        if rot == 1: # RzRyRx
            if time > 0:
                if t < time and angle_rad_z != 0:
                    self.individual_rotation(R_accum=np.eye(3), angle_rad=angle_rad_z, rot_name="Z", t=t, time=time)
                    t=t + ms_after / 1000
                    if t > time:
                        t=0
                        angle_rad_z=0
                    self.after(ms_after, lambda: self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z, t=t))
                elif t < time and angle_rad_y != 0:
                    self.individual_rotation(R_accum=utils.Rz(phi=self.angle_rad_z), angle_rad=angle_rad_y, rot_name="Y", t=t, time=time)
                    t=t + ms_after / 1000
                    if t > time:
                        t=0
                        angle_rad_y=0
                    self.after(ms_after, lambda: self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z, t=t))
                elif t < time and angle_rad_x != 0:
                    self.individual_rotation(R_accum=utils.Rz(phi=self.angle_rad_z) @ utils.Ry(theta=self.angle_rad_y), angle_rad=angle_rad_x, rot_name="X", t=t, time=time)
                    t=t + ms_after / 1000
                    if t > time:
                        t=0
                        angle_rad_x=0
                    self.after(ms_after, lambda: self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z, t=t))
                else:
                    self.R=utils.RzRyRx(psi=self.angle_rad_x, theta=self.angle_rad_y, phi=self.angle_rad_z)
                    self.plot_coordinate_system()
                    self.is_active=False
                    self.var_status.set(value="\nMatriz de rotacion:\n\n{}".format(np.array2string(self.R, precision=4)))
            else:
                self.R=utils.RzRyRx(psi=self.angle_rad_x, theta=self.angle_rad_y, phi=self.angle_rad_z)
                self.plot_coordinate_system()
                self.is_active=False
                self.var_status.set(value="\nMatriz de rotacion:\n\n{}".format(np.array2string(self.R, precision=4)))
        
    def init(self):
        if not self.is_active:
            self.R=np.eye(3)
            self.angle_rad_x=0
            self.angle_rad_y=0
            self.angle_rad_z=0
            self.var_status.set(value="")
            self.plot_coordinate_system()

    def start(self):
        angle_x=TextValidator.validate_number(text=self.var_angle_x.get())
        angle_y=TextValidator.validate_number(text=self.var_angle_y.get())
        angle_z=TextValidator.validate_number(text=self.var_angle_z.get())
        time=TextValidator.validate_number(text=self.var_time.get())
        if angle_x is not None and angle_y is not None and angle_z is not None:
            if time is not None and time >= 0 and time <= 10:
                if not self.is_active:
                    self.init()

                    rot=self.var_rotation.get()
                    angle_rad_x=angle_x * self.factor_degree_to_radian
                    angle_rad_y=angle_y * self.factor_degree_to_radian
                    angle_rad_z=angle_z * self.factor_degree_to_radian
                    self.angle_rad_x=angle_rad_x
                    self.angle_rad_y=angle_rad_y
                    self.angle_rad_z=angle_rad_z
                
                    self.is_active=True
                    self.start_routine(time=time, rot=rot, angle_rad_x=angle_rad_x, angle_rad_y=angle_rad_y, angle_rad_z=angle_rad_z)
            else:
                tk.messagebox.showinfo(title="Tiempo", message="El tiempo no es correcto. Favor de verificarlo.\n\nEl tiempo debe estar entre 0 y 10 segundos.")
        else:
            tk.messagebox.showinfo(title="Angulos", message="Los angulos no son correctos. Favor de verificarlos.")
        
    def restart_graphic(self):
        self.frame_graphic_3D.initial_configurations()
        self.frame_graphic_3D.draw()

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)

        # Configuramos nuestra aplicacion
        self.geometry("1366x768")
        self.title("Rotaciones 3D")

        # Configuramos el sistema de cuadricula
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Creamos un frame root
        self.frame_root=CreateFrame(master=self, name="FrameRoot", grid_frame=GridFrame(dim=(1,1), arr=None))
        
        # Colocamos el frame root en la cuadricula
        self.frame_root.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") # Al agregar sticky='nsew' el frame pasa de widthxheight a abarcar todo el espacio disponible

        # Creamos el elemento principal 
        self.frame_application=FrameApplication(master=self.frame_root, name="FrameApplication")

        # Insertamos el elemento principal
        self.frame_root.insert_element(cad_pos="0,0", element=self.frame_application, padx=5, pady=5, sticky="nsew")

        # Configuramos el cerrado de la ventana
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self):
        ctk.CTk.quit(self)
        ctk.CTk.destroy(self)

if __name__ == "__main__":
    # Configuramos e iniciamos la aplicacion
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("green")
    app=App()
    app.mainloop()