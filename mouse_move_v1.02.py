from gui_parser import *
#Imports___________________________________________________________#
from pynput.mouse import Button, Controller                        # Allows us to control mouse
from radar_filter import *
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
def get_vel(num_points_1, num_points_2, list1, list2):
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

def get_pos(num_points_1, list1):
    # the output data from chirp configuration demo in the first frame
    # num_points = 4 # The chirp configuration demo will output the number of points detected
    # points = np.array([[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]) # The chirp configuration demo will output the coordinates of the points

    # the output data from chirp configuration demo in the second frame
    # num_points_2 = 5 # The chirp configuration demo will output the number of points detected
    # points_2 = np.array([[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]) # The chirp configuration demo will output the coordinates of the points
    x = 0  # variable for x coordinates in the first frame
    y = 0  # variable for y coordinates in the first frame

    # average position of the first frame
    for i in range(num_points_1):  # loop for average position of the first frame

        x += list1[i][0]  # calculate the sum of the magnitude of x coordinates
        y += list1[i][2]  # calculate the sum of the magnitude of y coordinates
        average_x = x / num_points_1  # calculate the average coordinate of x axis
        average_y = y / num_points_1  # calculate the average coordinate of y axis

    return average_x, average_y


#Pointer Positioning
cfg = open("C:/Users/lemal/OneDrive/Desktop/ecen403/Finaldemo/xwr68xx_AOP_profile_2025_03_31T04_44_57_357.cfg", "r") #Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts("COM5", "COM3") #Device-Manager defined Ports
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
pre_x_pos = []
pre_y_pos = []
prev_x = 0
prev_y = 0
avg_x = 0                                                          # Average x_velocity
avg_y = 0                                                          # Average y_velocity
empty_frame_count = 0
original_bool = 0
stop_bool = 1
pre_x_pos = 0
pre_y_pos = 0


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
  
        #print("Gesture Data")
        #print(trimmed_Gesture, '\n') #Outputting feature data

        if pointer_numPoints == 0:
            xvels.append(0)
            yvels.append(0)
            empty_frame_count += 1
            print(empty_frame_count)
            if empty_frame_count == 8:
                point_clouds = []
                data_points = []  
                xvels = []                                                       
                yvels = [] 
                pre_x_pos = 100000
                pre_y_pos = 100000
                empty_frame_count = 0
                stop_bool = 1
            continue

        newPointCloud = filter_ys(pointCloudArray)

        if len(newPointCloud) == 0: 
            xvels.append(0)
            yvels.append(0)
            empty_frame_count += 1
            print(empty_frame_count)
            if empty_frame_count == 8:
                point_clouds = []
                data_points = []  
                xvels = []                                                       
                yvels = [] 
                pre_x_pos = 100000
                pre_y_pos = 100000
                empty_frame_count = 0
                stop_bool = 1
            continue

        x_pos, y_pos = get_pos(len(newPointCloud), newPointCloud)

        if(abs(x_pos) < 0.1 and abs(y_pos) < 0.1):
            stop_bool = 0        

        if ((abs(x_pos) > 0.1 or abs(y_pos) > 0.1)) and stop_bool == 1:
            continue



        # save previous location
        if stop_bool == 0:

            newPointCloud2 = []
            if pre_x_pos !=100000  or pre_y_pos != 100000:
                for point in newPointCloud:

                    if point[0] > (pre_x_pos - 1) and point[0] < (pre_x_pos + 1) and point[2] > (pre_y_pos - 1) and point[2] < (pre_y_pos + 1):
                        newPointCloud2.append(point)
                    else:
                        newPointCloud2 == newPointCloud2               
            print(newPointCloud2)

            point_clouds.append(newPointCloud2)
            data_points.append(len(newPointCloud2))

            if(len(data_points) > 1):
                x_vec, y_vec = get_vel(data_points[0], data_points[1], point_clouds[0], point_clouds[1])
                point_clouds.pop(0)
                data_points.pop(0)
        

                if abs(x_vec) < .05: x_vec = 0
                if abs(y_vec) < .05: y_vec = 0
                if abs(x_vec) > .3: x_vec = 0
                if abs(y_vec) > .3: y_vec = 0
                xvels.append(x_vec)
                yvels.append(y_vec)

            # if abs(x_vec) > .25 or abs(y_vec) > .25: continue
            if(len(xvels) == 0): continue
            while(len(xvels) > 5):
                xvels.pop(0)
                yvels.pop(0)
        
            avg_x = simple_avg(xvels)
            avg_y = simple_avg(yvels)
            if abs(avg_y) < .03: avg_y = 0
            mov_x = (avg_x + prev_x)/2
            mov_y = (avg_y + prev_y)/2

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
            pre_x_pos = x_pos
            pre_y_pos = y_pos

            mouse.move(X, Y)

        if stop_bool == 1:
            mouse.move(0, 0)
    
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