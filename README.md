Please extract EEG_Measurements.zip to root directory.

ModelGenerating.py:
Generate the model for prediction, based on data in EEG_measurements that are related to Spanish or English. The model will be stored in 'Spanish Data' folder and 'Non-Spanish Data' folder.

Prediction.py:
Making prediction about input participant's proficiency of Spanish. Input participant's EEG data should be provided in 'input' folder, in form of csv files. File names and data should be provided in the same format as data in EEG_measurements. Note that the model have a tiny probability of being not able to make the prediction, but you can ignore it.

TestInputGenerator.py:
This program is designed to generate test cases from EEG_measurements data. It will let you pick a participant as the test input (since these are all the data we have). You will be required to enter the number that stand for the participant into the terminal. The number you entered must between 1-40.

ScalpMap.py:
A program that can draw a scalp map of electrode placement.

BarGraph.py:
A program that plot a bar graph to compare the mean MSE between input and Spanish model & input and Non-Spanish model.