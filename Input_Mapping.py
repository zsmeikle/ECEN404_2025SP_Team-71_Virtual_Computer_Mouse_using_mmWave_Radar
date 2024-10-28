#Imports___________________________________________________________# 
from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays 
import csv                                                         # Allows us to read csv files (for testing)
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
Scale = 1                                                          # scales the X and Y movements by the value
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 30                                                  # refreshrate of the board/data
Test_File = "Test_Data.csv"                                        # the test file being used to demo
                                                                   #
#Test_Functions____________________________________________________# This section is only for testing
def get_data(line, size):                                          # get a specific line of data from the test file
    result = -1                                                    # if output is -1 it is eof or error
    with open(Test_File, "r") as Test_Data:                        #
        data = csv.reader(Test_Data)                               #
        row = list(data)                                           #
        if (line < size):                                          #
            result = row[line]                                     #
    return result                                                  #
                                                                   #
def get_size():                                                    # get the size of a csv file
    result = 0                                                     #
    with open(Test_File, "r") as Test_Data:                        #
        data = csv.reader(Test_Data)                               #
        for i, row in enumerate(data):                             #
            result += 1                                            #
    return result                                                  #
                                                                   #
#Code______________________________________________________________#
mouse = Controller()                                               # defines mouse so we can control it
Delay = 1/Refresh_Rate                                             # Coverts to delay fro mrefresh rate
Frame_Num = 0 #TESTING ONLY, REMOVE LATER!!!                       # Test variable for frame number
                                                                   #
tempX = 1                                                          # these variable will come from Matlab later
tempY = 1                                                          #
tempRight_Click = 0                                                #
tempLeft_Click = 0                                                 #
                                                                   #
X = 0                                                              # Initialize X and Y
Y = 0                                                              #
t0 = 0                                                             # initial time variable
                                                                   #
                                                                   #
while True: #maybe add kill variable                               # Loop to keep running
    t0 = time.time()                                               # get initial time
                                                                   #
    #TESTING_CODE--------------------#                             # Test code
    size = get_size()                #                             # get the size of the file for get_data function
    test = get_data(Frame_Num, size) #                             # Gets the data at the frame number
    if (test == -1):                 #                             # if at eof
        print("end of file")         #                             #
        break                        #                             #
    tempX = int(test[0])             #                             # define variables from data
    tempY = int(test[1])             #                             #
    tempRight_Click = int(test[2])   #                             #
    tempLeft_Click = int(test[3])    #                             #
    Frame_Num += 1                   #                             # incriment frame number
    #END_OF_TESTING CODE-------------#                             #
                                                                   #
                                                                   #
    match Switch_XY:                                               # If we are switching X and Y
        case 0:                                                    #
           X = Scale * Reverse_X * tempX                           #
           Y = Scale * Reverse_Y * tempY                           #
        case 1:                                                    #
           X = Scale * Reverse_X * tempY                           #
           Y = Scale * Reverse_Y * tempX                           #
                                                                   #
    match tempLeft_Click:                                          # If left click
        case 0:                                                    # if nothing no-op
            True                                                   #
        case 1:                                                    #
            mouse.release(Button.left)                             #
        case 2:                                                    #
            mouse.press(Button.left)                               #
                                                                   #
    match tempRight_Click:                                         # If right click
        case 0:                                                    # if nothing no-op
            True                                                   #
        case 1:                                                    #
            mouse.release(Button.right)                            #
        case 2:                                                    #
            mouse.press(Button.right)                              #
                                                                   #
    mouse.move(X, Y)                                               # Actually impliment the mouse movement
    time.sleep(Delay-(time.time() - t0))                           # Delay as per refresh rate
    
    





