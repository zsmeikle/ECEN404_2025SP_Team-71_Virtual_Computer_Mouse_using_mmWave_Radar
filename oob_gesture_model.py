import time
from gui_parser import *
from tensorflow import keras
import numpy as np
from radar_filter import simple_avg
import joblib
from pathlib import Path

class gesture_recognition_model:
    def __init__(self, model_path, scaler_path):
        self.frames = 30
        self.gesture_model = keras.models.load_model(model_path) #Gesture_CNN.keras is GEN 1 | Gesture_CNN5.keras is current GEN
        self.scaler = joblib.load(scaler_path)      #gesture_scaler2.bin is GEN 1 | gesture_scaler5.bin is current GEN
        print("Loaded Model Succesfully")
        self.data_queue = []
        self.gesture_names = ["NO_GESTURE", "PUSH", "SHINE", "TURN_LEFT", "TURN_RIGHT"]

    def fill_data(self, gestureData):
        if(len(gestureData) == self.frames):
            self.data_queue = gestureData
        else:
            raise ValueError("Queue size does not match")
    
    def fill_frame(self, numPoints, pointCloud):
        features = []
        if numPoints == 0:
            features = [0, 0, 0, 0, 0]
        else:
            x_pos = simple_avg([point[0] for point in pointCloud])
            y_pos = simple_avg([point[1] for point in pointCloud])
            z_pos = simple_avg([point[2] for point in pointCloud])
            doppler = simple_avg([point[3] for point in pointCloud])
            features = [x_pos, y_pos, z_pos, doppler, numPoints]
        self.data_queue.append(features)

    def add_frame(self, numPoints, pointCloud):
        self.fill_frame(numPoints, pointCloud)
        self.data_queue.pop(0)


    def get_prediction(self, data_queue=[]):
        # Convert the collected data to a numpy array
        if not(data_queue): data_queue = self.data_queue
        new_data_array = np.array(data_queue)
        
        num_features = new_data_array.shape[1] #just equal to 5, but this is better if num_features is unkown

        # Normalize the data
        new_data_scaled = self.scaler.transform(new_data_array)  # Apply scaler transformation

        # Reshape back to (1, 40, 10) to be compatible with the model
        new_data_scaled = new_data_scaled.reshape(1, self.frames, num_features)

        # Make predictions
        predictions = self.gesture_model.predict(new_data_scaled, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)

        # Translate id to name of Gesture

        gesture_name = self.gesture_names[predicted_classes[0]]

        return predicted_classes[0]
    