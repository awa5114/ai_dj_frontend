from __future__ import unicode_literals
import youtube_dl
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
import matplotlib.pyplot as plt
import librosa
import numpy as np
import os
import soundfile as sf

def get_BPM(output_filename):
    y, sr = librosa.load(output_filename, sr=44100)

    # Run the default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

    # Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return tempo, beat_frames, beat_times

def computeKey(afAudioData, f_s, afWindow=None, iBlockLength=4096, iHopLength=2048):

    # compute window function for FFT
    if afWindow is None:
        afWindow = ToolComputeHann(iBlockLength)

    assert(afWindow.shape[0] == iBlockLength), "parameter error: invalid window dimension"

    # key names
    cKeyNames = np.array(['C Maj', 'C# Maj', 'D Maj', 'D# Maj', 'E Maj', 'F Maj', 'F# Maj', 'G Maj', 'G# Maj', 'A Maj', 'A# Maj', 'B Maj',
                         'c min', 'c# min', 'd min', 'd# min', 'e min', 'f min', 'f# min', 'g min', 'g# min', 'a min', 'a# min', 'b min'])

    # template pitch chroma (Krumhansl major/minor), normalized to a sum of 1
    t_pc = np.array([[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
                    [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]])
    t_pc = t_pc / t_pc.sum(axis=1, keepdims=True)

    # pre-processing
    afAudioData = ToolPreprocAudio(afAudioData, iBlockLength)

    # in the real world, we would do this block by block...
    [f, t, X] = spectrogram(afAudioData,
                            f_s,
                            afWindow,
                            iBlockLength,
                            iBlockLength - iHopLength,
                            iBlockLength,
                            False,
                            True,
                            'spectrum')

    #  scale the same as for matlab
    X = np.sqrt(X / 2)

    # compute instantaneous pitch chroma
    v_pc = FeatureSpectralPitchChroma(X, f_s)

    # average pitch chroma
    v_pc = v_pc.mean(axis=1)
    # compute manhattan distances for modes (major and minor)
    d = np.zeros(t_pc.shape)
    v_pc = np.concatenate((v_pc, v_pc), axis=0).reshape(2, 12)
    for i in range(0, 12):
        d[:, i] = np.sum(np.abs(v_pc - np.roll(t_pc, i, axis=1)), axis=1)

    # get unwrapped key index
    iKeyIdx = d.argmin()

    cKey = cKeyNames[iKeyIdx]

    return (cKey)

def computeKeyCl(cPath):
    
    [f_s, afAudioData] = ToolReadAudio(cPath)
    # afAudioData = np.sin(2*np.pi * np.arange(f_s*1)*440./f_s)

    cKey = computeKey(afAudioData, f_s)
    print("detected key: ", cKey)
    
    return cKey


def analyze_song(link, df):
    title, song_id, output_filename = download_song(link)
    tempo, beat_frames, beat_times = get_BPM(output_filename)
    key = computeKeyCl(output_filename)
    new_song_dict = {"song_id":song_id,
                       "youtube_link":link,
                       "output_file": output_filename,
                       "title": title, 
                       "BPM": tempo, 
                       "key": key}
    df = df.append(new_song_dict, ignore_index=True)
    df = df.drop_duplicates()
    return df

def split_song(filename):
    separator.separate_to_file(filename, 'Downloads/')


if __name__=='__main__':

    title, song_id, output_filename = download_song(yt_link)

    # # Get BPM

    tempo, beat_frames, beat_times = get_BPM(output_filename)


    # # Get Key


    cPath = output_filename
    key = computeKeyCl(cPath)

    # # Display waveplots

    y, sr = librosa.load(output_filename, duration=60)
    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
    librosa.display.waveplot(y, sr=sr, ax=ax[0])
    ax[0].set(title='Monophonic')
    ax[0].label_outer()

    y, sr = librosa.load(output_filename, mono=False, duration=60)
    librosa.display.waveplot(y, sr=sr, ax=ax[1])
    ax[1].set(title='Stereo')
    ax[1].label_outer()

    y, sr = librosa.load(output_filename, duration=60)
    y_harm, y_perc = librosa.effects.hpss(y)
    librosa.display.waveplot(y_harm, sr=sr, alpha=0.25, ax=ax[2])
    librosa.display.waveplot(y_perc, sr=sr, color='r', alpha=0.5, ax=ax[2])
    ax[2].set(title='Harmonic + Percussive')

    # # Add to audio features dataframe

    audio_features_dict = {"song_id":song_id,
                        "youtube_link":yt_link,
                        "output_file": output_filename,
                        "title": title, 
                        "BPM": tempo, 
                        "key": key}


    audio_features = pd.DataFrame(columns=audio_features_dict.keys())


    audio_features = audio_features.append(audio_features_dict, ignore_index=True)




    new_song_link = "https://www.youtube.com/watch?v=xarC5jAiO7w"
    audio_features = analyze_song(new_song_link, audio_features)


    audio_features.head()


    song_list = ["https://www.youtube.com/watch?v=SF8DGbfOFig", 
                "https://www.youtube.com/watch?v=Q77vdqA0hnM", 
                "https://www.youtube.com/watch?v=j2A1_OOTTss", 
                "https://www.youtube.com/watch?v=VIeY1J1M9Ts", 
                "https://www.youtube.com/watch?v=L-2CyO8pc0E", 
                "https://www.youtube.com/watch?v=q5rliCxX8xc", 
                "https://www.youtube.com/watch?v=A1eiTbiSrRc", 
                "https://www.youtube.com/watch?v=SKUk9RUacDQ", 
                "https://www.youtube.com/watch?v=nXOSgekiAJc"]


    for song in song_list:
        audio_features = analyze_song(song, audio_features)
        
    audio_features


    audio_features.head()

    # # Split songs with Spleeter

    # Using embedded configuration.
    separator = Separator('spleeter:4stems')

    for file in audio_features['output_file']:
        split_song(file)

    song_1 = "64 Ways (Dam Swindle's 65th Way Dub) feat. Mayer Hawthorne-SKUk9RUacDQ.wav"
    tempo_1, beat_frames_1, beat_times_1 = get_BPM(song_1)



    song_2 = "Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30.wav"
    tempo_2, beat_frames_2, beat_times_2 = get_BPM(song_2)


    sound1 = AudioSegment.from_file("Downloads/64 Ways (Dam Swindle's 65th Way Dub) feat. Mayer Hawthorne-SKUk9RUacDQ/drums.wav")
    sound2 = AudioSegment.from_file("Downloads/Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30/other.wav")
    combined = sound1.overlay(sound2)

    combined.export("../ai_dj/data/64_kygo_combined2.wav", format='wav')