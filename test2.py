import csv
import math
import numpy as py
import time
import statistics

fps = 20
time_dis = 1/fps
i = 1
x = []
y = []
z = []

#activate = 1
#while activate == 1:

    
    # input csv data file
with open('C:/Users/lemal/Desktop/ecen403/sampledata.csv', 'r') as position_data:
    position_data = csv.reader(position_data)
    
    # extracting field names through first row
    next(position_data)
    position_data = list(position_data) # convert data to string list

    point_num = (len(position_data[0]))//3 # calc point num 
    print(f'{point_num} points in the list')

    points = [[] for i in range(point_num)] # build point list 
    
   # extracting each data row one by one
    for line in position_data:
        for i in range(point_num):
            sample_x = float(line[0 + i*3])
            sample_y = float(line[1 + i*3])
            sample_z = float(line[2 + i*3])
            points[i].append([sample_x,sample_y,sample_z])
    
   # print(points)



    
    velocities = []
    velocities = [[] for i in range(point_num)]
    count = 0
  #  velocities = [[] for i in range(point_num)]
    for i in range(point_num):
        for j in range(len(points[i])-1):
            if points[i][j][2] <= 1:
                velocities[i].append([(points[i][j+1][0] - points[i][j][0]) * fps, 
                                    (points[i][j+1][1] - points[i][j][1]) * fps, 
                                    (points[i][j+1][2] - points[i][j][2]) * fps])
                count +=1
            else:
                continue
    velocity_clear = []
    for x in velocities:
        if x!=[]:
            velocity_clear.append(x)
    hand_points = int(count/len(velocity_clear[0]))
    nunmber_velocity = len(velocity_clear[0])
    
    # delete empty data and address the output velocity
    final_velocity = [[],[],[]]
    j = 0
    while j < nunmber_velocity:
        x_v = 0
        y_v = 0
        z_v = 0
        i=0
        while i< hand_points:
            x_v += velocity_clear[i][j][0]
            y_v += velocity_clear[i][j][1]
            z_v += velocity_clear[i][j][2]
            i+=1
        final_velocity[0].append(x_v/hand_points)
        final_velocity[1].append(y_v/hand_points)
        final_velocity[2].append(z_v/hand_points)
        j+=1     

print(velocity_clear)
print(hand_points)
 
print(nunmber_velocity)

# final output
print(final_velocity)


        

#time.sleep(1/(fps))  # Sleep for 1/20th of a second