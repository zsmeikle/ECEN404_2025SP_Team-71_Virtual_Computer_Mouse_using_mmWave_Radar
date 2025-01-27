
import math

import time
import statistics

list1 = [[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]
list2 = [[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]
num_points_1 = 4
num_points_2 = 5

def get_pos(num_points_1,num_points_2,list1, list2):

    # the output data from chirp configuration demo in the first frame
    #num_points = 4 # The chirp configuration demo will output the number of points detected
    #points = np.array([[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]) # The chirp configuration demo will output the coordinates of the points

    # the output data from chirp configuration demo in the second frame
    #num_points_2 = 5 # The chirp configuration demo will output the number of points detected
    #points_2 = np.array([[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]) # The chirp configuration demo will output the coordinates of the points
    x = 0 # variable for x coordinates in the first frame
    y = 0 # variable for y coordinates in the first frame
    x_2 = 0 # variable for x coordinates in the second frame
    y_2 = 0 # variable for y coordinates in the second frame

    #average position of the first frame
    for i in range(num_points_1): # loop for average position of the first frame
        if list1[i][2]<2: # select the points with the correct distance z
            x+=list1[i][0] # calculate the sum of the magnitude of x coordinates
            y+=list1[i][1] # calculate the sum of the magnitude of y coordinates
            average_x = x / num_points_1 # calculate the average coordinate of x axis
            average_y = y / num_points_1 # calculate the average coordinate of y axis
        else: # else
            num_points -=1 # count the removed points
            average_x = x / num_points_1 # calculate the average coordinate of x axis
            average_y = y / num_points_1 # calculate the average coordinate of y axis
    print(average_x) # output check
    print(average_y) # output check


    #average position of the second frame
    for i in range(num_points_2): # loop for average position of the second frame 
        if list2[i][2]<2: # select the points with the correct distance z
            x_2+=list2[i][0] # calculate the sum of the magnitude of x coordinates
            y_2+=list2[i][1] # calculate the sum of the magnitude of y coordinates
            average_x_2 = x_2 / num_points_2 # calculate the average coordinate of x axis
            average_y_2 = y_2 / num_points_2 # calculate the average coordinate of y axis
        else: # else
            num_points_2 -=1 # count the removed points
            average_x_2 = x_2 / num_points_2 # calculate the average coordinate of x axis
            average_y_2 = y_2 / num_points_2 # calculate the average coordinate of y axis

    # use average positions to output moving path
    output_v_x = (average_x_2 - average_x) # calculate the velocity in x direction
    output_v_y = (average_y_2 - average_y) # calculate the velocity in y direction

    # velocity in z-direction is not required because the user is required to move his hand in parallel to the radar's x-y plane
    print("V_x euqals to ",output_v_x) # velocity check
    print("V_y euqals to ",output_v_y) # velocity check
    return [output_v_x, output_v_y]

get_pos(num_points_1,num_points_2,list1,list2)
