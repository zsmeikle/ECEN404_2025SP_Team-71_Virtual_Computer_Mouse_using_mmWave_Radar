#Imports___________________________________________________________# 
from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays 
import csv    
from my_main import gesture_recognition_model
from gui_parser import *
                                                                   # Allows us to read csv files (for testing)
Radar_model = gesture_recognition_model()                          # ML Implementation
gesture_active = False
DT_counter = 0
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
Scale = 1000                                                          # scales the X and Y movements by the value (must be int)
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 30                                                  # refreshrate of the board/data
DownTime = 30                                                      # number of frames the gesture model waits before next prediction
Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo

# Pointer Positioning Radar - G
my_parser = UARTParser("DoubleCOMPort")  # Defining Pointer Parser from class UARTParser
my_parser.connectComPorts("COM11", "COM10")  # Device-Manager defined Ports

#Code______________________________________________________________#
mouse = Controller()                                               # defines mouse so we can control it
Frame_Num = 0 #TESTING ONLY, REMOVE LATER!!!                       # Test variable for frame number
                                                                   #
No_Error = True                                                    # Kill variable for loop if error
                                                                   #
if (Refresh_Rate <= 0):                                            # Check if refresh rate is within bounds
    print('ERROR: Refresh_Rate must be greater than 0.')           #
    No_Error = False                                               #
else:                                                              #
    Delay = 1/Refresh_Rate                                         # Coverts to delay from refresh rate
                                                                   #
if ((Reverse_X != 1) & (Reverse_X != -1)):                         # Check Reverse_X is -1 or 1
    print('ERROR: Reverse_X must be 1 or -1.')                     #
    No_Error = False                                               #
if ((Reverse_Y != 1) & (Reverse_Y != -1)):                         # Check Reverse_Y is -1 or 1
    print('ERROR: Reverse_Y must be 1 or -1.')                     #
    No_Error = False                                               #
if ((Switch_XY != 1) & (Switch_XY != 0)):                          # Check Switch-XY is 0 or 1
    print('ERROR: Switch_XY must be 0 or 1.')                      #
    No_Error = False                                               #
if (isinstance(Scale, int) != True):                               # Check Scale is an int
    print('ERROR: Scale must be an int.')                          #
    No_Error = False                                               #

#Daniel-------------------------------------------------------------
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
#------------------------------------------------------------------
                                                                   #
                                                                   #
tempX = 1                                                          # these variable are temporary
tempY = 1                                                          #
tempRight_Click = 0                                                #
tempLeft_Click = 0
Frame_Num = 0
prediction_interval = 5                                                 #
                                                                   #
X = 0                                                              # Initialize X and Y
Y = 0                                                              #
t0 = 0                                                             # initial time variable
                                                                   #
prev_gest = 1
cur_gest = 0

data_points = []
point_clouds = []
count = 0
                                                                   #
                                                                   #
while No_Error:                                                    # Loop to keep running
    #Begin Radar Mouse Positioning - G
    try:
        pointer_Data = my_parser.readAndParseUartDoubleCOMPort() #Parsing Pointer radar data
        keys_Pointer = ['frameNum', 'pointCloud', 'numDetectedPoints'] #Only required fields needed for Pointer Position
        trimmed_Pointer = {key: pointer_Data[key] for key in keys_Pointer} #Trimming pointer_Data for keys_Pointer
        pointer_numPoints = int(trimmed_Pointer['numDetectedPoints']) #Pullihg Pointer number of Points
        pointer_frameNum = int(trimmed_Pointer['frameNum']) #Pulling Frame number for time-based reference, e.g. 20 FPS
        pointCloudArray = [] #Blank Array to store pointCloud info
        for i in range(pointer_numPoints): #Iterates through total number of points detected
            pointCloudArray.append(trimmed_Pointer['pointCloud'][i][0:3]) #Pulling X, Y, Z values per point detected
        for i in pointCloudArray: #Iterating and outputting each point (X, Y, Z)
            print(i)

        data_points.append(pointer_numPoints)
        point_clouds.append(pointCloudArray)
        count += 1
        tempX, tempY = 0, 0

        if count > 2:
            point_clouds.pop(0)
            data_points.pop(0)
            tempX, tempY = get_pos(data_points[0], data_points[1], point_clouds[0], point_clouds[1])
        mouse.move(X, Y)
    except:
       continue
    #End - G

    t0 = time.time()                                               # get initial time
                                                                   #
#ML implementation Start
    Radar_model.add_frame()                             # Add Frame to frame catcher
    if gesture_active == False:                         # If a gesture isn't active skip frame
        if Frame_Num % prediction_interval == 0:
            cur_gest = Radar_model.get_prediction()         # Check for Gesture
            print(cur_gest)
            if (cur_gest != 1):                             # If gesture detected start cooldown
                gesture_active = True
                DT_counter = 0
            
                if(prev_gest == cur_gest):
                    if cur_gest == 0:
                        tempLeft_Click = 2
                    if cur_gest == 2:
                        tempRight_Click = 2
                    prev_gest = 1
                else:
                    if cur_gest == 0:   #                             #
                        tempLeft_Click = 1
                    if cur_gest == 1:
                        True
                    if cur_gest == 2: 
                        tempRight_Click = 1
                    prev_gest = cur_gest
    else:                                               # Cooldown
        tempRight_Click = 0   #                             #
        tempLeft_Click = 0
        if(DT_counter < DownTime):
            DT_counter += 1
        else:
            gesture_active = False

       #                             #
    Frame_Num += 1                   #
                                                                   #                                               # If we are switching X and Y
    if Switch_XY == 0:                                                    #
        X = Scale * Reverse_X * tempX                           #
        Y = Scale * Reverse_Y * tempY                           #
    elif Switch_XY == 1:                                                    #
        X = Scale * Reverse_X * tempY                           #
        Y = Scale * Reverse_Y * tempX                           #
    else:                                              # Invalid Switch_XY
        print("ERROR: Switch-XY must be a 0 or a 1.")          #
        break                                                  #
                                                                   #                                        # If left click
    if tempLeft_Click == 0:                                                    # if nothing no-op
        True                                                   #
    elif tempLeft_Click == 1:                                                    #
        mouse.press(Button.left)                               #
        print('Left_press')
    elif tempLeft_Click == 2:                                                    #
        mouse.release(Button.left)                             #
        print('left_release')
    else:                                              # Error invaild input
        print("ERROR: invalid left click input: " + str(tempLeft_Click))
        break                                                  #                                         # If right click
    if tempRight_Click == 0:                                                    # if nothing no-op
        True                                                   #
    elif tempRight_Click == 1:                                                    #
        mouse.press(Button.right)                              #
        print('right_press')
    elif tempRight_Click == 2:                                                    #                              
        mouse.release(Button.right)                            #
        print('right_release')
    else:                                              # Error invaild input
        print("ERROR: invalid right click input: " + str(tempRight_Click))
        break                                                  #
                                                                   #
                                            # Actually impliment the mouse movement
    #New_Delay = Delay-(time.time() - t0)                           # Calculate delay with processing time
    #if (New_Delay < 0):                                            # Skip a frame if took to long to compute
    #    time.sleep(1)#(New_Delay + Delay
    #    print("Skipped Frame: " + str(Frame_Num))                  # Print if a frame was skipped
    #else:                                                          #
    #    time.sleep(1)                                      # Delay as per refresh rate and time code tookNew_Delay
#__________________________________________________________________#