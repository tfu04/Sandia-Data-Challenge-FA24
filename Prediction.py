import numpy as np
import pandas as pd
import os

# Loading model file names
espDataFileNames = []
nonEspDataFileNames = []
for filename in os.listdir('Spanish Data'):
    file_path = os.path.join('Spanish Data', filename)
    espDataFileNames.append(file_path)

for filename in os.listdir('Non-Spanish Data'):
    file_path = os.path.join('Non-Spanish Data', filename)
    nonEspDataFileNames.append(file_path)



# Loading input file names, also create a DataFrame of data for input
inputDataFileNames = []
inputDataFileList = pd.DataFrame(columns=['word', 'language', 'relation', 'inputFilePath'])
seen_files = set()
for filename in os.listdir('input'):
    file_path = os.path.join('input', filename)
    inputDataFileNames.append(file_path)
    parts = filename.split('_')
    word = parts[0]
    language = parts[1]
    relation = parts[2]

    unique_key = f"{word}_{language}_{relation}"
    if unique_key not in seen_files:
        inputDataFileList.loc[len(inputDataFileList)] = [word, language, relation, file_path]
        seen_files.add(unique_key)

# find the type of data that both input and model have
commonData = pd.merge(pd.read_csv('Data List.csv'), inputDataFileList)

# Function that calculate MSE between two DataFrame
def calculateMSE(first, second):
     return np.mean((first - second)**2)


# Calculate the average Mean Squared Error (MSE) between input data and spanish data and between input data and non-spanish data
spanishSum = 0 # the sum of MSE between input data and spanish data
nonSpanishSum = 0 # the sum of MSE between input data and spanish data
for i in range(len(commonData)):
    # read data files into DataFrame
    inputData = pd.read_csv(commonData.at[i, 'inputFilePath'])
    spanishData = pd.read_csv(os.path.join('Spanish Data', commonData.at[i, 'word'] + '_' + commonData.at[i, 'language'] + '_' + commonData.at[i, 'relation'] + '.csv'))
    nonSpanishData = pd.read_csv(os.path.join('Non-Spanish Data', commonData.at[i, 'word'] + '_' + commonData.at[i, 'language'] + '_' + commonData.at[i, 'relation'] + '.csv'))
    # calculate the different between data and add it to sum
    spanishSum += calculateMSE(inputData, spanishData)
    nonSpanishSum += calculateMSE(inputData, nonSpanishData)
spanishMean = spanishSum/len(commonData)
nonSpanishMean = nonSpanishSum/len(commonData)

# make prediction of whether the input participant speak spanish
if spanishMean < nonSpanishMean:
    print('participant speak spanish')
elif nonSpanishMean < spanishMean:
    print('participant does not speak spanish')
else:
    print('we are not able to predict whether participant speak spanish')
    # Note: The probability of having this result is extremely low. Most of the time you can ignore this case.