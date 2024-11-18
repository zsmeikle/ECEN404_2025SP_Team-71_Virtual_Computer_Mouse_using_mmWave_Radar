import csv
import time
from gui_parser import *

my_parser = UARTParser("DoubleCOMPort")
my_parser.connectComPorts("COM4", "COM3")

feature_names = [
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

def make_training_files(fileNumStart, fileNumStop):
    Filename = "C:/Users/lostk/OneDrive/Documents/A_M/Capstone/training_data/gesture_training"
    filetype = ".csv"
    for i in range(fileNumStart, fileNumStop+1):
        filenum = i
        fullFileName = "{}{}{}".format(Filename, filenum, filetype)
        with open(fullFileName, mode="w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write a header for features 1 to 10
            csv_writer.writerow(feature_names)  # Adjust based on your actual feature count

            #start_time = time.time_ns()
            print("Running:")
            numFrames = 0
            start_time = time.time_ns()
            while numFrames < 40:
                try:
                    outputData = my_parser.readAndParseUartDoubleCOMPort()
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
            end_time = time.time_ns()
            print((end_time-start_time)/10**9)

make_training_files(470, 479)
