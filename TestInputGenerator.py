import shutil
import os

shutil.rmtree('input')
os.makedirs('input')

# getting input (number that represent the participant) from the user
participant = input('the participant you wish to use as test input:')

# traverse all the files in EEG_Measurements
for filename in os.listdir('EEG_Measurements'):
    # exclude files unrelated to spanish or english
    if 'non-english' in filename:
        continue
    if ("spanish" not in filename) & ("english-english" not in filename):
        continue
    # copy files that belongs to the chosen participant
    if participant == filename.split('.')[0].split('_')[3]:
        shutil.copyfile(os.path.join('EEG_Measurements', filename),os.path.join('input', filename))