import pandas as pd
import numpy as np
from ai_dj import audio_features
from ai_dj.neighbour_songs import create_camelot_wheel
from ai_dj.audio_features import AudioFeatureExtracter
from ai_dj import params
import librosa
import random
from tensorflow.python.lib.io import file_io


def load_audio_features():
    audio_features_updated = np.load("ai_dj/data/audio_features2.npy", allow_pickle=True)
    audio_features_updated = pd.DataFrame(audio_features_updated)
    audio_features_updated.columns=["name", "output_file_mp3", "BPM", "key", 
                                        "wave_original", "mean_aplitude_original", "z_cross_original", "min_freq_original", "max_freq_original", "range_freq_original",
                                        "wave_bass", "mean_aplitude_bass", "z_cross_bass", "min_freq_bass", "max_freq_bass", "range_freq_bass",
                                        "wave_drums", "mean_aplitude_drums", "z_cross_drums", "min_freq_drums", "max_freq_drums", "range_freq_drums",
                                        "wave_vocals", "mean_aplitude_vocals", "z_cross_vocals", "min_freq_vocals", "max_freq_vocals", "range_freq_vocals",
                                        "wave_other", "mean_aplitude_other", "z_cross_other", "min_freq_other", "max_freq_other", "range_freq_other",
                                        "wave_mixed", "mean_aplitude_mixed", "z_cross_mixed", "min_freq_mixed", "max_freq_mixed", "range_freq_mixed", "beat_times"
                                        ]
    return audio_features_updated

def get_mix_features(mix_tracks_df):
    for ind, track in mix_tracks_df.iterrows():
        name = track["name"]
        bpm_list = [track["BPM"] for ind, track in mix_tracks_df.iterrows()]
        key_list = [track["key"] for ind, track in mix_tracks_df.iterrows()]
        mix_name_list = [track["name"] for ind, track in mix_tracks_df.iterrows()]
        z_cross_list = [track["z_cross_original"] for ind, track in mix_tracks_df.iterrows()]
        mean_ampl_list = [track["mean_aplitude_original"] for ind, track in mix_tracks_df.iterrows()]
        min_freq_list = [track["min_freq_original"] for ind, track in mix_tracks_df.iterrows()]
        max_freq_list = [track["max_freq_original"] for ind, track in mix_tracks_df.iterrows()]
        range_freq_list = [track["range_freq_original"] for ind, track in mix_tracks_df.iterrows()]


    mix_name = "-".join(mix_name_list)
    bpm_diff_original = abs(bpm_list[0] - bpm_list[1])
    z_cross_diff_original = abs(z_cross_list[0] - z_cross_list[1])
    mean_ampl_diff_original = abs(mean_ampl_list[0] - mean_ampl_list[1])
    min_freq_diff_original = abs(min_freq_list[0] - min_freq_list[1])
    max_freq_diff_original = abs(max_freq_list[0] - max_freq_list[1])
    range_freq_diff_original = abs(range_freq_list[0] - range_freq_list[1])

    camelot_wheel = create_camelot_wheel()
    camelot_key_df = camelot_wheel[camelot_wheel["key"] == key_list[0]].reset_index()
    if key_list[1] == camelot_key_df["neighbor_top"][0]:
        camelot_distance = "neighbor_top"
    elif key_list[1] == camelot_key_df["neighbor_left"][0]:
        camelot_distance = "neighbor_left"
    elif key_list[1] == camelot_key_df["neighbor_right"][0]:
        camelot_distance = "neighbor_right"
    elif key_list[1] == key_list[0]:
        camelot_distance = "same_key"
    else:
        camelot_distance = "no_neigbor"
    mix_df = pd.DataFrame(columns=["mix_name", "bpm_difference", "camelot_distance", "z_cross_diff_original",
                                   "mean_ampl_diff_original", "min_freq_diff_original", "max_freq_diff_original",
                                   "range_freq_diff_original"])
    mix_dict = {
        "mix_name": mix_name,
        "bpm_difference": bpm_diff_original,
        "camelot_distance": camelot_distance,
        "z_cross_diff_original": z_cross_diff_original,
        "mean_ampl_diff_original": mean_ampl_diff_original,
        "min_freq_diff_original": min_freq_diff_original,
        "max_freq_diff_original": max_freq_diff_original,
        "range_freq_diff_original": range_freq_diff_original
                }
    mix_df = mix_df.append(mix_dict, ignore_index=True)
    return mix_df

def get_wave_data(mix_tracks_df):
    wave_data = {}
    for ind, track in mix_tracks_df.iterrows():
        name = track["name"]
        wave_data[name] = {}
        wave_bass = track["wave_bass"]
        wave_drums = track["wave_drums"]
        wave_vocals = track["wave_vocals"]
        wave_other = track["wave_other"]
        stem_waves = {'bass': wave_bass,
                      'drums': wave_drums,
                      'vocals': wave_vocals,
                      'other': wave_other}
        beat_times = track["beat_times"]
        wave_data[name]["predictions"] = stem_waves
        wave_data[name]["beat_times"] = beat_times
    bpm_avg = np.array([track["BPM"] for ind, track in mix_tracks_df.iterrows()]).mean()
    return wave_data, bpm_avg


def get_mix_tracks(wave_data, target_tempo, n_stems=4, n_beats=32):
    target_tempo = target_tempo/60
    target_beat_length_seconds = 1/target_tempo
    target_total_length_seconds = target_beat_length_seconds*n_beats

    audio_files = list(wave_data.keys())
    available_stems = {}
    for file in audio_files:
        possible_stems = ['bass', 'drums', 'vocals', 'other']
        available_stems[file] = possible_stems
    #result = np.zeros((int(n_beats*target_beat_length_seconds*44100)))
    result = []
    stems = {}
    stems_used = []
    while len(result) < 4:
        stem = random.choice(possible_stems)
        audio_file = random.choice(audio_files)
        if stem in available_stems[audio_file]:
            #print("yes", audio_file, stem)
            available_stems[audio_file].remove(stem)
            
            stem_wave = wave_data[audio_file]["predictions"][stem]
            beat_times = wave_data[audio_file]['beat_times']
            stems[stem] = stem_wave
            stems_used.append(stem)

            start_time = beat_times[0] 
            end_time = beat_times[n_beats]
            start_sample = librosa.time_to_samples(beat_times, sr=44100)[0]
            end_sample = librosa.time_to_samples(beat_times, sr=44100)[n_beats]
            snippet = stem_wave[start_sample:end_sample]

            total_length_seconds = end_time - start_time
            rate = total_length_seconds/target_total_length_seconds

            current_result = librosa.effects.time_stretch(snippet, rate=rate)
            #print('next')
            #result += current_result
            result.append(current_result)
            
        else:
            #print("no", audio_file, stem)
            continue
    
    return result, stems_used

def get_stem_info(df, result, stems):
    n_drums = 0
    n_bass = 0
    n_vocals = 0
    n_other = 0
    for ind, key in enumerate(stems):
        if key == "drums":
            n_drums += 1
            if n_drums == 1:
                wave_drums = result[ind]
            else:
                if len(wave_drums) == len(result[ind]):
                    wave_drums += result[ind]
        if key == "bass":
            n_bass += 1
            if n_bass == 1:
                wave_bass = result[ind]
            else:
                if len(wave_bass) == len(result[ind]):
                    wave_bass += result[ind]
        if key == "vocals":
            n_vocals += 1
            if n_vocals == 1:
                wave_vocals = result[ind]
            else:
                if len(wave_vocals) == len(result[ind]):
                    wave_vocals += result[ind]
        if key == "other":
            n_other += 1
            if n_other == 1:
                wave_other = result[ind]
            else:
                if len(wave_other) == len(result[ind]):
                    wave_other += result[ind]
    if n_drums == 0:
        wave_drums = [0]
    if n_bass == 0:
        wave_bass = [0]   
    if n_vocals == 0:
        wave_vocals = [0]
    if n_other == 0:
        wave_other = [0]
    
    mix = result[0] + result[1] + result[2] + result[3]
    extracter = AudioFeatureExtracter()
    mean_ampl_mix = extracter.mean_amplitude(mix)
    z_cross_mix = extracter.z_cross(mix)

    df["n_drums"] = n_drums
    df["n_bass"] = n_bass
    df["n_vocals"] = n_vocals,
    df["n_other"] = n_other,
    # df["wave_drums"] = wave_drums,
    # df["wave_bass"] = wave_bass,
    # df["wave_vocals"] = wave_vocals,
    # df["wave_other"] = wave_other,
    df["mix"] = mix,
    df["mean_ampl_mix"] = mean_ampl_mix, 
    df["z_cross_mix"] = z_cross_mix,
    df["rating"] = 0
    return df

# ## Test ##
# audio_features_df = load_audio_features()
# mix_tracks_rating_df = pd.DataFrame()
# while len(mix_tracks_rating_df) < 10:
#     mix_tracks_df = audio_features_df.sample(2)
#     wave_data, bpm_avg = get_wave_data(mix_tracks_df)
#     mix_df = get_mix_features(mix_tracks_df)
#     result, stems = get_mix_tracks(wave_data, bpm_avg)
#     if len(result[0]) == len(result[1]) == len(result[2]) == len(result[3]):
#         mix_df = get_stem_info(mix_df, result, stems)
#         mixed_song = mix_df["mix"][0]
#         mix_tracks_rating_df = mix_tracks_rating_df.append(mix_df, ignore_index=True)
#     else:
#         continue
#     print(len(mix_tracks_rating_df))
# #np.save("ai_dj/data/mix_tracks_rating_df.npy", mix_tracks_rating_df)
# np.save(
#          file_io.FileIO(
#              f'gs://{params.BUCKET_NAME}/{params.AUDIO_FEATURES_FOLDER}/mix_tracks_rating_df30.npy',
#              'w'), mix_tracks_rating_df)
# ## find other way to play for rating
# #sr = 44100
# #Audio(data=mixed_song, rate=sr)
