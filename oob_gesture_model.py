import time
from gui_parser import *
from tensorflow import keras
import numpy as np

import joblib
from pynput.mouse import Button, Controller   

class gesture_recognition_model:
    def __init__(self):
        self.gesture_model = keras.models.load_model("C:/Users/lostk/Documents/A_M/Capstone/New_Gesture_CNN2.keras") #Gesture_CNN.keras is GEN 1 | Gesture_CNN5.keras is current GEN
        self.scaler = joblib.load("C:/Users/lostk/Documents/A_M/Capstone/new_gesture_scaler2.bin")      #gesture_scaler2.bin is GEN 1 | gesture_scaler5.bin is current GEN
        print("Loaded Model Succesfully")


    def get_prediction(self, gestureData):
        # Convert the collected data to a numpy array
        new_data_array = np.array(gestureData)
        
        num_features = new_data_array.shape[1] #just equal to 5, but this is better if num_features is unkown

        # Normalize the data
        new_data_scaled = self.scaler.transform(new_data_array)  # Apply scaler transformation

        # Reshape back to (1, 40, 10) to be compatible with the model
        new_data_scaled = new_data_scaled.reshape(1, 20, num_features)

        # Make predictions
        predictions = self.gesture_model.predict(new_data_scaled, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)

        # Translate id to name of Gesture
        gesture_names = ["NO_GESTURE", "PUSH", "SHINE", "TURN_LEFT", "TURN_RIGHT"]
        gesture_name = gesture_names[predicted_classes[0]]

        return predicted_classes[0]