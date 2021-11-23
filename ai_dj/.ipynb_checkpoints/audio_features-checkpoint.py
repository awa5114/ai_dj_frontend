from librosa.core import convert
from ai_dj.download_youtube import YoutubeDownloader
import numpy as np
import pandas as pd
import librosa
from scipy.signal import spectrogram
from pyACA.ToolComputeHann import ToolComputeHann
from pyACA.FeatureSpectralPitchChroma import FeatureSpectralPitchChroma
from pyACA.ToolPreprocAudio import ToolPreprocAudio
from pyACA.ToolReadAudio import ToolReadAudio
from ai_dj.params import DOWNLOADED_FOLDER, RAW_DATA_FOLDER
from ai_dj import convert_mp3
from os import path
from ai_dj import gcp_storage
from ai_dj import params

class AudioFeatureExtracter:

    def __init__(self):
        pass
        
    def get_BPM(self, file, sr=44100):
        y, sr = librosa.load(file, sr=sr)

        # Run the default beat tracker
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        #print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

        # Convert the frame indices of beat events into timestamps
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return tempo, y, sr

    def computeKey(self, afAudioData, f_s, afWindow=None, iBlockLength=4096, iHopLength=2048):

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

    def computeKeyCl(self, file):
        
        [f_s, afAudioData] = ToolReadAudio(file)
        # afAudioData = np.sin(2*np.pi * np.arange(f_s*1)*440./f_s)

        cKey = self.computeKey(afAudioData, f_s)
        #print("detected key: ", cKey)
        
        return cKey
    
    def min_max_freq(y, sr):
        librosa.feature.spectral_rolloff(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.99)
        max_freq = rolloff.max()
        rolloff_min = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.01)
        sorted_rolloff = sorted(rolloff_min[0])
        for val in sorted_rolloff:
            if val > 0:
                min_freq = val
                break
        freq_diff = max_freq-min_freq
        return max_freq, min_freq, freq_diff
    
    def youtube_audio_features(self, yt_link):
        youtubedl = YoutubeDownloader(yt_link)
        youtubedl.download_song()
        title, song_id, output_file, yt_link = youtubedl.download_metadata()
        file_path = f'{DOWNLOADED_FOLDER}/{output_file}'
        #audio_feature_extracter = AudioFeatureExtracter(f'{DOWNLOADED_FOLDER}/{output_filename}')
        tempo, y, sr = self.get_BPM(file_path)
        key = self.computeKeyCl(file_path)
        max_freq, min_freq, freq_diff = min_max_freq(y, sr)
        new_song_dict = {"song_id":song_id,
                        "youtube_link":yt_link,
                        "output_file": output_file,
                        "title": title, 
                        "BPM": tempo, 
                        "key": key, 
                        "beat_frames":"no beat_frames", 
                        "beat_times": "no beat_times", 
                        "min_freq": min_freq,
                        "max_freq": max_freq,
                        "freq_diff": freq_diff}
        self.df = pd.DataFrame(columns=new_song_dict.keys())
        self.df = self.df.append(new_song_dict, ignore_index=True)
        # write to csv
        csv_df = pd.read_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}', index_col=0)
        csv_df = csv_df.append(self.df)
        csv_df = csv_df.drop_duplicates(subset=['title'])
        csv_df.to_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}')
        return (output_file, tempo, key)
        
    def mp3_audio_features(self, file):
        output_file = convert_mp3.convert_mp3_to_wav(file)
        file_path = f'{DOWNLOADED_FOLDER}/{output_file}'
        title = output_file.replace(".wav", "")
        tempo, y, sr = self.get_BPM(file_path)
        key = self.computeKeyCl(file_path)
        max_freq, min_freq, freq_diff = min_max_freq(y, sr)
        new_song_dict = {"song_id":"no song_id",
                        "youtube_link":"no youtube_link",
                        "output_file": output_file,
                        "title": title, 
                        "BPM": tempo, 
                        "key": key, 
                        "beat_frames":"no beat_frames", 
                        "beat_times": "no beat_times", 
                        "min_freq": min_freq,
                        "max_freq": max_freq,
                        "freq_diff": freq_diff}
        self.df = pd.DataFrame(columns=new_song_dict.keys())
        self.df = self.df.append(new_song_dict, ignore_index=True)
        # write to csv
        csv_df = pd.read_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}', index_col=0)
        csv_df = csv_df.append(self.df)
        csv_df = csv_df.drop_duplicates(subset=['title'])
        # csv_df = self.df
        csv_df.to_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}')
        return output_file
        

## Test ##
# yt_link = "https://www.youtube.com/watch?v=L-2CyO8pc0E"
# #file_name = '056247.mp3'
# #file = f'{RAW_DATA_FOLDER}/{file_name}'
# extracter = AudioFeatureExtracter()
# #extracter.mp3_audio_features(file)
# extracter.youtube_audio_features(yt_link)
# extracter.write_to_csv()
# extracter.upload_csv_to_gcp()
## Test ##