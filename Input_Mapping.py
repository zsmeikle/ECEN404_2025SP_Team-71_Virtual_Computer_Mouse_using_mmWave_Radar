#Imports___________________________________________________________# 
from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays 
import csv                                                         # Allows us to read csv files (for testing)
import threading                                                   # Allows us to make threads
from Frame_gen import run_frame_gen                                               #
import queue                                                       #
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
Scale = 1                                                          # scales the X and Y movements by the value (must be int)
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 22                                                 # refreshrate of the board/data
frame_gen_frames = 5
frame_gen_on_off = True
lol = False
Test_File = "Test_Data.csv" #TESTING ONLY                          # the test file being used to demo
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
#def main():
shared_queue = queue.Queue()
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
                                                                #
                                                                    #
tempX = 1                                                          # these variable are temporary
tempY = 1                                                          #
tempRight_Click = 0                                                #
tempLeft_Click = 0                                                 #
                                                                    #
X = 0                                                              # Initialize X and Y
Y = 0                                                              #
t0 = 0                                                             # initial time variable
                                                                    #
size = get_size()#Testing only                                     # get the size of the file for get_data function
                                                                    #
                                                                    #
thread = threading.Thread(target=run_frame_gen, args=(shared_queue,Refresh_Rate, frame_gen_frames, lol,))
thread.start()
    
while No_Error:                                                    # Loop to keep running
    t0 = time.time()                                               # get initial time
                                                                    #
    #TESTING_CODE--------------------#                             # Test code
    size = get_size()                #                             # get the size of the file for get_data function
    test = get_data(Frame_Num, size) #                             # Gets the data at the frame number
    if (test == -1):                 #                             # if at eof end loop
        print("end of file")         #                             #
        break                        #                             #
    tempX = int(test[0])             #                             # define variables from data
    tempY = int(test[1])             #                             #
    tempRight_Click = int(test[2])   #                             #
    tempLeft_Click = int(test[3])    #                             #
    Frame_Num += 1                   #                             # incriment frame number
    #END_OF_TESTING CODE-------------#                             #
                                                                    #
    match Switch_XY:                                               # If we are switching X and Y
        case 0:                                                    #
            X = Scale * Reverse_X * tempX                           #
            Y = Scale * Reverse_Y * tempY                           #
        case 1:                                                    #
            X = Scale * Reverse_X * tempY                           #
            Y = Scale * Reverse_Y * tempX                           #
        case default:                                              # Invalid Switch_XY
            print("ERROR: Switch-XY must be a 0 or a 1.")          #
            break                                                  #
                                                                    #
    match tempLeft_Click:                                          # If left click
        case 0:                                                    # if nothing no-op
            True                                                   #
        case 1:                                                    #
            mouse.release(Button.left)                             #
        case 2:                                                    #
            mouse.press(Button.left)                               #
        case default:                                              # Error invaild input
            print("ERROR: invalid left click input: " + str(tempLeft_Click))
            break                                                  #
    match tempRight_Click:                                         # If right click
        case 0:                                                    # if nothing no-op
            True                                                   #
        case 1:                                                    #
            mouse.release(Button.right)                            #
        case 2:                                                    #
            mouse.press(Button.right)                              #
        case default:                                              # Error invaild input
            print("ERROR: invalid right click input: " + str(tempRight_Click))
            break                                                  #
                                                                    #
    if(frame_gen_on_off):
        shared_queue.put((X, Y, True))
    else:
        mouse.move(X, Y)

    if(Frame_Num == 500):
        lol = True
    
    #mouse.move(X, Y)                                               # Actually impliment the mouse movement
    New_Delay = Delay-(time.time() - t0)                           # Calculate delay with processing time
    #print(New_Delay)
    if (New_Delay < 0):                                            # Skip a frame if took to long to compute
        time.sleep(New_Delay + Delay)                              #
        print("Skipped Frame: " + str(Frame_Num))                  # Print if a frame was skipped
    else:                                                          #
        time.sleep(New_Delay)                                      # Delay as per refresh rate and time code took

shared_queue.put((0, 0, 0, False))
thread.join()
#thread.stop()
    #__________________________________________________________________#
#if __name__ == "__main__":
#    main()





