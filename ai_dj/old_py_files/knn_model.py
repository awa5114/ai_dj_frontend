import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import youtube_dl
import audioread
import librosa
import librosa.display
import matplotlib.pyplot as plt
from os import path
from pydub import AudioSegment
import numpy as np
import pandas as pd
from scipy.signal import spectrogram
from pyACA.ToolComputeHann import ToolComputeHann
from pyACA.FeatureSpectralPitchChroma import FeatureSpectralPitchChroma
from pyACA.ToolPreprocAudio import ToolPreprocAudio
from pyACA.ToolReadAudio import ToolReadAudio
from spleeter.separator import Separator
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

audio_df = pd.read_csv("ai_dj/data/audio_features.csv")

encoder = OneHotEncoder(sparse=False)
encoder.fit(audio_df[["key"]])
key_encoded = encoder.transform(audio_df[["key"]])
for index, key in enumerate(encoder.categories_[0]):
    audio_df[key] = key_encoded.T[index]
    
scaler = StandardScaler()
audio_df["bpm_scaled"] = scaler.fit_transform(audio_df[["BPM"]])

from sklearn.neighbors import KNeighborsRegressor

X = audio_df[['A Maj', 'A# Maj', 'B Maj', 'C Maj', 'C# Maj', 'D Maj', 'D# Maj',
        'E Maj', 'F Maj', 'F# Maj', 'G Maj', 'G# Maj', 'a min', 'a# min',
        'b min', 'c min', 'c# min', 'd min', 'd# min', 'e min', 'f min',
        'f# min', 'g min', 'g# min', 'bpm_scaled']]
y = audio_df['bpm_scaled']

knn_model = KNeighborsRegressor().fit(X,y)

## Audio_features from new song, needs to be pulled in from extracter
new_song = pd.DataFrame()
new_song.loc[0,"name"] = title
new_song.loc[0,"BPM"] = bpm
new_song.loc[0,"key"] = key

key_encoded = encoder.transform(new_song[["key"]])
for index, key in enumerate(encoder.categories_[0]):
    new_song[key] = key_encoded.T[index]
new_song["bpm_scaled"] = scaler.transform(new_song[["BPM"]])

new_X = new_song[['A Maj', 'A# Maj', 'B Maj', 'C Maj', 'C# Maj', 'D Maj', 'D# Maj',
        'E Maj', 'F Maj', 'F# Maj', 'G Maj', 'G# Maj', 'a min', 'a# min',
        'b min', 'c min', 'c# min', 'd min', 'd# min', 'e min', 'f min',
        'f# min', 'g min', 'g# min', 'bpm_scaled']]
neighbors = knn_model.kneighbors(new_X, n_neighbors=2)[1][0]

neighbor_1 = audio_df.iloc[neighbors[0]][["title", "BPM", "key"]]
neighbor_2 = audio_df.iloc[neighbors[1]][["title", "BPM", "key"]]

