from gui_parser import *
import matplotlib.pyplot as plt
cfg = open("C:/Users/lostk/Downloads/xwr68xx_AOP_profile_2025_02_18T21_04_53_947.cfg", "r") #Open Config File to send to radar over UART
my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts("COM6", "COM5") #Device-Manager defined Ports
my_parser.sendCfg(cfg) #Send Config File
cfg.close() #Close File

x_array = []
z_array = []
frames = []
k=0
num_frames = 15
while(k < num_frames):
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

        x_pos = 0
        z_pos = 0
        for i in pointCloudArray:
            x_pos += i[0]
            z_pos += i[2]
        x_array.append(x_pos/pointer_numPoints)
        z_array.append(z_pos/pointer_numPoints)
        frames.append(pointer_frameNum)
        k += 1
    except:
        continue

x_pos = []
z_pos = []
x_vels = []
z_vels = []
for i in range(num_frames-1):
    x_pos.append(x_array[i])
    z_pos.append(z_array[i])
    x_vels.append(x_array[i+1] - x_array[i])
    z_vels.append(z_array[i+1] - z_array[i])

plt.quiver(x_pos, z_pos, x_vels, z_vels) #Vector map
# plt.plot(x_pos, z_pos, linestyle="None", marker=".") #Average pos
plt.show()



# plt.subplot(3, 1, 1)
# plt.stem(frames, x_array, basefmt=" ")
# plt.subplot(3, 1, 2)
# plt.stem(frames, z_array, basefmt=" ")
# # plt.subplot(3, 1, 3)
# # plt.stem(z_array, x_array, basefmt= " ")
# plt.show()
    