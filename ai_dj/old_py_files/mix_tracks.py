import random
import madmom
import librosa
from spleeter.separator import Separator
import numpy as np
import pickle

def split_tracks(audio_file, n_stems, start=0):
    mix_data = {}
    for audio_file in audio_files:
        mix_data[audio_file] = {}
        
        # load audio with madmom
        audio_file = str(audio_file)
        stop = start + 60
        audio, sr = madmom.io.audio.load_ffmpeg_file(audio_file, sample_rate=44100, dtype=float, num_channels=2, start=start, stop=stop)
        audio = madmom.audio.signal.normalize(audio)
        
        # beat tracking
        proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
        act = madmom.features.beats.RNNBeatProcessor()(audio_file)
        beat_times = proc(act)
        clicks = librosa.clicks(beat_times, sr=sr, length=len(audio))
        mix_data[audio_file]['clicks'] = clicks
        mix_data[audio_file]['beat_times'] = beat_times
        
        # source separation
        separator = Separator('spleeter:{}stems'.format(n_stems))
        prediction = separator.separate(audio)
        mix_data[audio_file]['prediction'] = {}
        for key, value in prediction.items():
            mix_data[audio_file]['prediction'][key]=value

    return mix_data

def mix_tracks(mix_data, target_tempo, n_stems=4, n_beats=32):
    target_tempo = target_tempo/60
    target_beat_length_seconds = 1/target_tempo
    target_total_length_seconds = target_beat_length_seconds*n_beats

    audio_files = list(mix_data.keys())
    possible_stems = ['vocals', 'drums', 'vocals', 'other']
    #result = np.zeros((int(n_beats*target_beat_length_seconds*44100)))
    result = []
    for i in range(n_stems):
        stem = random.choice(possible_stems)
        audio_file = random.choice(audio_files)
        possible_stems.remove(stem)
        audio_files.remove(audio_file)
        
        stem = mix_data[audio_file]['prediction'][stem]
        beat_times = mix_data[audio_file]['beat_times']
        
        start_time = beat_times[0] 
        end_time = beat_times[n_beats]
        start_sample = librosa.time_to_samples(beat_times, sr=44100)[0]
        end_sample = librosa.time_to_samples(beat_times, sr=44100)[n_beats]
        snippet = stem[:,0][start_sample:end_sample]
        
        total_length_seconds = end_time - start_time
        rate = total_length_seconds/target_total_length_seconds
        
        current_result = librosa.effects.time_stretch(snippet, rate=rate)
        print('next')
        #result += current_result
        result.append(current_result)

    return result

if __name__=="__main__":
    with open('ai_dj/data/mixing_data_4stem.pickle', 'rb') as handle:
        mix_data = pickle.load(handle)

    n_stems = 4
    n_beats = 32
    target_tempo = 120/60
    target_beat_length_seconds = 1/target_tempo
    target_total_length_seconds = target_beat_length_seconds*n_beats

    audio_files = list(mix_data.keys())
    possible_stems = ['vocals', 'drums', 'vocals', 'other']
    result = np.zeros((int(n_beats*target_beat_length_seconds*44100)))

    for i in range(n_stems):
        stem = random.choice(possible_stems)
        audio_file = random.choice(audio_files)
        possible_stems.remove(stem)
        audio_files.remove(audio_file)
        
        stem = mix_data[audio_file]['prediction'][stem]
        beat_times = mix_data[audio_file]['beat_times']
        clicks = mix_data[audio_file]['clicks']
        
        start_time = beat_times[0] 
        end_time = beat_times[n_beats]
        start_sample = librosa.time_to_samples(beat_times, sr=44100)[0]
        end_sample = librosa.time_to_samples(beat_times, sr=44100)[n_beats]
        snippet = stem[:,0][start_sample:end_sample]
        
        
        
        total_length_seconds = end_time - start_time
        rate = total_length_seconds/target_total_length_seconds
        
        current_result = librosa.effects.time_stretch(snippet, rate=rate)
        print('next')
        result += current_result
        