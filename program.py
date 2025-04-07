# from gui_parser import *
# #Imports___________________________________________________________#
# from pathlib import Path
# from pynput.mouse import Controller, Button                        # Allows us to control mouse
# from radar_filter import *
# from oob_gesture_model import gesture_recognition_model
# import tkinter as tk
# from tkinter import ttk
# import threading
# from Frame_gen import run_frame_gen
# import queue
# import random
# import time                                                        # Allows us to add delays
# import serial.tools.list_ports
# cwd = Path.cwd()
# model_path = cwd.joinpath("resources", "New_Gesture_CNN3.keras")
# scaler_path = cwd.joinpath("resources", "new_gesture_scaler3.bin")
# cfg_path = cwd.joinpath("resources", "radar.cfg")
#
# ports = serial.tools.list_ports.comports()
# data_port = ''
# com_port = ''
# for port, desc, hwid in sorted(ports):
#         # print("{}: {} [{}]".format(port, desc, hwid)) #Displays all ports
#         if "UART Bridge: Standard" in desc: #Data port
#             data_port = port
#         if "UART Bridge: Enhanced" in desc: #COM port
#             com_port = port
#                                                                    #
# #Settings__________________________________________________________# These variables let us change different factors
# XScale = 1100                                                      # scales the X and Y movements by the value (must be int)
# YScale = 1150
# mouse_smoothing = "Velocity"
# frame_gen_on_off = 0  # Unchecked = 0 (off), Checked = 1 (on)
# frame_gen_frames = 1     # Default value, range 1 to 20
# Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
# Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
# Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
# Refresh_Rate = 30                                                  # refreshrate of the board/data
# # Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo
#
# #-----------------------------------------------------------------------------
#
# #Velocity Tracking variables
# x_vec = 1                                                          # these variable are temporary
# y_vec = 1                                                          #
# data_points = []                                                   # stores num_points for frames //Only 2 are need for velocity calculations
# point_clouds = []                                                  # stores point clouds for frames
# mouse = Controller()                                               # Start mouse controller
# xvels = []                                                         # stores x-velocities calculated from 2 frames
# yvels = []                                                         # stores y-velocities calculated from 2 frames
# num_vels = 0                                                       # tracks num of velocities
#
# prev_x = 0
# prev_y = 0
#
# #-------------------------------------------------------------------------------
# #Position Tracking Variables
# x_array = []
# z_array = []
# prev_posX = 0
# prev_posY = 0
#
# #-------------------------------------------------------------------------------
#
# # Custom color scheme
# BG_COLOR = "#f0f0f0"
# BUTTON_COLOR = "#4a7a8c"
# TEXT_BG = "#2e2e2e"
# TEXT_FG = "#00ff00"
#
# def gesture_action(cur_gest, prev_gest, gesture_map):
#     if(cur_gest == 0):
#         return prev_gest
#     else:
#         if(cur_gest != prev_gest):
#             map_action(False, gesture_map[cur_gest])
#             return cur_gest
#         else:
#             map_action(True, gesture_map[cur_gest])
#             return 0
#
# def map_action(repeat_bol, mouse_action):
#     if(mouse_action == "LEFT_HOLD_RELEASE"):
#         if(repeat_bol): mouse.release(Button.left)
#         else: mouse.press(Button.left)
#     if(mouse_action == "RIGHT_CLICK"):
#         mouse.click(Button.right)
#     if(mouse_action == "DOUBLE_LEFT"):
#         mouse.click(Button.left, 2)
#
#
# def get_pos(num_points_1, num_points_2, list1, list2):
#     # the output data from chirp configuration demo in the first frame
#     # num_points = 4 # The chirp configuration demo will output the number of points detected
#     # points = np.array([[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]) # The chirp configuration demo will output the coordinates of the points
#
#     # the output data from chirp configuration demo in the second frame
#     # num_points_2 = 5 # The chirp configuration demo will output the number of points detected
#     # points_2 = np.array([[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]) # The chirp configuration demo will output the coordinates of the points
#     x = 0  # variable for x coordinates in the first frame
#     y = 0  # variable for y coordinates in the first frame
#     x_2 = 0  # variable for x coordinates in the second frame
#     y_2 = 0  # variable for y coordinates in the second frame
#     average_x = 0
#     average_x_2 = 0
#     average_y = 0
#     average_y_2 = 0
#     # average position of the first frame
#     for i in range(num_points_1):  # loop for average position of the first frame
#
#         x += list1[i][0]  # calculate the sum of the magnitude of x coordinates
#         y += list1[i][2]  # calculate the sum of the magnitude of y coordinates
#         average_x = x / num_points_1  # calculate the average coordinate of x axis
#         average_y = y / num_points_1  # calculate the average coordinate of y axis
#
#     # average position of the second frame
#     for i in range(num_points_2):  # loop for average position of the second frame
#
#         x_2 += list2[i][0]  # calculate the sum of the magnitude of x coordinates
#         y_2 += list2[i][2]  # calculate the sum of the magnitude of y coordinates
#         average_x_2 = x_2 / num_points_2  # calculate the average coordinate of x axis
#         average_y_2 = y_2 / num_points_2  # calculate the average coordinate of y axis
#
#     # use average positions to output moving path
#     output_v_x = (average_x_2 - average_x)  # calculate the velocity in x direction
#     output_v_y = (average_y_2 - average_y)  # calculate the velocity in y direction
#
#     # velocity in z-direction is not required because the user is required to move his hand in parallel to the radar's x-y plane
#     print("V_x euqals to ", output_v_x)  # velocity check
#     print("V_y euqals to ", output_v_y)  # velocity check
#     return output_v_x, output_v_y
#
# def track_vel(numPoints, pointCloud):
#     global num_vels, prev_x, prev_y
#     if numPoints == 0:
#         xvels.append(0)
#         yvels.append(0)
#         return True, 0, 0
#
#     pointCloudArray = []  # Blank Array to store pointCloud info
#     for i in range(numPoints):  # Iterates through total number of points detected
#         pointCloudArray.append(pointCloud[i][0:3])  # Pulling X, Y, Z values per point detected
#
#     newPointCloud = filter_ys(pointCloudArray)
#     point_clouds.append(newPointCloud)
#     data_points.append(len(newPointCloud))
#
#     if (len(data_points) > 1):
#         x_vec, y_vec = get_pos(data_points[0], data_points[1], point_clouds[0], point_clouds[1])
#         point_clouds.pop(0)
#         data_points.pop(0)
#
#         if abs(x_vec) < .05: x_vec = 0
#         if abs(y_vec) < .05: y_vec = 0
#         if abs(x_vec) > .3: x_vec = 0
#         if abs(y_vec) > .3: y_vec = 0
#         xvels.append(x_vec)
#         yvels.append(y_vec)
#
#     # if abs(x_vec) > .25 or abs(y_vec) > .25: continue
#     if (len(xvels) == 0): return (True, 0 , 0)
#     while (len(xvels) > 5):
#         xvels.pop(0)
#         yvels.pop(0)
#
#     avg_x = simple_avg(xvels)
#     avg_y = simple_avg(yvels)
#     if abs(avg_y) < .03: avg_y = 0
#     mov_x = (avg_x + prev_x) / 2
#     mov_y = (avg_y + prev_y) / 2
#
#     prev_x = avg_x
#     prev_y = avg_y
#
#     if Switch_XY == 0:  # If we are switching X and Y
#         X = XScale * Reverse_X * mov_x  #
#         Y = YScale * Reverse_Y * mov_y  #
#     elif Switch_XY == 1:
#         X = XScale * Reverse_X * mov_y  #
#         Y = YScale * Reverse_Y * mov_x  #
#     else:
#         print("ERROR: Switch-XY must be a 0 or a 1.")  #
#
#     return False, X, Y
#
# def track_pos(pointCloud):
#     global prev_posX, prev_posY
#
#     x_pos = 0
#     z_pos = 0
#     if (len(pointCloud) == 0): return True, 0, 0
#     newPointCloud = filter_ys(pointCloud)
#     pointer_numPoints = len(newPointCloud)
#     if pointer_numPoints == 0:
#         return True, 0, 0
#     for point in newPointCloud:
#         x_pos += point[0]
#         z_pos += point[2]
#
#     x_pos /= pointer_numPoints
#     z_pos /= pointer_numPoints
#
#     x_array.append(x_pos)
#     z_array.append(z_pos)
#
#     while(len(x_array) > 10):
#         x_array.pop(0)
#         z_array.pop(0)
#
#     avg_x = simple_avg(x_array)
#     avg_z = simple_avg(z_array)
#
#     X = 2560 * (avg_x + .2)/.4
#     Y = 1600 * (avg_z + .2)/.4
#     delta_x = X-prev_posX
#     delta_y = Y-prev_posY
#
#     prev_posX = X
#     prev_posY = Y
#
#     return False, delta_x, delta_y
#
#
# def apply_settings():
#     """Retrieve values from the settings inputs and update globals."""
#     global XScale, YScale, mouse_smoothing
#     global Reverse_X, Reverse_Y, Switch_XY, frame_gen_on_off, frame_gen_frames
#     XScale = sensitivity_x_var.get()
#     YScale = sensitivity_y_var.get()
#     mouse_smoothing = smoothing_var.get()
#     Reverse_X = Reverse_X_var.get()
#     Reverse_Y = Reverse_Y_var.get()
#     Switch_XY = Switch_XY_var.get()
#     frame_gen_on_off = frame_gen_on_off_var.get()
#     frame_gen_frames = frame_gen_frames_var.get()
#     print("Updated Settings:")
#     print("Sensitivity X:", XScale)
#     print("Sensitivity Y:", YScale)
#     print("Mouse Smoothing:", mouse_smoothing)
#     print("Reverse X:", Reverse_X)
#     print("Reverse Y:", Reverse_Y)
#     print("Switch X and Y:", Switch_XY)
#     print("Generated Frames ON/OFF:", frame_gen_on_off)
#     print("Number of Generated Frames:", frame_gen_frames)
#
# #Pointer Positioning
# cfg = open(cfg_path, "r") #Open Config File to send to radar over UART
# my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
# my_parser.connectComPorts(com_port, data_port) #Device-Manager defined Ports
# my_parser.sendCfg(cfg) #Send Config File
# cfg.close() #Close File
#
# model = gesture_recognition_model(model_path, scaler_path)
#
# gesture_names = ["NO_GESTURE", "PUSH", "SHINE", "PULL", "SHAKE"]
# gesture_dict = {0:"NONE",
#                 1:"LEFT_HOLD_RELEASE",
#                 2:"RIGHT_CLICK",
#                 3:"DOUBLE_LEFT",
#                 4:"SCROLL"}
#
# #gesture_dict[1] = 'DOUBLE_LEFT'
#
# frames = 0
# while(frames < model.frames):
#     radarData = my_parser.readAndParseUartDoubleCOMPort() #Parsing Pointer radar data
#     # gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data
#     frameNum = radarData["frameNum"]
#     numPoints = radarData["numDetectedPoints"]
#     pointCloud = radarData["pointCloud"]
#
#     model.fill_frame(numPoints, pointCloud)
#     frames += 1
#
# frames = 0
# DT_counter = 0
# gesture_active = 0
# prev_gest = 0
#
# def radar_loop():
#     global frames
#     global frame_gen_on_off
#     global DT_counter
#     global gesture_active
#     global prev_gest
#     global frame_gen_frames
#     shared_queue = queue.Queue()
#     thread = threading.Thread(target=run_frame_gen, args=(shared_queue, Refresh_Rate, frame_gen_frames))
#
#     thread.start()
#     while (1):  # Radars connected and running, always true until not - Implement GUI?
#         try:
#             radarData = my_parser.readAndParseUartDoubleCOMPort()  # Parsing Pointer radar data
#
#             frameNum = radarData["frameNum"]
#             numPoints = radarData["numDetectedPoints"]
#             pointCloud = radarData["pointCloud"]
#
#
#             model.add_frame(numPoints, pointCloud)
#             frames += 1
#             if gesture_active == False:  # If a gesture isn't active skip frame
#                 if frames % 5 == 0:
#                     cur_gest = model.get_prediction()  # Check for Gesture
#                     print(cur_gest)
#                     if (cur_gest != 0):  # If gesture detected start cooldown
#                         gesture_active = True
#                         prev_gest = gesture_action(cur_gest, prev_gest, gesture_dict)
#             else:  # Cooldown
#                 if (DT_counter < 20):
#                     DT_counter += 1
#                 else:
#                     DT_counter = 0
#                     gesture_active = False
#
#             if(mouse_smoothing == "Velocity"):
#                 print("Here")
#                 skip_bol, X, Y = track_vel(len(pointCloud), pointCloud)
#             else:
#                 skip_bol, X, Y = track_pos(pointCloud)
#             if(skip_bol): continue
#
#             if (frame_gen_on_off):
#                 shared_queue.put((X, Y, frame_gen_frames, True))
#             else:
#                 mouse.move(X, Y)
#         except Exception as e:
#             print(f"Error: {e}")
#             continue
#         # __________________________________________________________________#
#
#
# # Start the radar thread
# radar_thread = threading.Thread(target=radar_loop, daemon=True)
# radar_thread.start()
#
#
# # Create the main Tkinter window
# root = tk.Tk()
# root.title("Virtual Mouse")
# root.geometry("500x450")
# root.configure(bg=BG_COLOR)
#
# # Set window icon (optional)
# try:
#     root.iconbitmap('TI_Logo.ico')
# except Exception as e:
#     print("Icon not found:", e)
#
# # Style configuration
# style = ttk.Style()
# style.theme_use('clam')
# style.configure('TFrame', background=BG_COLOR)
# style.configure('TButton', background=BUTTON_COLOR, foreground='white',
#                 font=('Helvetica', 10, 'bold'), borderwidth=1)
# style.map('TButton', background=[('active', BUTTON_COLOR), ('pressed', '#3a6a7c')])
#
# # Create only the Settings frame (no Notebook since there's just one tab)
# settings_frame = ttk.Frame(root)
# settings_frame.pack(padx=20, pady=20, fill='both', expand=True)
#
# # Title
# ttk.Label(settings_frame, text="Virtual Mouse Settings",
#           font=('Helvetica', 16, 'bold'), background=BG_COLOR)\
#           .grid(row=0, column=0, pady=10, columnspan=3)
#
# # Tkinter variables for settings
# sensitivity_x_var = tk.IntVar(value=XScale)
# sensitivity_y_var = tk.IntVar(value=YScale)
# smoothing_var = tk.StringVar(value=mouse_smoothing)
# Reverse_X_var = tk.IntVar(value=Reverse_X)
# Reverse_Y_var = tk.IntVar(value=Reverse_Y)
# Switch_XY_var = tk.IntVar(value=Switch_XY)
# frame_gen_on_off_var = tk.IntVar(value=frame_gen_on_off)
# frame_gen_frames_var = tk.IntVar(value=frame_gen_frames)
#
# # Sensitivity X
# ttk.Label(settings_frame, text="Horizontal Sensitivity:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=1, column=0, padx=10, pady=5, sticky='w')
# x_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
#                      textvariable=sensitivity_x_var,
#                      width=10, font=('Helvetica', 11))
# x_spin.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
#
# # Sensitivity Y
# ttk.Label(settings_frame, text="Vertical Sensitivity:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=2, column=0, padx=10, pady=5, sticky='w')
# y_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
#                      textvariable=sensitivity_y_var,
#                      width=10, font=('Helvetica', 11))
# y_spin.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
#
# # Tracking Algorithm selection
# ttk.Label(settings_frame, text="Tracking Algorithm:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=3, column=0, padx=10, pady=5, sticky='w')
# smoothing_options = ["Position", "Velocity"]
# smoothing_drop = ttk.Combobox(settings_frame, values=smoothing_options,
#                               textvariable=smoothing_var, state="readonly",
#                               font=('Helvetica', 11), width=18)
# smoothing_drop.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
#
# # Reverse X
# ttk.Label(settings_frame, text="Reverse X:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=4, column=0, padx=10, pady=5, sticky='w')
# Reverse_X_check = ttk.Checkbutton(settings_frame,
#                                   variable=Reverse_X_var,
#                                   onvalue=-1, offvalue=1)
# Reverse_X_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')
#
# # Reverse Y
# ttk.Label(settings_frame, text="Reverse Y:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=5, column=0, padx=10, pady=5, sticky='w')
# Reverse_Y_check = ttk.Checkbutton(settings_frame,
#                                   variable=Reverse_Y_var,
#                                   onvalue=-1, offvalue=1)
# Reverse_Y_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')
#
# # Switch X and Y
# ttk.Label(settings_frame, text="Switch X and Y:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=6, column=0, padx=10, pady=5, sticky='w')
# Switch_XY_check = ttk.Checkbutton(settings_frame,
#                                   variable=Switch_XY_var,
#                                   onvalue=1, offvalue=0)
# Switch_XY_check.grid(row=6, column=1, padx=10, pady=5, sticky='w')
#
# # Generated Frames ON/OFF
# ttk.Label(settings_frame, text="Generated Frames:",
#           font=('Helvetica', 11), background=BG_COLOR)\
#           .grid(row=7, column=0, padx=10, pady=5, sticky='w')
# frame_gen_on_off_check = ttk.Checkbutton(settings_frame,
#                                             variable=frame_gen_on_off_var,
#                                             onvalue=1, offvalue=0)
# frame_gen_on_off_check.grid(row=7, column=1, padx=10, pady=5, sticky='w')
#
# # --- CHANGED: Create and assign the label for the slider so we can show/hide it ---
# generated_frames_label = ttk.Label(settings_frame, text="Number of Generated Frames:",
#                                    font=('Helvetica', 11), background=BG_COLOR)
# # Create the slider and its associated value label
# generated_frames_scale = tk.Scale(settings_frame, from_=1, to=20,
#                                   variable=frame_gen_frames_var,
#                                   orient='horizontal', length=200, resolution=1,
#                                   showvalue=0, bg=BG_COLOR,
#                                   activebackground=BUTTON_COLOR,
#                                   troughcolor='#d9d9d9')
# generated_frames_value_label = ttk.Label(settings_frame,
#                                          textvariable=frame_gen_frames_var,
#                                          font=('Helvetica', 11),
#                                          background=BG_COLOR)
#
# # --- CHANGED: Update function to show/hide the slider components ---
# def update_generated_frames_state(*args):
#     if frame_gen_on_off_var.get() == 1:
#         generated_frames_label.grid(row=8, column=0, padx=10, pady=5, sticky='w')
#         generated_frames_scale.grid(row=8, column=1, padx=10, pady=5, sticky='ew')
#         generated_frames_value_label.grid(row=8, column=2, padx=10, pady=5, sticky='w')
#     else:
#         generated_frames_label.grid_remove()
#         generated_frames_scale.grid_remove()
#         generated_frames_value_label.grid_remove()
#
# frame_gen_on_off_var.trace('w', update_generated_frames_state)
# update_generated_frames_state()  # Set initial state based on checkbox (default is hidden)
#
# # Separator
# ttk.Separator(settings_frame, orient='horizontal')\
#     .grid(row=9, column=0, columnspan=3, pady=20, sticky='ew')
#
# # Apply button
# apply_btn = ttk.Button(settings_frame, text="Apply Configuration",
#                        command=apply_settings, style='TButton')
# apply_btn.grid(row=10, column=0, columnspan=3, pady=10, ipadx=20, ipady=5)
#
# # Configure grid columns for proper spacing
# settings_frame.columnconfigure(0, weight=1)
# settings_frame.columnconfigure(1, weight=1)
# settings_frame.columnconfigure(2, weight=0)
#
# root.mainloop()
#
# #----------------------------------------------------------------------------

# import queue
# import time
# from pynput.mouse import Button, Controller
#
# #IMPORTANT################################################################
# #                                                                        #
# # Make sure to tun "shared_queue.put((0, 0, 0, False))" before joing     #
# # thread or the thread will not die and will break the python terminal!! #
# #                                                                        #
# ##########################################################################
#
# def run_frame_gen(shared_queue, refresh_rate, frames):#generates frames inbetween data points
#     mouse = Controller()#start mouse thing
#     not_kill = True #to keep loop running
#     while not_kill:#loop until told to end
#         try:
#             X, Y, not_kill= shared_queue.get(timeout=1/refresh_rate) #get data from queue
#
#             for  i in range(0, frames, 1):#generate frames inbetween
#                 mouse.move(X/frames, Y/frames) #move mouse
#                 time.sleep(1/refresh_rate/frames) #wait till next time to move
#         except queue.Empty:#if nothing in queue continue
#             pass
from gui_parser import *
# Imports___________________________________________________________#
from pathlib import Path
from pynput.mouse import Controller, Button  # Allows us to control mouse
from radar_filter import *
from oob_gesture_model import gesture_recognition_model
import tkinter as tk
from tkinter import ttk
import threading
from Frame_gen import run_frame_gen
import queue
import random
import time  # Allows us to add delays
import serial.tools.list_ports

cwd = Path.cwd()
model_path = cwd.joinpath("resources", "New_Gesture_CNN3.keras")
scaler_path = cwd.joinpath("resources", "new_gesture_scaler3.bin")
cfg_path = cwd.joinpath("resources", "radar.cfg")

ports = serial.tools.list_ports.comports()
data_port = ''
com_port = ''
for port, desc, hwid in sorted(ports):
    # print("{}: {} [{}]".format(port, desc, hwid)) #Displays all ports
    if "UART Bridge: Standard" in desc:  # Data port
        data_port = port
    if "UART Bridge: Enhanced" in desc:  # COM port
        com_port = port
        #
# Settings__________________________________________________________# These variables let us change different factors
XScale = 1100  # scales the X and Y movements by the value (must be int)
YScale = 1150
mouse_smoothing = "Velocity"
frame_gen_on_off = 0  # Unchecked = 0 (off), Checked = 1 (on)
frame_gen_frames = 1  # Default value, range 1 to 20
Switch_XY = 0  # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1  # reverses X (1 = off, -1 = on)
Reverse_Y = 1  # reverses Y (1 = off, -1 = on)
Refresh_Rate = 30  # refreshrate of the board/data
# Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo

# -----------------------------------------------------------------------------

# Velocity Tracking variables
x_vec = 1  # these variable are temporary
y_vec = 1  #
data_points = []  # stores num_points for frames //Only 2 are need for velocity calculations
point_clouds = []  # stores point clouds for frames
mouse = Controller()  # Start mouse controller
xvels = []  # stores x-velocities calculated from 2 frames
yvels = []  # stores y-velocities calculated from 2 frames
num_vels = 0  # tracks num of velocities

prev_x = 0
prev_y = 0

# -------------------------------------------------------------------------------
# Position Tracking Variables
x_array = []
z_array = []
prev_posX = 0
prev_posY = 0

# -------------------------------------------------------------------------------

# Custom color scheme
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_BG = "#2e2e2e"
TEXT_FG = "#00ff00"


def gesture_action(cur_gest, prev_gest, gesture_map):
    if (cur_gest == 0):
        return prev_gest
    else:
        if (cur_gest != prev_gest):
            map_action(False, gesture_map[cur_gest])
            return cur_gest
        else:
            map_action(True, gesture_map[cur_gest])
            return 0


def map_action(repeat_bol, mouse_action):
    if (mouse_action == "LEFT_HOLD_RELEASE"):
        if (repeat_bol):
            mouse.release(Button.left)
        else:
            mouse.press(Button.left)
    if (mouse_action == "RIGHT_CLICK"):
        mouse.click(Button.right)
    if (mouse_action == "DOUBLE_LEFT"):
        mouse.click(Button.left, 2)


def get_pos(num_points_1, num_points_2, list1, list2):
    # the output data from chirp configuration demo in the first frame
    # num_points = 4 # The chirp configuration demo will output the number of points detected
    # points = np.array([[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]) # The chirp configuration demo will output the coordinates of the points

    # the output data from chirp configuration demo in the second frame
    # num_points_2 = 5 # The chirp configuration demo will output the number of points detected
    # points_2 = np.array([[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]) # The chirp configuration demo will output the coordinates of the points
    x = 0  # variable for x coordinates in the first frame
    y = 0  # variable for y coordinates in the first frame
    x_2 = 0  # variable for x coordinates in the second frame
    y_2 = 0  # variable for y coordinates in the second frame
    average_x = 0
    average_x_2 = 0
    average_y = 0
    average_y_2 = 0
    # average position of the first frame
    for i in range(num_points_1):  # loop for average position of the first frame

        x += list1[i][0]  # calculate the sum of the magnitude of x coordinates
        y += list1[i][2]  # calculate the sum of the magnitude of y coordinates
        average_x = x / num_points_1  # calculate the average coordinate of x axis
        average_y = y / num_points_1  # calculate the average coordinate of y axis

    # average position of the second frame
    for i in range(num_points_2):  # loop for average position of the second frame

        x_2 += list2[i][0]  # calculate the sum of the magnitude of x coordinates
        y_2 += list2[i][2]  # calculate the sum of the magnitude of y coordinates
        average_x_2 = x_2 / num_points_2  # calculate the average coordinate of x axis
        average_y_2 = y_2 / num_points_2  # calculate the average coordinate of y axis

    # use average positions to output moving path
    output_v_x = (average_x_2 - average_x)  # calculate the velocity in x direction
    output_v_y = (average_y_2 - average_y)  # calculate the velocity in y direction

    # velocity in z-direction is not required because the user is required to move his hand in parallel to the radar's x-y plane
    # print("V_x euqals to ", output_v_x)  # velocity check
    # print("V_y euqals to ", output_v_y)  # velocity check
    return output_v_x, output_v_y


def track_vel(numPoints, pointCloud):
    global num_vels, prev_x, prev_y
    if numPoints == 0:
        xvels.append(0)
        yvels.append(0)
        return True, 0, 0

    pointCloudArray = []  # Blank Array to store pointCloud info
    for i in range(numPoints):  # Iterates through total number of points detected
        pointCloudArray.append(pointCloud[i][0:3])  # Pulling X, Y, Z values per point detected

    newPointCloud = filter_ys(pointCloudArray)
    point_clouds.append(newPointCloud)
    data_points.append(len(newPointCloud))

    if (len(data_points) > 1):
        x_vec, y_vec = get_pos(data_points[0], data_points[1], point_clouds[0], point_clouds[1])
        point_clouds.pop(0)
        data_points.pop(0)

        if abs(x_vec) < .05: x_vec = 0
        if abs(y_vec) < .05: y_vec = 0
        if abs(x_vec) > .3: x_vec = 0
        if abs(y_vec) > .3: y_vec = 0
        xvels.append(x_vec)
        yvels.append(y_vec)

    # if abs(x_vec) > .25 or abs(y_vec) > .25: continue
    if (len(xvels) == 0): return (True, 0, 0)
    while (len(xvels) > 5):
        xvels.pop(0)
        yvels.pop(0)

    avg_x = simple_avg(xvels)
    avg_y = simple_avg(yvels)
    if abs(avg_y) < .03: avg_y = 0
    mov_x = (avg_x + prev_x) / 2
    mov_y = (avg_y + prev_y) / 2

    prev_x = avg_x
    prev_y = avg_y

    if Switch_XY == 0:  # If we are switching X and Y
        X = XScale * Reverse_X * mov_x  #
        Y = YScale * Reverse_Y * mov_y  #
    elif Switch_XY == 1:
        X = XScale * Reverse_X * mov_y  #
        Y = YScale * Reverse_Y * mov_x  #
    else:
        print("ERROR: Switch-XY must be a 0 or a 1.")  #

    return False, X, Y


def track_pos(pointCloud):
    global prev_posX, prev_posY

    x_pos = 0
    z_pos = 0
    if (len(pointCloud) == 0): return True, 0, 0
    newPointCloud = filter_ys(pointCloud)
    pointer_numPoints = len(newPointCloud)
    if pointer_numPoints == 0:
        return True, 0, 0
    for point in newPointCloud:
        x_pos += point[0]
        z_pos += point[2]

    x_pos /= pointer_numPoints
    z_pos /= pointer_numPoints

    x_array.append(x_pos)
    z_array.append(z_pos)

    while (len(x_array) > 10):
        x_array.pop(0)
        z_array.pop(0)

    avg_x = simple_avg(x_array)
    avg_z = simple_avg(z_array)

    X = 2560 * (avg_x + .2) / .4
    Y = 1600 * (avg_z + .2) / .4
    delta_x = X - prev_posX
    delta_y = Y - prev_posY

    prev_posX = X
    prev_posY = Y

    return False, delta_x, delta_y


def apply_settings():
    """Retrieve values from the settings inputs and update globals."""
    global XScale, YScale, mouse_smoothing
    global Reverse_X, Reverse_Y, Switch_XY, frame_gen_on_off, frame_gen_frames
    XScale = sensitivity_x_var.get()
    YScale = sensitivity_y_var.get()
    mouse_smoothing = smoothing_var.get()
    hold_release_left_click = hold_release_left_click_var.get()
    double_left_click = double_left_click_var.get()
    right_click = right_click_var.get()
    Reverse_X = Reverse_X_var.get()
    Reverse_Y = Reverse_Y_var.get()
    Switch_XY = Switch_XY_var.get()
    frame_gen_on_off = frame_gen_on_off_var.get()
    frame_gen_frames = frame_gen_frames_var.get()

    print("\n\n\n\n")
    if hold_release_left_click == 'Push':
        print("Changed hold/rel to Push")
        gesture_dict[1] = 'LEFT_HOLD_RELEASE'
    elif hold_release_left_click == 'Pull':
        print("Changed hold/rel to Pull")
        gesture_dict[3] = 'LEFT_HOLD_RELEASE'
    elif hold_release_left_click == "Shine":
        print("Changed hold/rel to Shine")
        gesture_dict[2] = 'LEFT_HOLD_RELEASE'
    else:
        print("Changed hold/rel to None")
        gesture_dict[1] = 'NONE'

    if double_left_click == 'Push':
        print("Changed double left to Push")
        gesture_dict[1] = 'DOUBLE_LEFT'
    elif double_left_click == 'Pull':
        print("Changed double left to Pull")
        gesture_dict[3] = 'DOUBLE_LEFT'
    elif double_left_click == "Shine":
        print("Changed double left to Shine")
        gesture_dict[2] = 'DOUBLE_LEFT'
    else:
        print("Changed double left to None")
        gesture_dict[3] = 'NONE'

    if right_click == 'Push':
        print("Changed right click to Push")
        gesture_dict[1] = 'RIGHT_CLICK'
    elif right_click == 'Pull':
        print("Changed right click to Pull")
        gesture_dict[3] = 'RIGHT_CLICK'
    elif right_click == 'Shine':
        print("Changed right click to Shine")
        gesture_dict[2] = 'RIGHT_CLICK'
    else:
        print("Changed right click to None")
        gesture_dict[2] = 'NONE'

    print("Updated Settings:")
    print("Sensitivity X:", XScale)
    print("Sensitivity Y:", YScale)
    print("Mouse Smoothing:", mouse_smoothing)
    print("Hold/Release Left Click:", hold_release_left_click)
    print("Double Left Click:", double_left_click)
    print("Right Click:", right_click)
    print("Reverse X:", Reverse_X)
    print("Reverse Y:", Reverse_Y)
    print("Switch X and Y:", Switch_XY)
    print("Generated Frames ON/OFF:", frame_gen_on_off)
    print("Number of Generated Frames:", frame_gen_frames)

    print(gesture_dict)

# Pointer Positioning
cfg = open(cfg_path, "r")  # Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort")  # Defining Pointer Parser from class UARTParser
my_parser.connectComPorts(com_port, data_port)  # Device-Manager defined Ports
my_parser.sendCfg(cfg)  # Send Config File
cfg.close()  # Close File

model = gesture_recognition_model(model_path, scaler_path)

gesture_names = ["NO_GESTURE", "PUSH", "SHINE", "PULL", "SHAKE"]
gesture_dict = {0: "NONE",
                1: "LEFT_HOLD_RELEASE",
                2: "RIGHT_CLICK",
                3: "DOUBLE_LEFT",
                4: "SCROLL"}

# gesture_dict[1] = 'DOUBLE_LEFT'

frames = 0
while (frames < model.frames):
    radarData = my_parser.readAndParseUartDoubleCOMPort()  # Parsing Pointer radar data
    # gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data
    frameNum = radarData["frameNum"]
    numPoints = radarData["numDetectedPoints"]
    pointCloud = radarData["pointCloud"]

    model.fill_frame(numPoints, pointCloud)
    frames += 1

frames = 0
DT_counter = 0
gesture_active = 0
prev_gest = 0


def radar_loop():
    global frames
    global frame_gen_on_off
    global DT_counter
    global gesture_active
    global prev_gest
    global frame_gen_frames
    shared_queue = queue.Queue()
    thread = threading.Thread(target=run_frame_gen, args=(shared_queue, Refresh_Rate, frame_gen_frames))

    thread.start()
    while (1):  # Radars connected and running, always true until not - Implement GUI?
        try:
            radarData = my_parser.readAndParseUartDoubleCOMPort()  # Parsing Pointer radar data

            frameNum = radarData["frameNum"]
            numPoints = radarData["numDetectedPoints"]
            pointCloud = radarData["pointCloud"]

            model.add_frame(numPoints, pointCloud)
            frames += 1
            if gesture_active == False:  # If a gesture isn't active skip frame
                if frames % 5 == 0:
                    cur_gest = model.get_prediction()  # Check for Gesture
                    # print(cur_gest)
                    if (cur_gest != 0):  # If gesture detected start cooldown
                        gesture_active = True
                        prev_gest = gesture_action(cur_gest, prev_gest, gesture_dict)
            else:  # Cooldown
                if (DT_counter < 20):
                    DT_counter += 1
                else:
                    DT_counter = 0
                    gesture_active = False

            if (mouse_smoothing == "Velocity"):
                skip_bol, X, Y = track_vel(len(pointCloud), pointCloud)
            else:
                skip_bol, X, Y = track_pos(pointCloud)
            if (skip_bol): continue

            if (frame_gen_on_off):
                shared_queue.put((X, Y, frame_gen_frames, True))
            else:
                mouse.move(X, Y)
        except Exception as e:
            print(f"Error: {e}")
            continue
        # __________________________________________________________________#


# Start the radar thread
radar_thread = threading.Thread(target=radar_loop, daemon=True)
radar_thread.start()

# Create the main Tkinter window
root = tk.Tk()
root.title("Virtual Mouse")
root.geometry("500x550")
root.configure(bg=BG_COLOR)

# Set window icon (optional)
try:
    root.iconbitmap('TI_Logo.ico')
except Exception as e:
    print("Icon not found:", e)

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=BG_COLOR)
style.configure('TButton', background=BUTTON_COLOR, foreground='white',
                font=('Helvetica', 10, 'bold'), borderwidth=1)
style.map('TButton', background=[('active', BUTTON_COLOR), ('pressed', '#3a6a7c')])

# Create only the Settings frame (no Notebook since there's just one tab)
settings_frame = ttk.Frame(root)
settings_frame.pack(padx=20, pady=20, fill='both', expand=True)

# Title
ttk.Label(settings_frame, text="Virtual Mouse Settings",
          font=('Helvetica', 16, 'bold'), background=BG_COLOR) \
    .grid(row=0, column=0, pady=10, columnspan=3)

# Tkinter variables for settings
sensitivity_x_var = tk.IntVar(value=XScale)
sensitivity_y_var = tk.IntVar(value=YScale)
smoothing_var = tk.StringVar(value=mouse_smoothing)
hold_release_left_click_var = tk.StringVar(value="Push")
double_left_click_var = tk.StringVar(value="Shine")
right_click_var = tk.StringVar(value="Pull")
Reverse_X_var = tk.IntVar(value=Reverse_X)
Reverse_Y_var = tk.IntVar(value=Reverse_Y)
Switch_XY_var = tk.IntVar(value=Switch_XY)
frame_gen_on_off_var = tk.IntVar(value=frame_gen_on_off)
frame_gen_frames_var = tk.IntVar(value=frame_gen_frames)

# Sensitivity X
ttk.Label(settings_frame, text="Horizontal Sensitivity:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=1, column=0, padx=10, pady=5, sticky='w')
x_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
                     textvariable=sensitivity_x_var,
                     width=10, font=('Helvetica', 11))
x_spin.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

# Sensitivity Y
ttk.Label(settings_frame, text="Vertical Sensitivity:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=2, column=0, padx=10, pady=5, sticky='w')
y_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
                     textvariable=sensitivity_y_var,
                     width=10, font=('Helvetica', 11))
y_spin.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

# Tracking Algorithm selection
ttk.Label(settings_frame, text="Tracking Algorithm:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=3, column=0, padx=10, pady=5, sticky='w')
smoothing_options = ["Position", "Velocity"]
smoothing_drop = ttk.Combobox(settings_frame, values=smoothing_options,
                              textvariable=smoothing_var, state="readonly",
                              font=('Helvetica', 11), width=18)
smoothing_drop.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

# NEW: Hold/Release Left Click setting
ttk.Label(settings_frame, text="Hold/Release Left Click:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=4, column=0, padx=10, pady=5, sticky='w')
hold_release_left_click_options = ["Push", "Pull", "Shine", "None"]
hold_release_left_click_drop = ttk.Combobox(settings_frame,
                                            values=hold_release_left_click_options,
                                            textvariable=hold_release_left_click_var,
                                            state="readonly",
                                            font=('Helvetica', 11), width=18)
hold_release_left_click_drop.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

# NEW: Double Left Click setting
ttk.Label(settings_frame, text="Double Left Click:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=5, column=0, padx=10, pady=5, sticky='w')
double_left_click_options = ["Push", "Pull", "Shine", "None"]
double_left_click_drop = ttk.Combobox(settings_frame,
                                      values=double_left_click_options,
                                      textvariable=double_left_click_var,
                                      state="readonly",
                                      font=('Helvetica', 11), width=18)
double_left_click_drop.grid(row=5, column=1, padx=10, pady=5, sticky='ew')

# NEW: Right Click setting
ttk.Label(settings_frame, text="Right Click:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=6, column=0, padx=10, pady=5, sticky='w')
right_click_options = ["Push", "Pull", "Shine", "None"]
right_click_drop = ttk.Combobox(settings_frame,
                                values=right_click_options,
                                textvariable=right_click_var,
                                state="readonly",
                                font=('Helvetica', 11), width=18)
right_click_drop.grid(row=6, column=1, padx=10, pady=5, sticky='ew')

# Reverse X
ttk.Label(settings_frame, text="Reverse X:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=7, column=0, padx=10, pady=5, sticky='w')
Reverse_X_check = ttk.Checkbutton(settings_frame,
                                  variable=Reverse_X_var,
                                  onvalue=-1, offvalue=1)
Reverse_X_check.grid(row=7, column=1, padx=10, pady=5, sticky='w')

# Reverse Y
ttk.Label(settings_frame, text="Reverse Y:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=8, column=0, padx=10, pady=5, sticky='w')
Reverse_Y_check = ttk.Checkbutton(settings_frame,
                                  variable=Reverse_Y_var,
                                  onvalue=-1, offvalue=1)
Reverse_Y_check.grid(row=8, column=1, padx=10, pady=5, sticky='w')

# Switch X and Y
ttk.Label(settings_frame, text="Switch X and Y:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=9, column=0, padx=10, pady=5, sticky='w')
Switch_XY_check = ttk.Checkbutton(settings_frame,
                                  variable=Switch_XY_var,
                                  onvalue=1, offvalue=0)
Switch_XY_check.grid(row=9, column=1, padx=10, pady=5, sticky='w')

# Generated Frames ON/OFF
ttk.Label(settings_frame, text="Generated Frames:",
          font=('Helvetica', 11), background=BG_COLOR) \
    .grid(row=10, column=0, padx=10, pady=5, sticky='w')
frame_gen_on_off_check = ttk.Checkbutton(settings_frame,
                                         variable=frame_gen_on_off_var,
                                         onvalue=1, offvalue=0)
frame_gen_on_off_check.grid(row=10, column=1, padx=10, pady=5, sticky='w')

# --- CHANGED: Create and assign the label for the slider so we can show/hide it ---
generated_frames_label = ttk.Label(settings_frame, text="Number of Generated Frames:",
                                   font=('Helvetica', 11), background=BG_COLOR)
# Create the slider and its associated value label
generated_frames_scale = tk.Scale(settings_frame, from_=1, to=20,
                                  variable=frame_gen_frames_var,
                                  orient='horizontal', length=200, resolution=1,
                                  showvalue=0, bg=BG_COLOR,
                                  activebackground=BUTTON_COLOR,
                                  troughcolor='#d9d9d9')
generated_frames_value_label = ttk.Label(settings_frame,
                                         textvariable=frame_gen_frames_var,
                                         font=('Helvetica', 11),
                                         background=BG_COLOR)


# --- CHANGED: Update function to show/hide the slider components ---
def update_generated_frames_state(*args):
    if frame_gen_on_off_var.get() == 1:
        generated_frames_label.grid(row=11, column=0, padx=10, pady=5, sticky='w')
        generated_frames_scale.grid(row=11, column=1, padx=10, pady=5, sticky='ew')
        generated_frames_value_label.grid(row=11, column=2, padx=10, pady=5, sticky='w')
    else:
        generated_frames_label.grid_remove()
        generated_frames_scale.grid_remove()
        generated_frames_value_label.grid_remove()


frame_gen_on_off_var.trace('w', update_generated_frames_state)
update_generated_frames_state()  # Set initial state based on checkbox (default is hidden)

# Separator
ttk.Separator(settings_frame, orient='horizontal') \
    .grid(row=12, column=0, columnspan=3, pady=20, sticky='ew')

# Apply button
apply_btn = ttk.Button(settings_frame, text="Apply Configuration",
                       command=apply_settings, style='TButton')
apply_btn.grid(row=13, column=0, columnspan=3, pady=10, ipadx=20, ipady=5)

# Configure grid columns for proper spacing
settings_frame.columnconfigure(0, weight=1)
settings_frame.columnconfigure(1, weight=1)
settings_frame.columnconfigure(2, weight=0)

root.mainloop()

# ----------------------------------------------------------------------------

