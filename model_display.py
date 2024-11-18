import numpy as np
import joblib
from keras.models import load_model
import tkinter as tk
from tkinter import Label
from gui_parser import UARTParser

class GestureRecognitionModel:
    def __init__(self):
        self.my_parser = UARTParser("DoubleCOMPort")
        self.my_parser.connectComPorts("COM4", "COM3")

        self.feature_names = [
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

        self.gesture_model = load_model("C:/Users/lostk/OneDrive/Documents/A_M/Capstone/Gesture_CNN4.keras")
        self.scaler = joblib.load("C:/Users/lostk/OneDrive/Documents/A_M/Capstone/gesture_scaler4.bin")
        print("Loaded Model Successfully")

        # Tkinter window setup
        self.root = tk.Tk()
        self.root.title("Gesture Recognition")
        self.root.attributes('-fullscreen', True)

        self.prediction_label = Label(self.root, text="Predicted Gesture: ", font=("Helvetica", 64))
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.prediction_label.pack(pady=350)

        # Start Tkinter event loop in a separate thread
        self.root.after(100, self.run_model)

    def toggle_fullscreen(self, event=None):
        current_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_fullscreen)
    def get_prediction(self, new_data):
        num_features = new_data.shape[2]

        # Reshape for scaling: Convert (1, 40, 10) to (40, 10)
        new_data_reshaped = new_data.reshape(-1, num_features)  # Shape becomes (40, 10)

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
        print(f"Predicted Gesture: {gesture_name}")

        # Update Tkinter label with the predicted gesture
        self.prediction_label.config(text=f"Predicted Gesture: {gesture_name}")
        self.root.update()  # Update the Tkinter window

    def run_model(self):
        num_frames = 0
        new_data = []

        while num_frames < 40:
            try:
                outputData = self.my_parser.readAndParseUartDoubleCOMPort()
                if not outputData:
                    continue

                keys_to_extract = ['features']
                trimmed_data = {key: outputData[key] for key in keys_to_extract if key in outputData}

                if 'features' in trimmed_data:
                    feature_value = trimmed_data['features']

                    # Check if feature_value is a valid list/tuple
                    if isinstance(feature_value, (list, tuple)) and len(feature_value) == len(self.feature_names):
                        new_data.append(feature_value)
                    else:
                        print(f"Feature value is not in the correct format: {feature_value}")
            except Exception as e:
                print(f"Error: {e}")
                continue

            num_frames += 1

        # Convert the collected data to a numpy array
        new_data_array = np.array(new_data)

        # Ensure the data is of shape (1, 40, 10) (batch size of 1, 40 time steps, 10 features)
        new_data_array = np.expand_dims(new_data_array, axis=0)  # Shape becomes (1, 40, 10)

        # Get prediction by passing data through the model
        self.get_prediction(new_data_array)

        # Re-run the model for continuous prediction
        self.root.after(10, self.run_model)  # Schedule the next model run

# Instantiate and start the Tkinter window with gesture recognition model
gesture_model = GestureRecognitionModel()
gesture_model.root.mainloop()  # Start Tkinter's main event loop
