import mne
import pandas as pd
import pyedflib
import numpy as np

# Define input and output files
csv_file = 'Non-Spanish Data/book_english-spanish_translation.csv'
edf_file = 'output.edf'

# Read CSV file
df = pd.read_csv(csv_file)

# Transpose data so each row represents a channel
data = df.values.T

# Set sampling rate and channel info
sample_rate = 256
n_channels = data.shape[0]
signal_labels = list(df.columns)

# Create EDF file
with pyedflib.EdfWriter(edf_file, n_channels=n_channels, file_type=pyedflib.FILETYPE_EDFPLUS) as edf:
    channel_info = []
    for i in range(n_channels):
        ch_dict = {
            'label': signal_labels[i],
            'dimension': 'uV',
            'sample_rate': sample_rate,
            'physical_min': data[i].min(),
            'physical_max': data[i].max(),
            'digital_min': -32768,
            'digital_max': 32767,
            'transducer': '',
            'prefilter': ''
        }
        channel_info.append(ch_dict)
    edf.setSignalHeaders(channel_info)
    edf.writeSamples(data)

print("CSV data successfully converted to EDF format.")

# Load EDF file in MNE
raw = mne.io.read_raw_edf(edf_file, preload=True)

# Set montage
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)

# Plot raw data for inspection
raw.plot(n_channels=n_channels, scalings='auto', title='Inspect Raw Data')

# Create events every second, ensuring they fit within the data duration
duration_in_seconds = int(len(raw.times) / sample_rate)
event_samples = np.arange(0, duration_in_seconds) * sample_rate
events = np.column_stack((event_samples, np.zeros_like(event_samples, dtype=int), np.ones_like(event_samples)))

# Debug: Check events and raw data length
print(f"Number of events: {len(events)}")
print(f"First event sample: {events[0, 0]}")
print(f"Last event sample: {events[-1, 0]}")
print(f"Total data duration in samples: {len(raw.times)}")

# Define event ID
event_id = {'FixedIntervalEvent': 1}

# Shorter time window in milliseconds, no baseline correction
tmin_ms = 0  # 0 ms
tmax_ms = 500  # 200 ms
epochs = mne.Epochs(raw, events, event_id=event_id, tmin=tmin_ms / 1000, tmax=tmax_ms / 1000,
                    baseline=None, reject=None, flat=None, preload=True, verbose=True)

# Check if epochs are not empty
if len(epochs) == 0:
    print("Warning: All epochs were dropped. Please check the event timing and data quality.")
else:
    # Compute and plot the topomap with time in milliseconds
    evoked = epochs.average()
    evoked.plot_topomap(times=[tmax_ms / 1000], ch_type='eeg', show=True, time_unit='ms')
