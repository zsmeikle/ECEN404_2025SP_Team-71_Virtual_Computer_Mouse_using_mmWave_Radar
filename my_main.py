import csv
import time
from gui_parser import *
from keras.models import load_model
import pandas as pd
import numpy as np
import joblib
from capstone_gui import Capstone_Demo as CapDemo
class gesture_recognition_model:
    def __init__(self):
        self.my_parser = UARTParser("DoubleCOMPort")
        self.my_parser.connectComPorts("COM4", "COM3")

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

        self.gesture_model = load_model("C:/Users/lostk/OneDrive/Documents/A_M/Capstone/Gesture_CNN4.keras") #Gesture_CNN.keras is GEN 1 | Gesture_CNN5.keras is current GEN
        self.scaler = joblib.load("C:/Users/lostk/OneDrive/Documents/A_M/Capstone/gesture_scaler4.bin")      #gesture_scaler2.bin is GEN 1 | gesture_scaler5.bin is current GEN
        print("Loaded Model Succesfully")

    def get_prediction(self):
        # Load new data
        new_data_files = ['C:/Users/lostk/OneDrive/Documents/A_M/Capstone/radar_toolbox_2_20_00_05/gesture_validation1.csv']
        new_data_list = []

        for file in new_data_files:
            sample = pd.read_csv(file)
            new_data_list.append(sample.values)  # Skip header

        new_data = np.array(new_data_list)
        num_features = new_data.shape[2]  # Adjust this if needed

        # Reshape
        new_data = new_data.reshape((-1, 40, num_features))

        # Normalize
        new_data_reshaped = new_data.reshape(-1, num_features)
        new_data_scaled = self.scaler.transform(new_data_reshaped).reshape(new_data.shape)

        # Make predictions
        predictions = self.gesture_model.predict(new_data_scaled, verbose = 0)
        predicted_classes = np.argmax(predictions, axis=1)

        #Translate id to name of Gesture
        gesture_name = ""
        if predicted_classes[0] == 0:
            gesture_name = "PUSH"
        elif predicted_classes[0] == 1:
            gesture_name = "NO_GESTURE"
        else:
            gesture_name = "SHINE"
        # Output the predictions
        print("Predicted classes: ", gesture_name)
        


    def run_model(self):
        while True:
            Filename = "gesture_validation"
            filetype = ".csv"
            filenum = 1
            fullFileName = "{}{}{}".format(Filename, filenum, filetype)
            #Make file for current prediction
            with open(fullFileName, mode="w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write a header for features 1 to 10
                csv_writer.writerow(self.feature_names)  # Adjust based on your actual feature count

                #start_time = time.time_ns()
                print("Running:")
                numFrames = 0
                while numFrames < 40:
                    try:
                        outputData = self.my_parser.readAndParseUartDoubleCOMPort()
                        if(not bool(outputData)):
                            continue
                        keys_to_extract = ['features']
                        trimmed_data = {key: outputData[key] for key in keys_to_extract if key in outputData}

                        if 'features' in trimmed_data:
                            feature_value = trimmed_data['features']

                            # Ensure feature_value is a list/tuple of the correct length
                            if isinstance(feature_value, (list, tuple)):
                                csv_writer.writerow(feature_value)  # Write the values to CSV
                            else:
                                print("Feature value is not a list/tuple of length 10")

                    except Exception as e:
                        print(f"Error: {e}")  # Print any errors for debugging
                        continue
                    numFrames = numFrames + 1
            #Load file to model and make prediction
            self.get_prediction()


Gesuture_model = gesture_recognition_model()
Gesuture_model.run_model()
    
    
    

