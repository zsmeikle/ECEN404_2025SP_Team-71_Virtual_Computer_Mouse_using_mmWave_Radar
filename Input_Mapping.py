#Imports___________________________________________________________# 
from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays 
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
Scale = 1                                                          # scales the X and Y movements by the value
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
Refresh_Rate = 20                                                  # refreshrate of the board/data
                                                                   #
#Code______________________________________________________________#
mouse = Controller()                                               # defines mouse so we can control it
Delay = 1/Refresh_Rate                                             # Coverts to delay fro mrefresh rate
                                                                   #
tempX = 1 #replace when Matlab                                     # these variable will come from Matlab later
tempY = 1 #replace when Matlab                                     #
tempRight_Click = 0 #replace when Matlab                           #
tempLeft_Click = 0 #replace when Matlab                            #
                                                                   #
X = 0                                                              # Initialize X and Y
Y = 0                                                              #
                                                                   #
                                                                   #
while True: #maybe add kill variable                               # Loop to keep running
    match Switch_XY:                                               # If we are switching X and Y
        case 0:                                                    #
           X = Scale * Reverse_X * tempX                           #
           Y = Scale * Reverse_Y * tempY                           #
        case 1:                                                    #
           X = Scale * Reverse_X * tempY                           #
           Y = Scale * Reverse_Y * tempX                           #
                                                                   #
    match tempLeft_Click:                                          # If left click
        case 0:                                                    # Posibly inefficient but we can worry about that later
            mouse.release(Button.left)                             #
        case 1:                                                    #
            mouse.press(Button.left)                               #
                                                                   #
    match tempRight_Click:                                         # If right click
        case 0:                                                    # See prev comment
            mouse.release(Button.right)                            #
        case 1:                                                    #
            mouse.press(Button.right)                              #
                                                                   #
    mouse.move(X, Y)                                               # Actually impliment the mouse movement
    time.sleep(Delay)                                              # Delay as per refresh rate
    
    





