import math
import numpy as np
import matplotlib.pyplot as plt

# Generate 20 random points in the X-Y plane (between 0 and 100)
# Weighted average (weights based on some factor, here using uniform weights as an example)

import statistics

def geo_mean(list):
    product = 1
    for num in list:
        product *= num

    list = product ** (1 / len(list))

    geometric_mean = product ** (1 / len(list))
    return geometric_mean
# 123456    561234

def get_pos(number_1,number_2,number_3,number_4,number_5,number_6, list1, list2,list3, list4,list5, list6):

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

