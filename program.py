from gui_parser import *
#Imports___________________________________________________________#
from pathlib import Path
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
# Get cwd and make all paths for used resources
cwd = Path.cwd()
model_path = cwd.joinpath("resources", "OOB_Gesture_CNN2.keras")
scaler_path = cwd.joinpath("resources", "OOB_Gesture_scaler2.bin")
cfg_path = cwd.joinpath("resources", "radar.cfg")
icon_path = cwd.joinpath("resources", "TI_Logo.ico")

# Identify ports used by radar
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
mouse_smoothing = "Velocity"
frame_gen_on_off = 0  # Unchecked = 0 (off), Checked = 1 (on)
frame_gen_frames = 1     # Default value, range 1 to 20
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 24                                                  # refreshrate of the board/data
# Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo

#-----------------------------------------------------------------------------

#Velocity Tracking variables
x_vec = 1                                                          # these variable are temporary
y_vec = 1                                                          #
data_points = []                                                   # stores num_points for frames //Only 2 are need for velocity calculations
point_clouds = []                                                  # stores point clouds for frames
mouse = Controller()                                               # Start mouse controller
xvels = []                                                         # stores x-velocities calculated from 2 frames
yvels = []                                                         # stores y-velocities calculated from 2 frames
num_vels = 0                                                       # tracks num of velocities
track_CD = 0                                                       # tracks count down for hand tracking outside boundaries
cur_x = 1                                                          # used to check current x-position
cur_z = 1                                                          # used to check current z-position
prev_x = 0                                                         # used to track previous x-position
prev_y = 0                                                         # used to track previous y-position
lastFrame = 0                                                      # tracks frame number of last significant frame

#-------------------------------------------------------------------------------
#Position Tracking Variables
x_array = []                                                       # tracks previous x-positions
z_array = []                                                       # tracks previous z-positions
prev_posX = 0                                                      # tracks the previous cursor X-position
prev_posY = 0                                                      # tracks the previous cursor Y-position
screen_width = 2560                                                # variable used to store screen width
screen_height = 1600                                               # variable used to store screen height

#-------------------------------------------------------------------------------

# Custom color scheme for GUI
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_BG = "#2e2e2e"
TEXT_FG = "#00ff00"

# Checks if a gesture is repeated and maps the gesture to a mouse action
def gesture_action(cur_gest, prev_gest, gesture_map):
    if(cur_gest == 0):
        return prev_gest
    else:
        if(cur_gest != prev_gest):
            map_action(False, gesture_map[cur_gest])
            return cur_gest
        else:
            map_action(True, gesture_map[cur_gest])
            return 0
            
# Helper function for gesture_action
def map_action(repeat_bol, mouse_action):
    if(mouse_action == "LEFT_HOLD_RELEASE"):
        if(repeat_bol): mouse.release(Button.left)
        else: mouse.press(Button.left)
    if(mouse_action == "RIGHT_CLICK"):
        mouse.click(Button.right)
    if(mouse_action == "DOUBLE_LEFT"):
        mouse.click(Button.left, 2)
    if(mouse_action == "SCROLL"):
        mouse.scroll(0, 10)
        
# get_pos takes 4 inputs
def get_pos(num_points_1, num_points_2, list1, list2):
    # the output data from chirp configuration demo in the first frame
    # num_points = 4 # The chirp configuration demo will output the number of points detected
    # points = np.array([[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]) # The chirp configuration demo will output the coordinates of the points

    # the output data from chirp configuration demo in the second frame
    # num_points_2 = 5 # The chirp configuration demo will output the number of points detected
    # points_2 = np.array([[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]) # The chirp configuration demo will output the coordinates of the points
    global cur_z, cur_x
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
        cur_x = abs(average_x_2)
        cur_z = abs(average_y_2)

    # use average positions to output moving path
    output_v_x = (average_x_2 - average_x)  # calculate the velocity in x direction
    output_v_y = (average_y_2 - average_y)  # calculate the velocity in y direction

    # velocity in z-direction is not required because the user is required to move his hand in parallel to the radar's x-y plane
    # print("V_x euqals to ", output_v_x)  # velocity check
    # print("V_y euqals to ", output_v_y)  # velocity check
    return output_v_x, output_v_y

# track_vel function returns X and Y movement vectors based on the perceived velocity of the hand.
# The input for this function is the current pointCloud
# The first output is a boolean variable that tells the main function if it should skip the frame for tracking
# The second and third return values are the movement vectors, X and Y respectively
def track_vel(pointCloud):
    # global variables used by function
    global num_vels, prev_x, prev_y, track_CD

    # Checks if frame is empty. If empty, append previous velocities with a factor of .5.
    # If out of bounds and count down is 0 reset tracking variables
    numPoints = len(pointCloud)
    if numPoints == 0:
        xvels.append(prev_x * .5)
        yvels.append(prev_y * .5)
        if(track_CD > 0):
            track_CD -= 1
            if(track_CD == 0):
                data_points.clear()
                point_clouds.clear()
                xvels.clear()
                yvels.clear()
                num_vels = 0
        return True, 0, 0

    #Filter point cloud based on y-position
    newPointCloud = filter_ys(pointCloud)
    point_clouds.append(newPointCloud)
    data_points.append(len(newPointCloud))

    # If two frames are stored calculate the velocity between the two.
    if (len(data_points) > 1):
        # Get velocity vectors assuming 1 frame difference
        x_vec, y_vec = get_pos(data_points[0], data_points[1], point_clouds[0], point_clouds[1])

        #pop oldest frame data
        point_clouds.pop(0)
        data_points.pop(0)

        # Check if current point is within tracking bounds
        # If it is start count down, if it isn't check if the count down is 0.
        # If count down is 0 then skip frame.
        if (cur_x < .1 and cur_z < .1):
            track_CD = 25
        else:
            if (track_CD == 0): return True, 0, 0
        # clip velocities if they are too large or too small
        if abs(x_vec) < .05: x_vec = 0
        if abs(y_vec) < .05: y_vec = 0
        if abs(x_vec) > .3: x_vec = 0
        if abs(y_vec) > .3: y_vec = 0
        xvels.append(x_vec)
        yvels.append(y_vec)

    # if abs(x_vec) > .25 or abs(y_vec) > .25: continue

    #if no stored velocities skip frame
    if (len(xvels) == 0): return (True, 0 , 0)

    # only keep the latest 5 calculated velocities
    while (len(xvels) > 5):
        xvels.pop(0)
        yvels.pop(0)

    # calculate average velocities
    avg_x = simple_avg(xvels)
    avg_y = simple_avg(yvels)

    # clip y velocity if it is too small
    if abs(avg_y) < .03: avg_y = 0

    # use the averge of the previous velocity and the current velocity
    mov_x = (avg_x + prev_x) / 2
    mov_y = (avg_y + prev_y) / 2

    # Update previous velocity
    prev_x = avg_x
    prev_y = avg_y

    # Switch X and Y if necessary and calculate mouse movement vectors
    if Switch_XY == 0:  # If we are switching X and Y
        X = XScale * Reverse_X * mov_x  #
        Y = YScale * Reverse_Y * mov_y  #
    elif Switch_XY == 1:
        X = XScale * Reverse_X * mov_y  #
        Y = YScale * Reverse_Y * mov_x  #
    else:
        print("ERROR: Switch-XY must be a 0 or a 1.")  #
    # decrease tracking count down
    track_CD -= 1

    # Check if count down is 0 and reset all tracking variables
    if(track_CD == 0):
        data_points.clear()
        point_clouds.clear()
        xvels.clear()
        yvels.clear()
        num_vels = 0

    # return movement vector
    return False, X, Y

# this function uses velocities to calculate the mouse movement vector using different logic than track_vel()
# It takes two inputs the current pointCloud and the current frame number
# Its outputs are the same as track_vel()
def track_vel2(pointCloud, frameNum):
    # global variables used by function
    global lastFrame, prev_x, prev_y

    # check if emmpty frame. Append 0 velocity to array of previous velocities
    if len(pointCloud) == 0: 
        xvels.append(0)
        yvels.append(0)
        return True, 0, 0
        
    # filter out points that have low doppler
    newPointCloud = filter_doppler(pointCloud)
    # If no points left skip frame
    if(len(newPointCloud) == 0): return True, 0, 0
    # newPointCloud = filter_ys(newPointCloud)
    # if(len(newPointCloud) == 0): continue

    #append pointCloud to previous frame tracker
    point_clouds.append(newPointCloud)

    # If difference between frames is larger than 8 reset pointClouds
    if(frameNum - lastFrame > 8):
        if(len(point_clouds) > 1):
            point_clouds.pop(0)
    # Update lastFrame
    lastFrame = frameNum

    # If two consecutive frames calcualte normalized velocity vector assuming 1 frame difference
    if(len(point_clouds) > 1):
        # Make x and z arrays for both pointClouds
        point_x1 = [point[0] for point in point_clouds[0]]
        point_z1 = [point[2] for point in point_clouds[0]]
        point_x2 = [point[0] for point in point_clouds[1]]
        point_z2 = [point[2] for point in point_clouds[1]]
        # Calculate averages
        x_pos1 = simple_avg(point_x1)
        z_pos1 = simple_avg(point_z1)
        x_pos2 = simple_avg(point_x2)
        z_pos2 = simple_avg(point_z2)
        # x_pos.append(x_pos1)
        # y_pos.append(z_pos1)
        
        # Calculate normalized velocities
        y_vec = z_pos2-z_pos1
        x_vec = x_pos2-x_pos1

        # remove oldest pointCloud
        point_clouds.pop(0)
    

        # if abs(x_vec) < .05: x_vec = 0
        # if abs(y_vec) < .05: y_vec = 0
        # clip velocities if they are too large (most likely made from noise)
        if abs(x_vec) > .21: x_vec = 0
        if abs(y_vec) > .21: y_vec = 0
        # append velocities to array tracking previous velocities
        xvels.append(x_vec)
        yvels.append(y_vec)

    # if abs(x_vec) > .25 or abs(y_vec) > .25: continue

    # if previous velocities are empty skip frame
    if(len(xvels) == 0): return True, 0, 0
    # check that only the last 5 frames are being used
    while(len(xvels) > 5):
        xvels.pop(0)
        yvels.pop(0)
        # x_pos.pop(0)
        # y_pos.pop(0)

    #calculate average velocity using last 5 velocities
    avg_x = simple_avg(xvels)
    avg_y = simple_avg(yvels)

    # adjust velocity for higher control over small mouse cursor movements
    if(abs(avg_x) > .07): avg_x *= 3
    else: avg_x /= 4
    if(abs(avg_y) > .08): avg_y *= 2
    else: avg_y /= 4

    # use avergae between this and last average velocities
    mov_x = (avg_x + prev_x)/2
    mov_y = (avg_y + prev_y)/2

    # update previous velocities
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
    
# This function returns the motion vector based on the point cloud data from current frame.
# The first return value is a skip boolean which tells the program to skip the frame if no valuable data is available
# The last two return values are the movement vectors in the X-Y direction of the screen
def track_pos(pointCloud):
    # Global variables used by this function
    global prev_posX, prev_posY, screen_height, screen_width

    # Intialize x and z
    x_pos = 0
    z_pos = 0
    # Check for empty frame
    if (len(pointCloud) == 0): return True, 0, 0

    # Filter points based on y-values and doppler. Check for empty data after
    newPointCloud = filter_ys(pointCloud)
    pointer_numPoints = len(newPointCloud)
    if pointer_numPoints == 0:
        return True, 0, 0
    newPointCloud = filter_doppler(newPointCloud)
    pointer_numPoints = len(newPointCloud)
    if pointer_numPoints == 0:
        return True, 0, 0

    #Calculate average x and z position
    for point in newPointCloud:
        x_pos += point[0]
        z_pos += point[2]

    x_pos /= pointer_numPoints
    z_pos /= pointer_numPoints

    # append new position to the array containig the previous 10 frames
    x_array.append(x_pos)
    z_array.append(z_pos)

    # Make sure that only the last 10 significant frames are being taken into consideration
    while(len(x_array) > 10):
        x_array.pop(0)
        z_array.pop(0)

    # Take the average position of the last 10 frames
    avg_x = simple_avg(x_array)
    avg_z = simple_avg(z_array)
    
    # Convert hand position into cursor position on screen
    X = screen_width * (avg_x + .26)/.52   #The x-axis is shifted by .26 so that 0 is at the middle of the screen
    Y = screen_height * (avg_z + .2)/.4    #The z-axis is shifted by .20 so that 0 is at the middle of the screen

    # Check if hand is within the screen if not move it to the edge in which it's laying.
    if(X < 0):
        Y = prev_posY
        if(prev_posX != 0): X = 0
        else: X = prev_posX
    elif(X > screen_width):
        Y = prev_posY
        if(prev_posX != screen_width): X = screen_width
        else: X = prev_posX
    elif(Y < 0):
        X = prev_posX
        if(prev_posY != 0): Y = 0
        else: Y = prev_posY
    elif(Y > screen_height):
        X = prev_posX
        if(prev_posY != screen_height): Y = screen_height
        else: Y = prev_posY
    
    # Calculate change in position so that the output is compatible with frame generator
    delta_x = X-prev_posX
    delta_y = Y-prev_posY

    # Update previous location
    prev_posX = X
    prev_posY = Y

    # Return motion vectors
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

    #Check for invalid settings (Repeat mouse actions)
    if ((hold_release_left_click == right_click and right_click != "None") or (hold_release_left_click == double_left_click and hold_release_left_click != "None") or (double_left_click == right_click and right_click != "None")):
        print("Invalid Gesture Settings: Same gesture assigned to more than one action")
    else:
        # Update gesture to mouse action mapping
        for i in range(4):
            gesture_dict[i] = "NONE"
        if hold_release_left_click == "Push":
            gesture_dict[1] = "LEFT_HOLD_RELEASE"
        elif hold_release_left_click == "Shine":
            gesture_dict[2] = "LEFT_HOLD_RELEASE"
        elif hold_release_left_click == "Pull":
            gesture_dict[3] = "LEFT_HOLD_RELEASE"
        
        if right_click == "Push":
            gesture_dict[1] = "RIGHT_CLICK"
        elif right_click == "Shine":
            gesture_dict[2] = "RIGHT_CLICK"
        elif right_click == "Pull":
            gesture_dict[3] = "RIGHT_CLICK"

        if double_left_click == "Push":
            gesture_dict[1] = "DOUBLE_LEFT"
        elif double_left_click == "Shine":
            gesture_dict[2] = "DOUBLE_LEFT"
        elif double_left_click == "Pull":
            gesture_dict[3] = "DOUBLE_LEFT"
    
    # Show updated settings
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

#Pointer Positioning
cfg = open(cfg_path, "r") #Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts(com_port, data_port) #Device-Manager defined Ports
my_parser.sendCfg(cfg) #Send Config File
cfg.close() #Close File

# initialize gesture model
model = gesture_recognition_model(model_path, scaler_path)

gesture_names = ["NO_GESTURE", "PUSH", "SHINE", "PULL", "SHAKE"]
gesture_dict = {0:"NONE",
                1:"LEFT_HOLD_RELEASE",
                2:"RIGHT_CLICK",
                3:"DOUBLE_LEFT",
                4:"SCROLL"}

#populate initial frames
frames = 0
while(frames < model.frames):
    radarData = my_parser.readAndParseUartDoubleCOMPort() #Parsing Pointer radar data
    # gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data
    frameNum = radarData["frameNum"]
    numPoints = radarData["numDetectedPoints"]
    pointCloud = radarData["pointCloud"]

    model.fill_frame(numPoints, pointCloud)
    frames += 1

#restart tracking variables
frames = 0
DT_counter = 0
gesture_active = 0
prev_gest = 0
gesture_validation = 0


# GUI main loop
def radar_loop():
    global frames
    global frame_gen_on_off
    global DT_counter
    global gesture_active
    global prev_gest
    global gesture_validation
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
                    if (cur_gest != 0):  # If gesture detected start cooldown
                        if(cur_gest == gesture_validation):
                            print(gesture_dict[cur_gest])
                            gesture_active = True
                            prev_gest = gesture_action(cur_gest, prev_gest, gesture_dict)
                            gesture_validation = 0
                        else: 
                            gesture_validation = cur_gest
                            print(gesture_dict[cur_gest])
            else:  # Cooldown
                if (DT_counter < 20):
                    DT_counter += 1
                else:
                    DT_counter = 0
                    gesture_active = False
            if(mouse_smoothing == "Velocity"):
                skip_bol, X, Y = track_vel2(pointCloud, frameNum)
            else:
                skip_bol, X, Y = track_pos(pointCloud)
            if(skip_bol): continue

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
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title("Virtual Mouse")
root.geometry("500x550")
root.configure(bg=BG_COLOR)

# Set window icon
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print("Icon not found:", e)

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=BG_COLOR)
style.configure('TButton', background=BUTTON_COLOR, foreground='white',
                font=('Helvetica', 10, 'bold'), borderwidth=1)
style.map('TButton', background=[('active', BUTTON_COLOR), ('pressed', '#3a6a7c')])

# Create Settings frame
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

# Hold/Release Left Click setting
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

# Double Left Click setting
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

# Right Click setting
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

# Create and assign the label for the slider so we can show/hide it
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


# Update function to show/hide the slider components
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
