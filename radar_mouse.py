import threading
import subprocess
import os

# Function to run a Python script
python_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
def run_script(script_name):
    subprocess.run([python_path, script_name])

# Create threads to run mouse_mov.py and mouse_actions.py
thread1 = threading.Thread(target=run_script, args=('tools/visualizers/Applications_Visualizer/common/mouse_mov.py',))
thread2 = threading.Thread(target=run_script, args=('tools/visualizers/Applications_Visualizer/common/mouse_actions.py',))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both scripts have finished executing.")