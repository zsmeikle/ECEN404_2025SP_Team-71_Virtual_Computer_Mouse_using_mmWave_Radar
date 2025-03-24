# import tkinter as tk
# from tkinter import ttk
# import threading
# import time
# import random
#
# # Global variables that other threads/functions can access
# XScale = 10
# YScale = 10
# mouse_smoothing = "Algorithm 1"
# Reverse_X = 1  # Unchecked = -1 (reverse), Checked = 1 (normal)
# Reverse_Y = 1  # Unchecked = -1 (reverse), Checked = 1 (normal)
# Switch_XY = 0   # Unchecked = 0 (no switch), Checked = 1 (switch)
# generated_frames_on = 0  # Unchecked = 0 (off), Checked = 1 (on)
# generated_frames = 1     # Default value, range 1 to 20
#
# # Custom color scheme
# BG_COLOR = "#f0f0f0"
# BUTTON_COLOR = "#4a7a8c"
# TEXT_BG = "#2e2e2e"
# TEXT_FG = "#00ff00"
#
# li = ['1', '2', '3']
# x = 1
#
# def read_radar_data():
#     """Simulate or continuously read radar data."""
#     while True:
#         if x == 1:
#             update_terminal(li)
#         time.sleep(1)
#         # print(XScale)
#         # print(YScale)
#         # print(mouse_smoothing)
#
# def update_terminal(data):
#     """Update the terminal tab with radar data."""
#     terminal_text.configure(state='normal')
#     for entry in data:
#         formatted_entry = " ".join(map(str, entry)) + "\n"
#         terminal_text.insert(tk.END, formatted_entry)
#     terminal_text.insert(tk.END, "\n")
#     terminal_text.configure(state='disabled')
#     terminal_text.see(tk.END)
#
# def start_radar_thread():
#     """Start a thread for radar data reading."""
#     radar_thread = threading.Thread(target=read_radar_data, daemon=True)
#     radar_thread.start()
#
# def apply_settings():
#     """Retrieve values from the settings inputs and update globals."""
#     global XScale, YScale, mouse_smoothing, Reverse_X, Reverse_Y, Switch_XY, generated_frames_on, generated_frames
#     XScale = sensitivity_x_var.get()
#     YScale = sensitivity_y_var.get()
#     mouse_smoothing = smoothing_var.get()
#     Reverse_X = Reverse_X_var.get()
#     Reverse_Y = Reverse_Y_var.get()
#     Switch_XY = Switch_XY_var.get()
#     generated_frames_on = generated_frames_on_var.get()
#     generated_frames = generated_frames_var.get()
#     print("Updated Settings:")
#     print("Sensitivity X:", XScale)
#     print("Sensitivity Y:", YScale)
#     print("Mouse Smoothing:", mouse_smoothing)
#     print("Reverse X:", Reverse_X)
#     print("Reverse Y:", Reverse_Y)
#     print("Switch X and Y:", Switch_XY)
#     print("Generated Frames ON/OFF:", generated_frames_on)
#     print("Number of Generated Frames:", generated_frames)
#
# # Create the main Tkinter window
# root = tk.Tk()
# root.title("Radar GUI")
# root.geometry("800x600")
# root.configure(bg=BG_COLOR)
#
# # Set window icon (replace 'radar_icon.ico' with your actual icon file)
# try:
#     root.iconbitmap('TI_Logo.ico')
# except Exception as e:
#     print("Icon not found:", e)
#
# # Style configuration
# style = ttk.Style()
# style.theme_use('clam')
# style.configure('TNotebook', background=BG_COLOR)
# style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'))
# style.configure('TFrame', background=BG_COLOR)
# style.configure('TButton', background=BUTTON_COLOR, foreground='white',
#                 font=('Helvetica', 10, 'bold'), borderwidth=1)
# style.map('TButton', background=[('active', BUTTON_COLOR), ('pressed', '#3a6a7c')])
#
# # Create notebook (tabs)
# notebook = ttk.Notebook(root)
# notebook.pack(fill='both', expand=True)
#
# # Terminal Tab
# terminal_frame = ttk.Frame(notebook)
# notebook.add(terminal_frame, text="Terminal")
#
# terminal_text = tk.Text(terminal_frame, wrap='word', state='disabled',
#                         height=30, width=80, bg=TEXT_BG, fg=TEXT_FG,
#                         insertbackground=TEXT_FG, font=('Consolas', 10))
# terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#
# terminal_scroll = ttk.Scrollbar(terminal_frame, command=terminal_text.yview)
# terminal_scroll.pack(side=tk.RIGHT, fill=tk.Y)
# terminal_text['yscrollcommand'] = terminal_scroll.set
#
# # Settings Tab
# settings_frame = ttk.Frame(notebook)
# notebook.add(settings_frame, text="Settings")
#
# # Settings content container
# settings_container = ttk.Frame(settings_frame)
# settings_container.pack(padx=20, pady=20, fill='both', expand=True)
#
# # Title
# ttk.Label(settings_container, text="Control Settings",
#          font=('Helvetica', 16, 'bold'), background=BG_COLOR).grid(row=0, column=0, pady=10, columnspan=3)
#
# # Tkinter variables
# sensitivity_x_var = tk.IntVar(value=XScale)
# sensitivity_y_var = tk.IntVar(value=YScale)
# smoothing_var = tk.StringVar(value=mouse_smoothing)
# Reverse_X_var = tk.IntVar(value=Reverse_X)
# Reverse_Y_var = tk.IntVar(value=Reverse_Y)
# Switch_XY_var = tk.IntVar(value=Switch_XY)
# generated_frames_on_var = tk.IntVar(value=generated_frames_on)
# generated_frames_var = tk.IntVar(value=generated_frames)
#
# # Sensitivity X
# ttk.Label(settings_container, text="Horizontal Sensitivity:",
#          font=('Helvetica', 11)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
# x_spin = ttk.Spinbox(settings_container, from_=0, to=100, textvariable=sensitivity_x_var,
#                     width=10, font=('Helvetica', 11))
# x_spin.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
#
# # Sensitivity Y
# ttk.Label(settings_container, text="Vertical Sensitivity:",
#          font=('Helvetica', 11)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
# y_spin = ttk.Spinbox(settings_container, from_=0, to=100, textvariable=sensitivity_y_var,
#                     width=10, font=('Helvetica', 11))
# y_spin.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
#
# # Algorithm selectionf
# ttk.Label(settings_container, text="Smoothing Algorithm:",
#          font=('Helvetica', 11)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
# smoothing_options = ["None", "Algorithm 1", "Algorithm 2", "Advanced Filter"]
# smoothing_drop = ttk.Combobox(settings_container, values=smoothing_options,
#                              textvariable=smoothing_var, state="readonly",
#                              font=('Helvetica', 11), width=18)
# smoothing_drop.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
#
# # Reverse X
# ttk.Label(settings_container, text="Reverse X:", font=('Helvetica', 11)).grid(row=4, column=0, padx=10, pady=5, sticky='w')
# Reverse_X_check = ttk.Checkbutton(settings_container, variable=Reverse_X_var, onvalue=-1, offvalue=1)
# Reverse_X_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')
#
# # Reverse Y
# ttk.Label(settings_container, text="Reverse Y:", font=('Helvetica', 11)).grid(row=5, column=0, padx=10, pady=5, sticky='w')
# Reverse_Y_check = ttk.Checkbutton(settings_container, variable=Reverse_Y_var, onvalue=-1, offvalue=1)
# Reverse_Y_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')
#
# # Switch X and Y
# ttk.Label(settings_container, text="Switch X and Y:", font=('Helvetica', 11)).grid(row=6, column=0, padx=10, pady=5, sticky='w')
# Switch_XY_check = ttk.Checkbutton(settings_container, variable=Switch_XY_var, onvalue=1, offvalue=0)
# Switch_XY_check.grid(row=6, column=1, padx=10, pady=5, sticky='w')
#
# # Generated Frames ON/OFF
# ttk.Label(settings_container, text="Generated Frames ON/OFF:", font=('Helvetica', 11)).grid(row=7, column=0, padx=10, pady=5, sticky='w')
# generated_frames_on_check = ttk.Checkbutton(settings_container, variable=generated_frames_on_var, onvalue=1, offvalue=0)
# generated_frames_on_check.grid(row=7, column=1, padx=10, pady=5, sticky='w')
#
# ttk.Label(settings_container, text="Number of Generated Frames:", font=('Helvetica', 11)).grid(row=8, column=0, padx=10, pady=5, sticky='w')
# generated_frames_scale = tk.Scale(settings_container, from_=1, to=20, variable=generated_frames_var, orient='horizontal', length=200, resolution=1, showvalue=0, bg=BG_COLOR, activebackground=BUTTON_COLOR, troughcolor='#d9d9d9')
# generated_frames_scale.grid(row=8, column=1, padx=10, pady=5, sticky='ew')
# generated_frames_value_label = ttk.Label(settings_container, textvariable=generated_frames_var, font=('Helvetica', 11))
# generated_frames_value_label.grid(row=8, column=2, padx=10, pady=5, sticky='w')
#
# # # Generated Frames Slider
# # ttk.Label(settings_container, text="Number of Generated Frames:", font=('Helvetica', 11)).grid(row=8, column=0, padx=10, pady=5, sticky='w')
# # generated_frames_scale = ttk.Scale(settings_container, from_=1, to=20, variable=generated_frames_var, orient='horizontal', length=200)
# # generated_frames_scale.grid(row=8, column=1, padx=10, pady=5, sticky='ew')
# # generated_frames_value_label = ttk.Label(settings_container, textvariable=generated_frames_var, font=('Helvetica', 11))
# # generated_frames_value_label.grid(row=8, column=2, padx=10, pady=5, sticky='w')
#
# # Function to enable/disable the slider based on the checkbox state
# def update_generated_frames_state(*args):
#     if generated_frames_on_var.get() == 1:
#         generated_frames_scale.configure(state='normal')
#     else:
#         generated_frames_scale.configure(state='disabled')
#
# # Bind the function to the checkbox variable and set initial state
# generated_frames_on_var.trace('w', update_generated_frames_state)
# update_generated_frames_state()
#
# # Separator
# ttk.Separator(settings_container, orient='horizontal').grid(row=9, column=0, columnspan=3, pady=20, sticky='ew')
#
# # Apply button
# apply_btn = ttk.Button(settings_container, text="Apply Configuration",
#                       command=apply_settings, style='TButton')
# apply_btn.grid(row=10, column=0, columnspan=3, pady=10, ipadx=20, ipady=5)
#
# # Configure grid columns
# settings_container.columnconfigure(0, weight=1)
# settings_container.columnconfigure(1, weight=1)
# settings_container.columnconfigure(2, weight=0)
#
# # Start radar thread
# start_radar_thread()
#
# # Start the Tkinter main loop
# root.mainloop()

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

# Global variables that other threads/functions can access
XScale = 10
YScale = 10
mouse_smoothing = "Algorithm 1"
Reverse_X = 1   # Unchecked = -1 (reverse), Checked = 1 (normal)
Reverse_Y = 1   # Unchecked = -1 (reverse), Checked = 1 (normal)
Switch_XY = 0   # Unchecked = 0 (no switch), Checked = 1 (switch)
generated_frames_on = 0  # Unchecked = 0 (off), Checked = 1 (on)
generated_frames = 1     # Default value, range 1 to 20

# Custom color scheme
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_BG = "#2e2e2e"
TEXT_FG = "#00ff00"

def apply_settings():
    """Retrieve values from the settings inputs and update globals."""
    global XScale, YScale, mouse_smoothing
    global Reverse_X, Reverse_Y, Switch_XY, generated_frames_on, generated_frames
    XScale = sensitivity_x_var.get()
    YScale = sensitivity_y_var.get()
    mouse_smoothing = smoothing_var.get()
    Reverse_X = Reverse_X_var.get()
    Reverse_Y = Reverse_Y_var.get()
    Switch_XY = Switch_XY_var.get()
    generated_frames_on = generated_frames_on_var.get()
    generated_frames = generated_frames_var.get()
    print("Updated Settings:")
    print("Sensitivity X:", XScale)
    print("Sensitivity Y:", YScale)
    print("Mouse Smoothing:", mouse_smoothing)
    print("Reverse X:", Reverse_X)
    print("Reverse Y:", Reverse_Y)
    print("Switch X and Y:", Switch_XY)
    print("Generated Frames ON/OFF:", generated_frames_on)
    print("Number of Generated Frames:", generated_frames)


def radar_loop():
    while True:
        # Example radar processing that uses the current settings
        print("Radar using settings -> Sensitivity X:", XScale,
              "Sensitivity Y:", YScale)
        # Add your radar code logic here
        time.sleep(1)  # Adjust as needed for your application

# Start the radar thread
radar_thread = threading.Thread(target=radar_loop, daemon=True)
radar_thread.start()


# Create the main Tkinter window
root = tk.Tk()
root.title("Virtual Mouse")
root.geometry("500x450")
root.configure(bg=BG_COLOR)

# Set window icon (optional)
try:
    root.iconbitmap('TI_Logo.ico')
except Exception as e:
    print("Icon not found:", e)

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=BG_COLOR)
style.configure('TButton', background=BUTTON_COLOR, foreground='white',
                font=('Helvetica', 10, 'bold'), borderwidth=1)
style.map('TButton', background=[('active', BUTTON_COLOR), ('pressed', '#3a6a7c')])

# Create only the Settings frame (no Notebook since there's just one tab)
settings_frame = ttk.Frame(root)
settings_frame.pack(padx=20, pady=20, fill='both', expand=True)

# Title
ttk.Label(settings_frame, text="Virtual Mouse Settings",
          font=('Helvetica', 16, 'bold'), background=BG_COLOR)\
          .grid(row=0, column=0, pady=10, columnspan=3)

# Tkinter variables for settings
sensitivity_x_var = tk.IntVar(value=XScale)
sensitivity_y_var = tk.IntVar(value=YScale)
smoothing_var = tk.StringVar(value=mouse_smoothing)
Reverse_X_var = tk.IntVar(value=Reverse_X)
Reverse_Y_var = tk.IntVar(value=Reverse_Y)
Switch_XY_var = tk.IntVar(value=Switch_XY)
generated_frames_on_var = tk.IntVar(value=generated_frames_on)
generated_frames_var = tk.IntVar(value=generated_frames)

# Sensitivity X
ttk.Label(settings_frame, text="Horizontal Sensitivity:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=1, column=0, padx=10, pady=5, sticky='w')
x_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
                     textvariable=sensitivity_x_var,
                     width=10, font=('Helvetica', 11))
x_spin.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

# Sensitivity Y
ttk.Label(settings_frame, text="Vertical Sensitivity:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=2, column=0, padx=10, pady=5, sticky='w')
y_spin = ttk.Spinbox(settings_frame, from_=0, to=100,
                     textvariable=sensitivity_y_var,
                     width=10, font=('Helvetica', 11))
y_spin.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

# Smoothing Algorithm selection
ttk.Label(settings_frame, text="Smoothing Algorithm:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=3, column=0, padx=10, pady=5, sticky='w')
smoothing_options = ["None", "Algorithm 1", "Algorithm 2", "Advanced Filter"]
smoothing_drop = ttk.Combobox(settings_frame, values=smoothing_options,
                              textvariable=smoothing_var, state="readonly",
                              font=('Helvetica', 11), width=18)
smoothing_drop.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

# Reverse X
ttk.Label(settings_frame, text="Reverse X:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=4, column=0, padx=10, pady=5, sticky='w')
Reverse_X_check = ttk.Checkbutton(settings_frame,
                                  variable=Reverse_X_var,
                                  onvalue=-1, offvalue=1)
Reverse_X_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')

# Reverse Y
ttk.Label(settings_frame, text="Reverse Y:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=5, column=0, padx=10, pady=5, sticky='w')
Reverse_Y_check = ttk.Checkbutton(settings_frame,
                                  variable=Reverse_Y_var,
                                  onvalue=-1, offvalue=1)
Reverse_Y_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')

# Switch X and Y
ttk.Label(settings_frame, text="Switch X and Y:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=6, column=0, padx=10, pady=5, sticky='w')
Switch_XY_check = ttk.Checkbutton(settings_frame,
                                  variable=Switch_XY_var,
                                  onvalue=1, offvalue=0)
Switch_XY_check.grid(row=6, column=1, padx=10, pady=5, sticky='w')

# Generated Frames ON/OFF
ttk.Label(settings_frame, text="Generated Frames:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=7, column=0, padx=10, pady=5, sticky='w')
generated_frames_on_check = ttk.Checkbutton(settings_frame,
                                            variable=generated_frames_on_var,
                                            onvalue=1, offvalue=0)
generated_frames_on_check.grid(row=7, column=1, padx=10, pady=5, sticky='w')

ttk.Label(settings_frame, text="Number of Generated Frames:",
          font=('Helvetica', 11), background=BG_COLOR)\
          .grid(row=8, column=0, padx=10, pady=5, sticky='w')
generated_frames_scale = tk.Scale(settings_frame, from_=1, to=20,
                                  variable=generated_frames_var,
                                  orient='horizontal', length=200, resolution=1,
                                  showvalue=0, bg=BG_COLOR,
                                  activebackground=BUTTON_COLOR,
                                  troughcolor='#d9d9d9')
generated_frames_scale.grid(row=8, column=1, padx=10, pady=5, sticky='ew')
generated_frames_value_label = ttk.Label(settings_frame,
                                         textvariable=generated_frames_var,
                                         font=('Helvetica', 11),
                                         background=BG_COLOR)
generated_frames_value_label.grid(row=8, column=2, padx=10, pady=5, sticky='w')

# Enable/disable the slider based on the checkbox state
def update_generated_frames_state(*args):
    if generated_frames_on_var.get() == 1:
        generated_frames_scale.configure(state='normal')
    else:
        generated_frames_scale.configure(state='disabled')

generated_frames_on_var.trace('w', update_generated_frames_state)
update_generated_frames_state()

# Separator
ttk.Separator(settings_frame, orient='horizontal')\
    .grid(row=9, column=0, columnspan=3, pady=20, sticky='ew')

# Apply button
apply_btn = ttk.Button(settings_frame, text="Apply Configuration",
                       command=apply_settings, style='TButton')
apply_btn.grid(row=10, column=0, columnspan=3, pady=10, ipadx=20, ipady=5)

# Configure grid columns for proper spacing
settings_frame.columnconfigure(0, weight=1)
settings_frame.columnconfigure(1, weight=1)
settings_frame.columnconfigure(2, weight=0)

root.mainloop()
