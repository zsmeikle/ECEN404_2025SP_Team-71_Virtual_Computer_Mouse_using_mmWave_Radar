#Imports___________________________________________________________# 
from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays 
                                                                   #
#Settings__________________________________________________________# These variables let us change different factors
Scale = 1                                                          # scales the X and Y movements by the value
Switch_XY = 0                                                      # switches X with Y and vice versa (0 = off, 1 = on)
Reverse_X = 1                                                      # reverses X (1 = off, -1 = on)
Reverse_Y = 1                                                      # reverses Y (1 = off, -1 = on)
                                                                   #
#Code______________________________________________________________#
mouse = Controller()

tempX = 1 #replace when Matlab
tempY = 1 #replace when Matlab
X = 0
Y = 0


while True:
    match Switch_XY:
        case 0:
           X = Scale * Reverse_X * tempX
           Y = Scale * Reverse_Y * tempY 
        case 0:
           X = Scale * Reverse_X * tempY
           Y = Scale * Reverse_Y * tempX
    
    mouse.move(x[n%4], y[n%4])
    n += 1
    time.sleep(0.05)
    
    





