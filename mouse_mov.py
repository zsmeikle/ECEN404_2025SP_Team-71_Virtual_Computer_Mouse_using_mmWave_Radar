from gui_parser import *
#Imports___________________________________________________________#
from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays
import math
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
XScale = 1100                                                      # scales the X and Y movements by the value (must be int)
YScale = 1150
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = -1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = -1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 20                                                  # refreshrate of the board/data
# Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo

#-----------------------------------------------------------------------------
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
#Pointer Positioning
cfg = open("C:/Users/lostk/Downloads/xwr68xx_AOP_profile_2025_02_17T14_44_16_998.cfg", "r") #Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts("COM7", "COM8") #Device-Manager defined Ports
my_parser.sendCfg(cfg) #Send Config File
cfg.close() #Close File

#ML Gesture
# my_parser2 = UARTParser("DoubleCOMPort") #Defining Gesture Parser from class UARTParser
# my_parser2.connectComPorts("COM9", "COM10") #Device-Manager defined Ports
tempX = 1                                                          # these variable are temporary
tempY = 1                                                          #
count = 0
prevFrame = 0
data_points = []
point_clouds = []
mouse = Controller()
xvels = []
yvels = []
num_vels = 0
continous_frames = 0

avg_x = 0
avg_y = 0
while(1): #Radars connected and running, always true until not - Implement GUI?
    try:
        pointer_Data = my_parser.readAndParseUartDoubleCOMPort() #Parsing Pointer radar data

        # gesture_Data = my_parser2.readAndParseUartDoubleCOMPort() #Parsing Gesture radar data

        keys_Pointer = ['frameNum', 'pointCloud', 'numDetectedPoints'] #Only required fields needed for Pointer Position
        trimmed_Pointer = {key: pointer_Data[key] for key in keys_Pointer} #Trimming pointer_Data for keys_Pointer
        key_Gesture = ['features'] #Only required field needed for Gesture
        #trimmed_Gesture = {key: gesture_Data[key] for key in key_Gesture} #Trimming gesture_Data for key_Gesture
        pointer_numPoints = int(trimmed_Pointer['numDetectedPoints']) #Pullihg Pointer number of Points
        pointer_frameNum = int(trimmed_Pointer['frameNum']) #Pulling Frame number for time-based reference, e.g. 20 FPS
        pointCloudArray = [] #Blank Array to store pointCloud info
        for i in range(pointer_numPoints): #Iterates through total number of points detected
            pointCloudArray.append(trimmed_Pointer['pointCloud'][i][0:3]) #Pulling X, Y, Z values per point detected
        #print("Pointer Data")
        #print(pointer_numPoints, "|",pointer_frameNum) #Outputting points, frame number per frame
        # for i in pointCloudArray: #Iterating and outputting each point (X, Y, Z)
        #     print(i)

        #print()
        #print("Gesture Data")
        #print(trimmed_Gesture, '\n') #Outputting feature data
        if(pointer_frameNum - prevFrame > 3 or continous_frames > 10):
            xvels.clear()
            yvels.clear()
            num_vels = 0
            data_points.clear()
            point_clouds.clear()
            count = 0
            avg_x, avg_y = 0, 0
            continous_frames = 0

        if(pointer_numPoints > 0):
            data_points.append(pointer_numPoints)
            point_clouds.append(pointCloudArray)
            count += 1
            tempX, tempY = 0, 0
            prevFrame = pointer_frameNum
            continous_frames += 1

            if count > 2:
                point_clouds.pop(0)
                data_points.pop(0)
                tempX, tempY = get_pos(data_points[0], data_points[1], point_clouds[0], point_clouds[1])
                if abs(tempX) < .07: tempX = 0
                if abs(tempY) < .07: tempY = 0
                xvels.append(tempX)
                yvels.append(tempY)
                num_vels += 1 
        else:
            xvels.append(0)
            yvels.append(0)
            num_vels += 1
        avg_x = 0
        avg_y = 0
        tot_weight = 0
        for i in range(num_vels):
            tot_weight += (i+1)
            avg_x += xvels[i]*(i+1)
            avg_y += yvels[i]*(i+1)
        avg_x /= tot_weight
        avg_y /= tot_weight
        #if(avg_x/avg_y > 10 or avg_y/avg_x > 10)
        #print(avg_x, avg_y)
        if Switch_XY == 0:  # If we are switching X and Y
            X = XScale * Reverse_X * avg_x  #
            Y = YScale * Reverse_Y * avg_y  #
        elif Switch_XY == 1:
            X = XScale * Reverse_X * avg_y  #
            Y = YScale * Reverse_Y * avg_x  #
        else:
            print("ERROR: Switch-XY must be a 0 or a 1.")  #
            break  #
                #
        mouse.move(X, Y)  # Actually impliment the mouse movement
        # New_Delay = Delay - (time.time() - t0)  # Calculate delay with processing time
        # if (New_Delay < 0):  # Skip a frame if took to long to compute
        #     time.sleep(New_Delay + Delay)  #
        #     print("Skipped Frame: " + str(Frame_Num))  # Print if a frame was skipped
        # else:  #
        #     time.sleep(New_Delay)  # Delay as per refresh rate and time code took
    # __________________________________________________________________#
    except:
       continue
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