import csv
import time
from gui_parser import *
from tensorflow import keras
import numpy as np
import joblib
from pynput.mouse import Button, Controller   

class gesture_recognition_model:
    def __init__(self):
        self.my_parser = UARTParser("DoubleCOMPort")
        self.my_parser.connectComPorts("COM12", "COM13")
        print("Connection Successful")
        self.feature_names = [           #Feature Names for the TI parser
            'weightedDoppler',
            'weightedPositiveDoppler',  
            'weightedNegativeDoppler',
            'weightedRange',
            'numPoints',
            'weightedAzimuthMean',
            'weightedElevationMean',
            'azimuthDopplerCorrelation',
            'weightedAzimuthDispersion',
            'weightedElevationDispersion'
        ]

        self.gesture_model = keras.models.load_model("C:/Users/snowb/Desktop/Capstone/UART Reader/Gesture_CNN6.keras") #Gesture_CNN.keras is GEN 1 | Gesture_CNN5.keras is current GEN
        self.scaler = joblib.load("C:/Users/snowb/Desktop/Capstone/UART Reader/gesture_scaler6.bin")      #gesture_scaler2.bin is GEN 1 | gesture_scaler5.bin is current GEN
        print("Loaded Model Succesfully")
        self.data_queue = []
        self.populate_data()

    def get_prediction(self):
        # Convert the collected data to a numpy array
        new_data_array = np.array(self.data_queue)

        # Ensure the data is of shape (1, 40, 10) (batch size of 1, 40 time steps, 10 features)
        new_data_array = np.expand_dims(new_data_array, axis=0)  # Shape becomes (1, 40, 10)
        
        num_features = new_data_array.shape[2] #just equal to 10, but this is better if num_features is unkown

        # Reshape for scaling: Convert (1, 40, 10) to (40, 10)
        new_data_reshaped = new_data_array.reshape(-1, num_features)  # Shape becomes (40, 10)

        # Normalize the data
        new_data_scaled = self.scaler.transform(new_data_reshaped)  # Apply scaler transformation

        # Reshape back to (1, 40, 10) to be compatible with the model
        new_data_scaled = new_data_scaled.reshape(1, 40, num_features)

        # Make predictions
        predictions = self.gesture_model.predict(new_data_scaled, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)

        # Translate id to name of Gesture
        gesture_names = ["PUSH", "NO_GESTURE", "SHINE"]
        gesture_name = gesture_names[predicted_classes[0]]
        #print(f"Predicted Gesture: {gesture_name}")
        #print(predicted_classes[0])
        return predicted_classes[0]

    def populate_data(self):
        num_frames = 0 #Used to check if the dataFrame is the right size for the model
        new_data = [] #Array to take in the data

        while num_frames < 40:
            try:
                outputData = self.my_parser.readAndParseUartDoubleCOMPort() #get frame from parser
                if not outputData: # If outputData is empty skip frame
                    continue

                keys_to_extract = ['features'] #Since outputData is a dictionary we only want the features
                trimmed_data = {key: outputData[key] for key in keys_to_extract if key in outputData} #Parse Frame for features
                if 'features' in trimmed_data:
                    feature_value = trimmed_data['features'] #Get only features without the keyname

                    # Check if feature_value is a valid list/tuple
                    if isinstance(feature_value, (list, tuple)) and len(feature_value) == len(self.feature_names):
                        new_data.append(feature_value)
                    else:
                        print(f"Feature value is not in the correct format: {feature_value}")
            except Exception as e:
                print(f"Error: {e}")
                continue

            num_frames += 1
        self.data_queue = new_data

    def add_frame(self):
        num_frames = 0 #Used to check if the dataFrame is the right size for the model
        self.data_queue.pop(0)

        while num_frames < 1:
            try:
                outputData = self.my_parser.readAndParseUartDoubleCOMPort() #get frame from parser
                if not outputData: # If outputData is empty skip frame
                    continue

                keys_to_extract = ['frameNum', 'features'] #Since outputData is a dictionary we only want the features
                trimmed_data = {key: outputData[key] for key in keys_to_extract if key in outputData} #Parse Frame for features
                if 'features' in trimmed_data:
                    feature_value = trimmed_data['features'] #Get only features without the keyname
                    # print(trimmed_data['frameNum'])
                    # Check if feature_value is a valid list/tuple
                    if isinstance(feature_value, (list, tuple)) and len(feature_value) == len(self.feature_names):
                        self.data_queue.append(feature_value)
                    else:
                        print(f"Feature value is not in the correct format: {feature_value}")
            except Exception as e:
                print(f"Error: {e}")
                continue

            num_frames += 1
    # Get prediction by passing data through the model

# ML_model = gesture_recognition_model()
# mouse = Controller()
# DownTime = 30
# DT_counter = 0
# gesture_active = False
# prev_gest = 1
# cur_gest = 1
# prediction_interval = 5
# frame_counter = 0
# while True:
#     ML_model.add_frame()                             # Add Frame to frame catcher
#     if gesture_active == False:                      # If a gesture isn't active skip frame
#         if frame_counter % prediction_interval == 0:
#             cur_gest = ML_model.get_prediction()         # Check for Gesture
#             print(cur_gest)
#             if (cur_gest != 1):                             # If gesture detected start cooldown
#                 gesture_active = True
#                 DT_counter = 0
#
#                 if(prev_gest == cur_gest):
#                     if cur_gest == 0:
#                         mouse.release(Button.left)
#                     if cur_gest == 2:
#                         mouse.release(Button.right)
#                     prev_gest = 1
#                 else:
#                     if cur_gest == 0:   #                             #
#                         mouse.press(Button.left)
#                     elif cur_gest == 1:
#                         True
#                     elif cur_gest == 2:
#                         mouse.press(Button.right)
#                     prev_gest = cur_gest
#     else:                                               # Cooldown
#         tempRight_Click = 0   #                             #
#         tempLeft_Click = 0
#         if(DT_counter < DownTime):
#             DT_counter += 1
#         else:
#             gesture_active = False
#     frame_counter += 1