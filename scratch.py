import tkinter as tk
from tkinter import ttk
import threading
import time
from gui_parser import *

my_parser = UARTParser("DoubleCOMPort") #Defining Pointer Parser from class UARTParser
my_parser.connectComPorts("COM11", "COM10") #Device-Manager defined Ports

def read_radar_data():
    """Simulate or continuously read radar data."""
    while True:  # Infinite loop for radar data
        while (1):  # Radars connected and running, always true until not - Implement GUI?
            try:
                pointer_Data = my_parser.readAndParseUartDoubleCOMPort()  # Parsing Pointer radar data
                #gesture_Data = my_parser2.readAndParseUartDoubleCOMPort()  # Parsing Gesture radar data

                keys_Pointer = ['frameNum', 'pointCloud',
                                'numDetectedPoints']  # Only required fields needed for Pointer Position
                trimmed_Pointer = {key: pointer_Data[key] for key in
                                   keys_Pointer}  # Trimming pointer_Data for keys_Pointer
                #key_Gesture = ['features']  # Only required field needed for Gesture
                #trimmed_Gesture = {key: gesture_Data[key] for key in
                #                   key_Gesture}  # Trimming gesture_Data for key_Gesture
                pointer_numPoints = int(trimmed_Pointer['numDetectedPoints'])  # Pullihg Pointer number of Points
                pointer_frameNum = int(
                    trimmed_Pointer['frameNum'])  # Pulling Frame number for time-based reference, e.g. 20 FPS
                pointCloudArray = []  # Blank Array to store pointCloud info
                for i in range(pointer_numPoints):  # Iterates through total number of points detected
                    pointCloudArray.append(
                        trimmed_Pointer['pointCloud'][i][0:3])  # Pulling X, Y, Z values per point detected
                print("Pointer Data")
                print(pointer_numPoints, "|", pointer_frameNum)  # Outputting points, frame number per frame
                for i in pointCloudArray:  # Iterating and outputting each point (X, Y, Z)
                    print(i)
                print()
                #print("Gesture Data")
                #print(trimmed_Gesture, '\n')  # Outputting feature data
                update_terminal(pointCloudArray)
            except:
                continue


def update_terminal(data):
    """Update the terminal tab with radar data."""
    terminal_text.configure(state='normal')  # Enable editing the widget temporarily

    for entry in data:
        # Join the elements in the list into a string, separate each by space, then add a newline
        formatted_entry = " ".join(map(str, entry)) + "\n"
        terminal_text.insert(tk.END, formatted_entry)

    terminal_text.insert(tk.END, "\n")  # Add an extra newline to separate batches of updates
    terminal_text.configure(state='disabled')  # Prevent user editing
    terminal_text.see(tk.END)  # Auto-scroll to the latest entry
    # terminal_text.configure(state='normal')
    # terminal_text.insert(tk.END, data)
    # terminal_text.configure(state='disabled')
    # terminal_text.see(tk.END)

def start_radar_thread():
    """Start a thread for radar data reading."""
    radar_thread = threading.Thread(target=read_radar_data, daemon=True)
    radar_thread.start()

# Create the main Tkinter window
root = tk.Tk()
root.title("Radar GUI")
root.geometry("800x600")

# Create a notebook (tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Terminal Tab
terminal_frame = ttk.Frame(notebook)
notebook.add(terminal_frame, text="Terminal")

terminal_text = tk.Text(terminal_frame, wrap='word', state='disabled', height=30, width=80)
terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar
terminal_scroll = ttk.Scrollbar(terminal_frame, command=terminal_text.yview)
terminal_scroll.pack(side=tk.RIGHT, fill=tk.Y)
terminal_text['yscrollcommand'] = terminal_scroll.set

# Settings Tab
settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text="Settings")

tk.Label(settings_frame, text="Settings Placeholder", font=('Arial', 14)).pack(pady=20)

# Start radar thread
start_radar_thread()

# Start the Tkinter main loop
root.mainloop()

import math
import statistics

list1 = [[-6, 0, 1], [-4, 2, 1], [-2, 0, 1], [-4, -2, 1]]
list2 = [[-2, 4, 1], [0, 6, 1], [2, 4, 1], [0, 2, 1], [3, 3, 3]]
num_points_1 = 4
num_points_2 = 5


def get_pos(num_points_1, num_points_2, list1, list2):
    # the output data from chirp configuration demo in the first frame
    # num_points = 4 # The chirp configuration demo will output the number of points detected
    # points = np.array([[-6, 0, 1],[-4, 2, 1],[-2, 0, 1],[-4, -2, 1]]) # The chirp configuration demo will output the coordinates of the points

    # the output data from chirp configuration demo in the second frame
    # num_points_2 = 5 # The chirp configuration demo will output the number of points detected
    # points_2 = np.array([[-2, 4, 1],[0, 6, 1],[2, 4, 1],[0, 2, 1],[3, 3, 3]]) # The chirp configuration demo will output the coordinates of the points
    x = 0  # variable for x coordinates in the first frame
    y = 0  # variable for y coordinates in the first frame
    x_2 = 0  # variable for x coordinates in the second frame
    y_2 = 0  # variable for y coordinates in the second frame

    # average position of the first frame
    for i in range(num_points_1):  # loop for average position of the first frame
        if list1[i][2] < 2:  # select the points with the correct distance z
            x += list1[i][0]  # calculate the sum of the magnitude of x coordinates
            y += list1[i][1]  # calculate the sum of the magnitude of y coordinates
            average_x = x / num_points_1  # calculate the average coordinate of x axis
            average_y = y / num_points_1  # calculate the average coordinate of y axis
        else:  # else
            num_points_1 -= 1  # count the removed points
            average_x = x / num_points_1  # calculate the average coordinate of x axis
            average_y = y / num_points_1  # calculate the average coordinate of y axis
    print(average_x)  # output check
    print(average_y)  # output check

    # average position of the second frame
    for i in range(num_points_2):  # loop for average position of the second frame
        if list2[i][2] < 2:  # select the points with the correct distance z
            x_2 += list2[i][0]  # calculate the sum of the magnitude of x coordinates
            y_2 += list2[i][1]  # calculate the sum of the magnitude of y coordinates
            average_x_2 = x_2 / num_points_2  # calculate the average coordinate of x axis
            average_y_2 = y_2 / num_points_2  # calculate the average coordinate of y axis
        else:  # else
            num_points_2 -= 1  # count the removed points
            average_x_2 = x_2 / num_points_2  # calculate the average coordinate of x axis
            average_y_2 = y_2 / num_points_2  # calculate the average coordinate of y axis

    # use average positions to output moving path
    output_v_x = (average_x_2 - average_x)  # calculate the velocity in x direction
    output_v_y = (average_y_2 - average_y)  # calculate the velocity in y direction

    # velocity in z-direction is not required because the user is required to move his hand in parallel to the radar's x-y plane
    print("V_x euqals to ", output_v_x)  # velocity check
    print("V_y euqals to ", output_v_y)  # velocity check
    return [output_v_x, output_v_y]


get_pos(num_points_1, num_points_2, list1, list2)