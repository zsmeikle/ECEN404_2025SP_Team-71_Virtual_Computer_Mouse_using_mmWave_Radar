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

    
    geometric_mean = math.prod(list) ** (1 / len(list))
    
    return geometric_mean
# 123456    561234

def get_pos(list1, list2):

    updated_list1 = [[element + 100 for element in sublist] for sublist in list1]
    updated_list2 = [[element + 100 for element in sublist] for sublist in list2]



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


    distance_x = geo_mean_2_x - geo_mean_1_x
    distance_y = geo_mean_2_y - geo_mean_1_y

    
    velovity_x = distance_x


    velovity_y = distance_y
   

    return velovity_x,velovity_y


#Pointer Positioning
# cfg = open("C:/Users/lemal/OneDrive/Desktop/ecen403/Finaldemo/xwr68xx_AOP_profile_2025_02_17T14_57_20_747.cfg", "r") #Open Config File to send to radar over UART
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

empty_frame_count = 0
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
        
        # limit of number of points
        if pointer_numPoints < 1:
            empty_frame_count += 1
            print(empty_frame_count)
            if empty_frame_count == 8:
                point_clouds = []
                print(point_clouds)
                empty_frame_count =0
            continue
        # data_points is the number of points for the points cloud

        newPointCloud = []
        for point in pointCloudArray:
            minY = 0.15
            maxY = 0.22
            if point[1] > minY and point[1] < maxY:
                newPointCloud.append(point)
            else:
                newPointCloud == newPointCloud
        
        if newPointCloud == []:
            continue  
        #x range
        newPointCloud2 = []
        for point in newPointCloud:
            minX = -0.15
            maxX = 0.15
            if point[0] > minX and point[0] < maxX:
                newPointCloud2.append(point)
            else:
                newPointCloud2 == newPointCloud2

        if newPointCloud2 == []:
            continue                

        #z range

        newPointCloud3 = []
        for point in newPointCloud2:
            minZ = -0.15
            maxZ = 0.15
            if point[0] > minZ and point[0] < maxZ:
                newPointCloud3.append(point)
            else:
                newPointCloud3 == newPointCloud3
             

        new_pointer_numPoints = int(len(newPointCloud3))

        if new_pointer_numPoints < 1:
            continue

        print(pointer_numPoints)
        print(new_pointer_numPoints)
        print(newPointCloud3)
        data_points.append(pointer_numPoints)
        # array of point clouds

        


        #how many points you want to delete
        delete_num = int(0)

        newPointCloud3 = np.array(newPointCloud3)
        newPointCloud3 = [[element + 100 for element in sublist] for sublist in newPointCloud3]

        for num in range(0):
            # Extract x-coordinates
            x_values = np.array([point[0] for point in newPointCloud3])
            y_values = np.array([point[2] for point in newPointCloud3])
            z_values = np.array([point[1] for point in newPointCloud3])
            # Compute the average x value
            avg_x = np.mean(x_values)
            avg_y = np.mean(y_values)
            avg_z = np.mean(z_values)

            # Find the index of the point with the highest |x - avg_x| difference
            idx_to_remove = np.argmax(np.abs((z_values-avg_z)))

            # Remove the point
            newPointCloud3 = np.delete(newPointCloud3, idx_to_remove, axis=0)


        for num in range(delete_num):
            # Extract x-coordinates
            x_values = np.array([point[0] for point in newPointCloud3])
            y_values = np.array([point[2] for point in newPointCloud3])
            z_values = np.array([point[1] for point in newPointCloud3])
            # Compute the average x value
            avg_x = np.mean(x_values)
            avg_y = np.mean(y_values)
            avg_z = np.mean(z_values)

            # Find the index of the point with the highest |x - avg_x| difference
            idx_to_remove = np.argmax(np.abs(((x_values - avg_x)*(2/5))**2+((z_values-avg_z)*(3/5))**2))

            # Remove the point
            newPointCloud3 = np.delete(newPointCloud3, idx_to_remove, axis=0)

        for num in range(delete_num):
            # Extract x-coordinates
            x_values = np.array([point[0] for point in newPointCloud3])
            y_values = np.array([point[2] for point in newPointCloud3])
            z_values = np.array([point[1] for point in newPointCloud3])
            # Compute the average x value
            avg_x = np.mean(x_values)
            avg_y = np.mean(y_values)
            avg_z = np.mean(z_values)

            # Find the index of the point with the highest |x - avg_x| difference
            idx_to_remove = np.argmax(np.abs(((y_values - avg_y)*(2/5))**2+((z_values-avg_z)*(3/5))**2))

            # Remove the point
            newPointCloud3 = np.delete(newPointCloud3, idx_to_remove, axis=0)


        if len(newPointCloud3) == 0:
            continue

        newPointCloud3 = [[element - 100 for element in sublist] for sublist in newPointCloud3]   
            
        #print(newPointCloud3)

        point_clouds.append(newPointCloud3)
        #point_clouds.append(newPointCloud3)
        #print(pointCloudArray)


        if len(point_clouds) < 2:
            continue
        
        #my function
        avg_x, avg_y = get_pos(point_clouds[0],point_clouds[1])
        #[point1,point2]      


        data_points.pop(0)
        point_clouds.pop(0)

        
        if xvels == []:
            last_mov_x = 0
        else:
            last_mov_x = xvels[len(xvels)-1]


        if yvels == []:
            last_mov_y = 0
        else:
            last_mov_y = yvels[len(yvels)-1]            

        if (avg_x > 0 and last_mov_x < 0) or (avg_x < 0 and last_mov_x > 0) or last_mov_x == 0:
            xvels = []
            xvels.append(avg_x)
        else:
            xvels.append(avg_x)
        print(xvels)

        if (avg_y > 0 and last_mov_y < 0) or (avg_y < 0 and last_mov_y > 0) or last_mov_y == 0:
            yvels = []
            yvels.append(avg_y)
        else:
            yvels.append(avg_y)    
        print(yvels)        
        # clean xvels
        #xvels.append(avg_x)
        #yvels.append(avg_y)
        #print(avg_x, avg_y)

        # average velocity
        tot_weight = 0
        avg_x = 0
        avg_y = 0
        for i in range(len(xvels)):
            tot_weight += (i+1)*(i+1)
            avg_x += xvels[i]*(i+1)*(i+1) # apply weights
        avg_x /= tot_weight # Normalize average
        xvels.pop()
        xvels.append(avg_x)  
        avg_x = avg_x * 1000000000
        if abs(avg_x) < 0.03 * 1000000000:
            avg_x = 0
            xvels.pop()
            xvels.append(avg_x)         
        print(avg_x)
        #if(avg_x/avg_y > 10 or avg_y/avg_x > 10)
        #print(avg_x, avg_y)
        tot_weight = 0 
        for i in range(len(yvels)):
            tot_weight += (i+1)*(i+1)
            avg_y += yvels[i]*(i+1)*(i+1) # apply weights
        avg_y /= tot_weight # Normalize average   
        yvels.pop()
        yvels.append(avg_y)    
        avg_y = avg_y * 1000000000
        if abs(avg_y) < 0.03 * 1000000000:
            avg_y = 0
            yvels.pop()
            yvels.append(avg_y) 
        print(avg_y)

        if Switch_XY == 0:  # If we are switching X and Y
            X = XScale * Reverse_X * avg_x / 700000000
            Y = YScale * Reverse_Y * avg_y / 700000000
        elif Switch_XY == 1:
            X = XScale * Reverse_X * avg_x / 700000000
            Y = YScale * Reverse_Y * avg_y / 700000000
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
    except Exception as e:
       print(e)
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