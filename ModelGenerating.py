import pandas as pd
import os

# Loading participants data
participants = pd.read_csv("metadata.csv")
participants['participant'] = participants['participant'].astype(int)

# Categorize participants by their proficiency in Spanish
espParticipants = participants[participants['spanish'] == 1]['participant'].tolist()  # participants who speak Spanish
nonEspParticipants = participants[participants['spanish'] == 0]['participant'].tolist()  # participants who do not speak Spanish

folder_path = 'EEG_Measurements'
filenames = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    filenames.append(file_path)

espFiles = pd.DataFrame(columns=['word', 'language', 'relation', 'files'])
nonEspFiles = pd.DataFrame(columns=['word', 'language', 'relation', 'files'])

seen_files_spanish = set()
seen_files_nonSpanish = set()

for filename in filenames:
    if "non-english" in filename:
        continue
    if ("spanish" not in filename) & ("english-english" not in filename):
        continue
    parts = filename.split('\\')[1].split('_')
    word = parts[0]
    language = parts[1]
    relation = parts[2]
    person = int(parts[3].split('.')[0])

    unique_key = f"{word}_{language}_{relation}"
    if person in espParticipants:
        if unique_key not in seen_files_spanish:
            espFiles.loc[len(espFiles)] = [word, language, relation, [filename]]
            seen_files_spanish.add(unique_key)
        else:
            idx = espFiles.index[(espFiles['word'] == word) &
                                 (espFiles['language'] == language) &
                                 (espFiles['relation'] == relation)].tolist()
            if idx:
                idx = idx[0]
                espFiles.at[idx, 'files'].append(filename)
    else:
        if unique_key not in seen_files_nonSpanish:
            nonEspFiles.loc[len(nonEspFiles)] = [word, language, relation, [filename]]
            seen_files_nonSpanish.add(unique_key)
        else:
            idx = nonEspFiles.index[(nonEspFiles['word'] == word) &
                                    (nonEspFiles['language'] == language) &
                                    (nonEspFiles['relation'] == relation)].tolist()
            if idx:
                idx = idx[0]
                nonEspFiles.at[idx, 'files'].append(filename)

DataList = espFiles[['word', 'language', 'relation']]
DataList.to_csv('Data List.csv', index=False)

# Create folders for data
os.makedirs('Spanish Data', exist_ok=True)
os.makedirs('Non-Spanish Data', exist_ok=True)

# Function to process and save data
def process_data(files_df, output_folder):
    for index, row in files_df.iterrows():
        data_list = []
        for fileName in row['files']:
            data = pd.read_csv(fileName)
            data_list.append(data)
        # Concatenate DataFrames and compute mean
        combined_data = pd.concat(data_list).groupby(level=0).mean()
        # Construct the output filename
        output_filename = f"{row['word']}_{row['language']}_{row['relation']}.csv"
        combined_data.to_csv(os.path.join(output_folder, output_filename), index=False)

# Process Spanish Data
process_data(espFiles, 'Spanish Data')

# Process Non-Spanish Data
process_data(nonEspFiles, 'Non-Spanish Data')
