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
def geo_mean(list):
    product = 1
    for num in list:
        product *= num

    list = product ** (1 / len(list))

    geometric_mean = product ** (1 / len(list))
    return geometric_mean
# 123456    561234

def get_pos(list1, list2,list3, list4,list5, list6):

    updated_list1 = [[element + 100 for element in sublist] for sublist in list1]
    updated_list2 = [[element + 100 for element in sublist] for sublist in list2]
    updated_list3 = [[element + 100 for element in sublist] for sublist in list3]
    updated_list4 = [[element + 100 for element in sublist] for sublist in list4]
    updated_list5 = [[element + 100 for element in sublist] for sublist in list5]
    updated_list6 = [[element + 100 for element in sublist] for sublist in list6]


#list1 x
    first_elements_1_x = [sublist[0] for sublist in updated_list1]
#list1 y
    first_elements_1_y = [sublist[2] for sublist in updated_list1]
    geo_mean_1_x = geo_mean(first_elements_1_x)
    geo_mean_1_y = geo_mean(first_elements_1_y)



#list2 x
    first_elements_2_x = [sublist[0] for sublist in updated_list2]
#list2 y
    first_elements_2_y = [sublist[2] for sublist in updated_list2]
    geo_mean_2_x = geo_mean(first_elements_2_x)
    geo_mean_2_y = geo_mean(first_elements_2_y)

#list3 x
    first_elements_3_x = [sublist[0] for sublist in updated_list3]
#list3 y
    first_elements_3_y = [sublist[2] for sublist in updated_list3]
    geo_mean_3_x = geo_mean(first_elements_3_x)
    geo_mean_3_y = geo_mean(first_elements_3_y)



#list4 x
    first_elements_4_x = [sublist[0] for sublist in updated_list4]
#list4 y
    first_elements_4_y = [sublist[2] for sublist in updated_list4]
    geo_mean_4_x = geo_mean(first_elements_4_x)
    geo_mean_4_y = geo_mean(first_elements_4_y)

#list5 x
    first_elements_5_x = [sublist[0] for sublist in updated_list5]
#list5 y
    first_elements_5_y = [sublist[2] for sublist in updated_list5]
    geo_mean_5_x = geo_mean(first_elements_5_x)
    geo_mean_5_y = geo_mean(first_elements_5_y)


#list6 x
    first_elements_6_x = [sublist[0] for sublist in updated_list6]
#list6 y
    first_elements_6_y = [sublist[2] for sublist in updated_list6]
    geo_mean_6_x = geo_mean(first_elements_6_x)
    geo_mean_6_y = geo_mean(first_elements_6_y)

    x_points = np.array([geo_mean_1_x,geo_mean_2_x,geo_mean_3_x,geo_mean_4_x,geo_mean_5_x,geo_mean_6_x])
    y_points = np.array([geo_mean_1_y,geo_mean_2_y,geo_mean_3_y,geo_mean_4_y,geo_mean_5_y,geo_mean_6_y])
    slope, intercept = np.polyfit(x_points, y_points, 1)
    distance_x = geo_mean_6_x - geo_mean_1_x
    distance_y = geo_mean_6_y - geo_mean_1_y
    mag_distance = math.sqrt(distance_x**2+distance_y**2)

    angle_radians = math.atan(slope)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)
    if geo_mean_6_y > geo_mean_1_y:
        velovity_y = mag_distance * math.sin(angle_radians)
    else:
        velovity_y = -mag_distance * math.sin(angle_radians)
        
    if geo_mean_6_x > geo_mean_1_x:
        velovity_x = mag_distance * math.cos(angle_radians)
    else:
        velovity_x = -mag_distance * math.cos(angle_radians)

    return velovity_x,velovity_y


#Pointer Positioning
cfg = open("C:/Users/lemal/OneDrive/Desktop/ecen403/Finaldemo/xwr68xx_AOP_profile_2025_02_17T14_57_20_747.cfg", "r") #Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts("COM5", "COM3") #Device-Manager defined Ports
my_parser.sendCfg(cfg) #Send Config File
cfg.close() #Close File

#ML Gesture
# my_parser2 = UARTParser("DoubleCOMPort") #Defining Gesture Parser from class UARTParser
# my_parser2.connectComPorts("COM9", "COM10") #Device-Manager defined Ports
tempX = 1                                                          # these variable are temporary
tempY = 1                                                          #
count = 0                                                          # Tracking number of frames stored
prevFrame = 0                                                      # Set to 0 on startup
data_points = []                                                   # stores num_points for frames //Only 2 are need for velocity calculations
point_clouds = []                                                  # stores point clouds for frames
mouse = Controller()                                               # Start mouse controller
xvels = []                                                         # stores x-velocities calculated from 2 frames
yvels = []                                                         # stores y-velocities calculated from 2 frames
num_vels = 0                                                       # tracks num of velocities
continous_frames = 0                                               # tracks number of continuous active frames

avg_x = 0                                                          # Average x_velocity
avg_y = 0                                                          # Average y_velocity

# first 5 frames, mouse does not move, 6th frame mouse 
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

        if pointer_numPoints == 0: 
            continue
        count += 1
        # data_points is the number of points for the points cloud
        data_points.append(pointer_numPoints)
        # array of point clouds
        point_clouds.append(pointCloudArray)


        if len(data_points) < 6:
            continue
    
        #my function
        avg_x, avg_y = get_pos(point_clouds[0],point_clouds[1],point_clouds[2],point_clouds[3],point_clouds[4],point_clouds[5])
        #[1,2,3,4,5,6]

        data_points.pop(0)
        data_points.pop(1)
        data_points.pop(2)
        data_points.pop(3)
        point_clouds.pop(0)
        point_clouds.pop(1)
        point_clouds.pop(2)
        point_clouds.pop(3)
        #[5,6] len = 2
        #[[[],[]],[[],[]]]


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