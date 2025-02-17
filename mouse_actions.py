from pynput.mouse import Button, Controller                        # Allows us to control mouse
import time                                                        # Allows us to add delays 
import csv    
from gesture_recognition import gesture_recognition_model

Radar_model = gesture_recognition_model()                          # ML Implementation
mouse = Controller()
gesture_active = False
DT_counter = 0
DownTime = 30

gestures =[
    "PUSH",             #ID: 0
    "NO_GESTURE",       #ID: 1
    "SHINE",            #ID: 2
    "TBD1",             #ID: 3
    "TBD2"              #ID: 4
    ]
mouse_act = [
    "Left-Hold-Release",
    "NONE",
    "Right-Hold-Release",
    "Left-Click",
    "Left-Double-Click"
    ]
mouse_mapping = [0, 1, 2, 3, 4]

tempRight_Click = 0                                                #
tempLeft_Click = 0
Frame_Num = 0
prediction_interval = 5    

prev_gest = 1
cur_gest = 0

while True:
    Radar_model.add_frame()                             # Add Frame to frame catcher
    if gesture_active == False:                         # If a gesture isn't active skip frame
        if Frame_Num % prediction_interval == 0:
            cur_gest = mouse_mapping[Radar_model.get_prediction()]         # Check for Gesture
            print(cur_gest)
            if (cur_gest != 1):                             # If gesture detected start cooldown
                gesture_active = True
                DT_counter = 0
            
                if(prev_gest == cur_gest):
                    if cur_gest == 0:
                        tempLeft_Click = 2
                    if cur_gest == 2:
                        tempRight_Click = 2
                    prev_gest = 1
                else:
                    if cur_gest == 0:   #                             #
                        tempLeft_Click = 1
                    if cur_gest == 1:
                        True
                    if cur_gest == 2: 
                        tempRight_Click = 1
                    prev_gest = cur_gest
    else:                                               # Cooldown
        tempRight_Click = 0   #                             #
        tempLeft_Click = 0
        if(DT_counter < DownTime):
            DT_counter += 1
        else:
            gesture_active = False
    Frame_Num += 1

    if tempLeft_Click == 0:                                                    # if nothing no-op
        True                                                   #
    elif tempLeft_Click == 1:                                                    #
        mouse.press(Button.left)                               #
        print('Left_press')
    elif tempLeft_Click == 2:                                                    #
        mouse.release(Button.left)                             #
        print('left_release')
    else:                                              # Error invaild input
        print("ERROR: invalid left click input: " + str(tempLeft_Click))
        break                                                  #                                         # If right click
    if tempRight_Click == 0:                                                    # if nothing no-op
        True                                                   #
    elif tempRight_Click == 1:                                                    #
        mouse.press(Button.right)                              #
        print('right_press')
    elif tempRight_Click == 2:                                                    #                              
        mouse.release(Button.right)                            #
        print('right_release')
    else:                                              # Error invaild input
        print("ERROR: invalid right click input: " + str(tempRight_Click))
        break