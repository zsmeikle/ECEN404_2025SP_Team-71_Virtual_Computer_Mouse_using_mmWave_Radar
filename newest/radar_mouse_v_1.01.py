from gui_parser import *
#Imports___________________________________________________________#
from pynput.mouse import Controller, Button                        # Allows us to control mouse
from radar_filter import *
from oob_gesture_model import gesture_recognition_model
import tkinter as tk
from tkinter import ttk
import threading
from Frame_gen import run_frame_gen
import queue
import random
import time                                                        # Allows us to add delays
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
data_port = ''
com_port = ''
for port, desc, hwid in sorted(ports):
        # print("{}: {} [{}]".format(port, desc, hwid)) #Displays all ports
        if "UART Bridge: Standard" in desc: #Data port
            data_port = port
        if "UART Bridge: Enhanced" in desc: #COM port
            com_port = port
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
XScale = 1100                                                      # scales the X and Y movements by the value (must be int)
YScale = 1150
mouse_smoothing = "Algorithm 1"
frame_gen_on_off = 0  # Unchecked = 0 (off), Checked = 1 (on)
frame_gen_frames = 1     # Default value, range 1 to 20
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 24                                                  # refreshrate of the board/data
# Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo

#-----------------------------------------------------------------------------

# Custom color scheme
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_BG = "#2e2e2e"
TEXT_FG = "#00ff00"

def apply_settings():
    """Retrieve values from the settings inputs and update globals."""
    global XScale, YScale, mouse_smoothing
    global Reverse_X, Reverse_Y, Switch_XY, frame_gen_on_off, frame_gen_frames
    XScale = sensitivity_x_var.get()
    YScale = sensitivity_y_var.get()
    mouse_smoothing = smoothing_var.get()
    Reverse_X = Reverse_X_var.get()
    Reverse_Y = Reverse_Y_var.get()
    Switch_XY = Switch_XY_var.get()
    frame_gen_on_off = frame_gen_on_off_var.get()
    frame_gen_frames = frame_gen_frames_var.get()
    print("Updated Settings:")
    print("Sensitivity X:", XScale)
    print("Sensitivity Y:", YScale)
    print("Mouse Smoothing:", mouse_smoothing)
    print("Reverse X:", Reverse_X)
    print("Reverse Y:", Reverse_Y)
    print("Switch X and Y:", Switch_XY)
    print("Generated Frames ON/OFF:", frame_gen_on_off)
    print("Number of Generated Frames:", frame_gen_frames)

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
    print("V_x euqals to ", output_v_x)  # velocity check
    print("V_y euqals to ", output_v_y)  # velocity check
    return output_v_x, output_v_y
#Pointer Positioning
cfg = open("C:/Users/snowb/Desktop/Capstone/newest/xwr68xx_AOP_profile_2025_02_17T14_57_20_747.cfg", "r") #Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts(com_port, data_port) #Device-Manager defined Ports
my_parser.sendCfg(cfg) #Send Config File
cfg.close() #Close File

#ML Gesture
# my_parser2 = UARTParser("DoubleCOMPort") #Defining Gesture Parser from class UARTParser
# my_parser2.connectComPorts("COM9", "COM10") #Device-Manager defined Ports
x_vec = 1                                                          # these variable are temporary
y_vec = 1                                                          #
data_points = []                                                   # stores num_points for frames //Only 2 are need for velocity calculations
point_clouds = []                                                  # stores point clouds for frames
mouse = Controller()                                               # Start mouse controller
xvels = []                                                         # stores x-velocities calculated from 2 frames
yvels = []                                                         # stores y-velocities calculated from 2 frames
num_vels = 0                                                       # tracks num of velocities

prev_x = 0
prev_y = 0
avg_x = 0                                                          # Average x_velocity
avg_y = 0                                                          # Average y_velocity
model = gesture_recognition_model()

data_queue = []
gesture_names = ["NO_GESTURE", "PUSH", "SHINE", "TURN_LEFT", "TURN_RIGHT"]
frames = 0
while(frames < 20):
    radarData = my_parser.readAndParseUartDoubleCOMPort() #Parsing Pointer radar data
    # gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data

    frameNum = radarData["frameNum"]
    numPoints = radarData["numDetectedPoints"]
    pointCloud = radarData["pointCloud"]

    if numPoints == 0:
        features = [0, 0, 0, 0, 0]
    else:
        x_pos = simple_avg([point[0] for point in pointCloud])
        y_pos = simple_avg([point[1] for point in pointCloud])
        z_pos = simple_avg([point[2] for point in pointCloud])
        doppler = simple_avg([point[3] for point in pointCloud])
        features = [x_pos, y_pos, z_pos, doppler, numPoints]

    data_queue.append(features)
    frames += 1
frames = 0
DT_counter = 0
gesture_active = 0
prev_gest = 0

def radar_loop():
    global frames
    global data_queue
    global prev_x
    global prev_y
    global frame_gen_on_off
    global DT_counter
    global gesture_active
    global prev_gest
    global frame_gen_frames
    shared_queue = queue.Queue()
    thread = threading.Thread(target=run_frame_gen, args=(shared_queue, Refresh_Rate, frame_gen_frames))

    thread.start()
    tempRight_Click = 0
    tempLeft_Click = 0
    while (1):  # Radars connected and running, always true until not - Implement GUI?
        try:
            gestureID = 0
            data_queue.pop(0)
            radarData = my_parser.readAndParseUartDoubleCOMPort()  # Parsing Pointer radar data
            # gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data

            frameNum = radarData["frameNum"]
            numPoints = radarData["numDetectedPoints"]
            pointCloud = radarData["pointCloud"]

            pointCloudArray = []  # Blank Array to store pointCloud info
            for i in range(numPoints):  # Iterates through total number of points detected
                pointCloudArray.append(pointCloud[i][0:3])  # Pulling X, Y, Z values per point detected
            # print("Pointer Data")
            # print(pointer_numPoints, "|",pointer_frameNum) #Outputting points, frame number per frame
            # for i in pointCloudArray: #Iterating and outputting each point (X, Y, Z)
            #     print(i)

            if numPoints == 0:
                features = [0, 0, 0, 0, 0]
            else:
                x_pos = simple_avg([point[0] for point in pointCloud])
                y_pos = simple_avg([point[1] for point in pointCloud])
                z_pos = simple_avg([point[2] for point in pointCloud])
                doppler = simple_avg([point[3] for point in pointCloud])
                features = [x_pos, y_pos, z_pos, doppler, numPoints]
            data_queue.append(features)
            frames += 1
            if gesture_active == False:  # If a gesture isn't active skip frame
                if frames % 5 == 0:
                    cur_gest = model.get_prediction(data_queue)  # Check for Gesture
                    print(cur_gest)
                    if (cur_gest != 0):  # If gesture detected start cooldown
                        gesture_active = True
                        DT_counter = 0

                        if (prev_gest == cur_gest):
                            if cur_gest == 1:
                                tempLeft_Click = 2
                            if cur_gest == 2:
                                tempRight_Click = 2
                            prev_gest = 0
                        else:
                            if cur_gest == 1:  # #
                                tempLeft_Click = 1
                            if cur_gest == 0:
                                True
                            if cur_gest == 2:
                                tempRight_Click = 1
                            prev_gest = cur_gest
            else:  # Cooldown
                tempRight_Click = 0  # #
                tempLeft_Click = 0
                if (DT_counter < 20):
                    DT_counter += 1
                else:
                    gesture_active = False
            # print()
            # print("Gesture Data")
            # print(trimmed_Gesture, '\n') #Outputting feature data
            if numPoints == 0:
                xvels.append(0)
                yvels.append(0)
                continue
            print(frameNum)
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
            if (len(xvels) == 0): continue
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
                break  #
                #

            if tempLeft_Click == 0:  # if nothing no-op
                True  #
            elif tempLeft_Click == 1:  #
                mouse.press(Button.left)  #
                print('Left_press')
            elif tempLeft_Click == 2:  #
                mouse.release(Button.left)  #
                print('left_release')
            else:  # Error invaild input
                print("ERROR: invalid left click input: " + str(tempLeft_Click))
                break  # # If right click
            if tempRight_Click == 0:  # if nothing no-op
                True  #
            elif tempRight_Click == 1:  #
                mouse.press(Button.right)  #
                print('right_press')
            elif tempRight_Click == 2:  #
                mouse.release(Button.right)  #
                print('right_release')
            else:  # Error invaild input
                print("ERROR: invalid right click input: " + str(tempRight_Click))
                break

            if (frame_gen_on_off):
                shared_queue.put((X, Y, frame_gen_frames, True))
            else:
                mouse.move(X, Y)
            # New_Delay = Delay - (time.time() - t0)  # Calculate delay with processing time
            # if (New_Delay < 0):  # Skip a frame if took to long to compute
            #     time.sleep(New_Delay + Delay)  #
            #     print("Skipped Frame: " + str(Frame_Num))  # Print if a frame was skipped
            # else:  #
            #     time.sleep(New_Delay)  # Delay as per refresh rate and time code took
        # __________________________________________________________________#
        except Exception as e:
            print(f"Error: {e}")
            continue


# Start the radar thread
radar_thread = threading.Thread(target=radar_loop, daemon=True)
radar_thread.start()


# Create the main Tkinter window
root = tk.Tk()
root.title("Virtual Mouse")
root.geometry("500x450")
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
          font=('Helvetica', 16, 'bold'), background=BG_COLOR)\
          .grid(row=0, column=0, pady=10, columnspan=3)

# Tkinter variables for settings
sensitivity_x_var = tk.IntVar(value=XScale)
sensitivity_y_var = tk.IntVar(value=YScale)
smoothing_var = tk.StringVar(value=mouse_smoothing)
Reverse_X_var = tk.IntVar(value=Reverse_X)
Reverse_Y_var = tk.IntVar(value=Reverse_Y)
Switch_XY_var = tk.IntVar(value=Switch_XY)
frame_gen_on_off_var = tk.IntVar(value=frame_gen_on_off)
frame_gen_frames_var = tk.IntVar(value=frame_gen_frames)

# Sensitivity X
ttk.Label(settings_frame, text="Horizontal Sensitivity:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=1, column=0, padx=10, pady=5, sticky='w')
x_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
                     textvariable=sensitivity_x_var,
                     width=10, font=('Helvetica', 11))
x_spin.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

# Sensitivity Y
ttk.Label(settings_frame, text="Vertical Sensitivity:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=2, column=0, padx=10, pady=5, sticky='w')
y_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
                     textvariable=sensitivity_y_var,
                     width=10, font=('Helvetica', 11))
y_spin.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

# Smoothing Algorithm selection
ttk.Label(settings_frame, text="Smoothing Algorithm:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=3, column=0, padx=10, pady=5, sticky='w')
smoothing_options = ["None", "Algorithm 1", "Algorithm 2", "Advanced Filter"]
smoothing_drop = ttk.Combobox(settings_frame, values=smoothing_options,
                              textvariable=smoothing_var, state="readonly",
                              font=('Helvetica', 11), width=18)
smoothing_drop.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

# Reverse X
ttk.Label(settings_frame, text="Reverse X:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=4, column=0, padx=10, pady=5, sticky='w')
Reverse_X_check = ttk.Checkbutton(settings_frame,
                                  variable=Reverse_X_var,
                                  onvalue=-1, offvalue=1)
Reverse_X_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')

# Reverse Y
ttk.Label(settings_frame, text="Reverse Y:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=5, column=0, padx=10, pady=5, sticky='w')
Reverse_Y_check = ttk.Checkbutton(settings_frame,
                                  variable=Reverse_Y_var,
                                  onvalue=-1, offvalue=1)
Reverse_Y_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')

# Switch X and Y
ttk.Label(settings_frame, text="Switch X and Y:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=6, column=0, padx=10, pady=5, sticky='w')
Switch_XY_check = ttk.Checkbutton(settings_frame,
                                  variable=Switch_XY_var,
                                  onvalue=1, offvalue=0)
Switch_XY_check.grid(row=6, column=1, padx=10, pady=5, sticky='w')

# Generated Frames ON/OFF
ttk.Label(settings_frame, text="Generated Frames:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=7, column=0, padx=10, pady=5, sticky='w')
frame_gen_on_off_check = ttk.Checkbutton(settings_frame,
                                            variable=frame_gen_on_off_var,
                                            onvalue=1, offvalue=0)
frame_gen_on_off_check.grid(row=7, column=1, padx=10, pady=5, sticky='w')

ttk.Label(settings_frame, text="Number of Generated Frames:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=8, column=0, padx=10, pady=5, sticky='w')
frame_gen_frames_scale = tk.Scale(settings_frame, from_=1, to=20,
                                  variable=frame_gen_frames_var,
                                  orient='horizontal', length=200, resolution=1,
                                  showvalue=0, bg=BG_COLOR,
                                  activebackground=BUTTON_COLOR,
                                  troughcolor='#d9d9d9')
frame_gen_frames_scale.grid(row=8, column=1, padx=10, pady=5, sticky='ew')
frame_gen_frames_value_label = ttk.Label(settings_frame,
                                         textvariable=frame_gen_frames_var,
                                         font=('Helvetica', 11),
                                         background=BG_COLOR)
frame_gen_frames_value_label.grid(row=8, column=2, padx=10, pady=5, sticky='w')

# Enable/disable the slider based on the checkbox state
def update_frame_gen_frames_state(*args):
    if frame_gen_on_off_var.get() == 1:
        frame_gen_frames_scale.configure(state='normal')
    else:
        frame_gen_frames_scale.configure(state='disabled')

frame_gen_on_off_var.trace('w', update_frame_gen_frames_state)
update_frame_gen_frames_state()

# Separator
ttk.Separator(settings_frame, orient='horizontal')\
    .grid(row=9, column=0, columnspan=3, pady=20, sticky='ew')

# Apply button
apply_btn = ttk.Button(settings_frame, text="Apply Configuration",
                       command=apply_settings, style='TButton')
apply_btn.grid(row=10, column=0, columnspan=3, pady=10, ipadx=20, ipady=5)

# Configure grid columns for proper spacing
settings_frame.columnconfigure(0, weight=1)
settings_frame.columnconfigure(1, weight=1)
settings_frame.columnconfigure(2, weight=0)

root.mainloop()

#----------------------------------------------------------------------------











# from gui_parser import *
#
# #-----------------------------------------------------------------------------
# #Pointer Positioning
# my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
# my_parser.connectComPorts("COM7", "COM8") #Device-Manager defined Ports
#
# #ML Gesture
# #my_parser2 = UARTParser("DoubleCOMPort") #Defining Gesture Parser from class UARTParser
# #my_parser2.connectComPorts("COM5", "COM6") #Device-Manager defined Ports
#
# while(1): #Radars connected and running, always true until not - Implement GUI?
#     try:
#         pointer_Data = my_parser.readAndParseUartDoubleCOMPort() #Parsing Pointer radar data
#         gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data
#
#         keys_Pointer = ['frameNum', 'pointCloud', 'numDetectedPoints'] #Only required fields needed for Pointer Position
#         trimmed_Pointer = {key: pointer_Data[key] for key in keys_Pointer} #Trimming pointer_Data for keys_Pointer
#         key_Gesture = ['features'] #Only required field needed for Gesture
#         trimmed_Gesture = {key: gesture_Data[key] for key in key_Gesture} #Trimming gesture_Data for key_Gesture
#         try:
#             pointer_numPoints = int(trimmed_Pointer['numDetectedPoints']) #Pullihg Pointer number of Points
#             pointer_frameNum = int(trimmed_Pointer['frameNum']) #Pulling Frame number for time-based reference, e.g. 20 FPS
#             pointCloudArray = [] #Blank Array to store pointCloud info
#             for i in range(pointer_numPoints): #Iterates through total number of points detected
#                  pointCloudArray.append(trimmed_Pointer['pointCloud'][i][0:3]) #Pulling X, Y, Z values per point detected
#             print("Pointer Data")
#             print(pointer_numPoints, "|",pointer_frameNum) #Outputting points, frame number per frame
#             for i in pointCloudArray: #Iterating and outputting each point (X, Y, Z)
#                 print(i)
#             print()
#             print("Gesture Data")
#             print(trimmed_Gesture, '\n') #Outputting feature data
#         except:
#             continue
#     except:
#        continue
# #----------------------------------------------------------------------------