import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt

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

# Define a function that calculate MSE between two DataFrame
def calculateMSE(first, second):
    return np.mean((first - second)**2)


# Calculate the average Mean Squared Error (MSE) between input data and spanish data and between input data and non-spanish data
plotData = pd.DataFrame(columns=['language', 'relation', 'spanishMean', 'nonSpanishMean', 'NofFiles'])
createdRow = set()
for i in range(len(commonData)):
    # read data files into DataFrame
    inputData = pd.read_csv(commonData.at[i, 'inputFilePath'])
    spanishData = pd.read_csv(os.path.join('Spanish Data', commonData.at[i, 'word'] + '_' + commonData.at[i, 'language'] + '_' + commonData.at[i, 'relation'] + '.csv'))
    nonSpanishData = pd.read_csv(os.path.join('Non-Spanish Data', commonData.at[i, 'word'] + '_' + commonData.at[i, 'language'] + '_' + commonData.at[i, 'relation'] + '.csv'))
    # calculate the different between data and add it to sum
    unique_key = f"{commonData.at[i, 'language']}_{commonData.at[i, 'relation']}"
    if unique_key not in createdRow:
        plotData.loc[len(plotData)] = [commonData.at[i, 'language'], commonData.at[i, 'relation'], calculateMSE(spanishData, inputData), calculateMSE(nonSpanishData, inputData), 1]
        createdRow.add(unique_key)
    else:
        plotData.loc[(plotData.language == commonData.at[i, 'language']) & (plotData.relation == commonData.at[i, 'relation']), 'spanishMean'] += calculateMSE(spanishData, inputData)
        plotData.loc[(plotData.language == commonData.at[i, 'language']) & (plotData.relation == commonData.at[i, 'relation']), 'nonSpanishMean'] += calculateMSE(nonSpanishData, inputData)
        plotData.loc[(plotData.language == commonData.at[i, 'language']) & (plotData.relation == commonData.at[i, 'relation']), 'NofFiles'] += 1
plotData.spanishMean = plotData.spanishMean/plotData.NofFiles
plotData.nonSpanishMean = plotData.nonSpanishMean/plotData.NofFiles

# Combine 'language' and 'relation' columns into a single column for the x-axis
plotData['language_relation'] = plotData['language'] + ' - ' + plotData['relation']

# Plotting spanishMean and nonSpanishMean
plotData.plot(
    x='language_relation',
    y=['spanishMean', 'nonSpanishMean'],
    kind='bar',
    figsize=(10, 6),
    width=0.8
)

plt.title('Comparison of Spanish and Non-Spanish Mean MSE by Language and Relation')
plt.xlabel('Language - Relation')
plt.ylabel('Mean Squared Error (MSE)')
plt.xticks(rotation=45)
plt.legend(['Spanish Mean', 'Non-Spanish Mean'])
plt.tight_layout()
plt.show()