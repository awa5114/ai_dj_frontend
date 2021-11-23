from ai_dj import gcp_storage, params
from ai_dj.mix_rating import get_wave_data, get_mix_features, get_mix_tracks, get_stem_info
from ai_dj.audio_features import get_BPM, computeKeyCl, min_max_freq, mean_amplitude, z_cross
from ai_dj.download_youtube import download_wav_and_metadata
from ai_dj.split_audio import split_tracks
from ai_dj.linear_model import load_rated_mixes, update_model
import librosa
import numpy as np
import pandas as pd
import os
import shutil
from tensorflow.python.lib.io import file_io
import io
import pandas as pd
import pickle
from scipy.io.wavfile import write

## Clean local folders
def clean_local_folders():
    if os.path.isdir(params.DOWNLOADED_FOLDER):
            shutil.rmtree(params.DOWNLOADED_FOLDER)
    os.mkdir(params.DOWNLOADED_FOLDER)
    if os.path.isdir(params.MIXED_AUDIO_FOLDER):
            shutil.rmtree(params.MIXED_AUDIO_FOLDER)
    os.mkdir(params.MIXED_AUDIO_FOLDER)

## Get youtube_link from app
def get_youtube_link():
    youtube_link = "https://www.youtube.com/watch?v=xarC5jAiO7w&ab_channel=ODESZA"
    start = 0
    return youtube_link, start

## Extract youtube_wav file & audiofeatures + upload to the folder
def extract_wav_from_yt_link(youtube_link):
    title, output_filename = download_wav_and_metadata(youtube_link)
    print("download done")
    #gcp_storage.upload_youtube_wav(output_filename)
    print("file not uploaded to gcp")
    return title, output_filename

def get_audio_features_db():
    f = io.BytesIO(
            file_io.read_file_to_string(
                f'gs://ai_dj_batch627_data/data/audio_features/audio_features_track_names.csv',
                binary_mode=True))
    audio_feature_track_names = np.load(f, allow_pickle=True)
    # audio_feature_track_names = pd.read_csv("ai_dj/data/audio_features_track_names.csv")
    audio_feature_track_names = pd.DataFrame(audio_feature_track_names)
    print(audio_feature_track_names)
    audio_feature_track_names.columns=["name", "youtube_link", "audio_features_file"]
    return audio_feature_track_names

def get_audio_features(name):
    f = io.BytesIO(
            file_io.read_file_to_string(
                f'gs://ai_dj_batch627_data/data/audio_features/{name}.npy',
                binary_mode=True))
    audio_features_df = np.load(f, allow_pickle=True)
    if len(audio_features_df) > 1:
        audio_features_df = pd.DataFrame(audio_features_df.T)
    else:
        audio_features_df = pd.DataFrame(audio_features_df)
    audio_features_df.columns=["name", "output_file_mp3", "BPM", "key", 
                                    "wave_original", "mean_aplitude_original", "z_cross_original", "min_freq_original", "max_freq_original", "range_freq_original",
                                    "wave_bass", "mean_aplitude_bass", "z_cross_bass", "min_freq_bass", "max_freq_bass", "range_freq_bass",
                                    "wave_drums", "mean_aplitude_drums", "z_cross_drums", "min_freq_drums", "max_freq_drums", "range_freq_drums",
                                    "wave_vocals", "mean_aplitude_vocals", "z_cross_vocals", "min_freq_vocals", "max_freq_vocals", "range_freq_vocals",
                                    "wave_other", "mean_aplitude_other", "z_cross_other", "min_freq_other", "max_freq_other", "range_freq_other",
                                    "wave_mixed", "mean_aplitude_mixed", "z_cross_mixed", "min_freq_mixed", "max_freq_mixed", "range_freq_mixed", "beat_times"
                                    ]
    return audio_features_df

def update_new_audio_features(output_filename, title):
    file_path = f'{params.DOWNLOADED_FOLDER}/{output_filename}'
    y, sr = librosa.load(file_path, sr=44100)
    bpm = get_BPM(y, sr)
    key = computeKeyCl(file_path)
    max_freq_original, min_freq_original, range_freq_original = min_max_freq(y, sr)
    mean_aplitude_original = mean_amplitude(y)
    z_cross_original = z_cross(y)
    audio_files = [output_filename]
    print("ready to split files")
    mix_data = split_tracks(audio_files, 4, 60)
    wave_bass = mix_data[output_filename]["prediction"]["bass"][:,0]
    max_freq_bass, min_freq_bass, range_freq_bass = min_max_freq(wave_bass, sr)
    mean_aplitude_bass = mean_amplitude(wave_bass)
    z_cross_bass = z_cross(wave_bass)
    wave_drums = mix_data[output_filename]["prediction"]["drums"][:,0]
    max_freq_drums, min_freq_drums, range_freq_drums = min_max_freq(wave_drums, sr)
    mean_aplitude_drums = mean_amplitude(wave_drums)
    z_cross_drums = z_cross(wave_drums)
    wave_vocals = mix_data[output_filename]["prediction"]["vocals"][:,0]
    max_freq_vocals, min_freq_vocals, range_freq_vocals = min_max_freq(wave_vocals, sr)
    mean_aplitude_vocals = mean_amplitude(wave_vocals)
    z_cross_vocals = z_cross(wave_vocals)
    wave_other = mix_data[output_filename]["prediction"]["other"][:,0]
    max_freq_other, min_freq_other, range_freq_other = min_max_freq(wave_other, sr)
    mean_aplitude_other = mean_amplitude(wave_other)
    z_cross_other = z_cross(wave_other)
    wave_mixed = wave_bass + wave_drums + wave_vocals + wave_other
    max_freq_mixed, min_freq_mixed, range_freq_mixed = min_max_freq(wave_mixed, sr)
    mean_aplitude_mixed = mean_amplitude(wave_mixed)
    z_cross_mixed = z_cross(wave_mixed)
    beat_times = mix_data[output_filename]["beat_times"]
    
    new_song = pd.DataFrame(columns=["name", "output_file_mp3", "BPM", "key", 
                                        "wave_original", "mean_aplitude_original", "z_cross_original", "min_freq_original", "max_freq_original", "range_freq_original",
                                        "wave_bass", "mean_aplitude_bass", "z_cross_bass", "min_freq_bass", "max_freq_bass", "range_freq_bass",
                                        "wave_drums", "mean_aplitude_drums", "z_cross_drums", "min_freq_drums", "max_freq_drums", "range_freq_drums",
                                        "wave_vocals", "mean_aplitude_vocals", "z_cross_vocals", "min_freq_vocals", "max_freq_vocals", "range_freq_vocals",
                                        "wave_other", "mean_aplitude_other", "z_cross_other", "min_freq_other", "max_freq_other", "range_freq_other",
                                        "wave_mixed", "mean_aplitude_mixed", "z_cross_mixed", "min_freq_mixed", "max_freq_mixed", "range_freq_mixed", "beat_times"
                                        ])
    new_song_dict = {"name": title,
                     "output_file_mp3": output_filename,
                     "BPM": bpm,
                     "key": key,
                     "wave_original": y,
                     "mean_aplitude_original": mean_aplitude_original,
                     "z_cross_original": z_cross_original,
                     "min_freq_original": min_freq_original, 
                     "max_freq_original": max_freq_original,
                     "range_freq_original": range_freq_original,
                     "wave_bass": wave_bass,
                     "mean_aplitude_bass": mean_aplitude_bass, 
                     "z_cross_bass": z_cross_bass, 
                     "min_freq_bass": min_freq_bass, 
                     "max_freq_bass": max_freq_bass, 
                     "range_freq_bass": range_freq_bass,
                     "wave_drums": wave_drums,
                     "mean_aplitude_drums": mean_aplitude_drums, 
                     "z_cross_drums": z_cross_drums, 
                     "min_freq_drums": min_freq_drums, 
                     "max_freq_drums": max_freq_drums, 
                     "range_freq_drums": range_freq_drums,
                     "wave_vocals": wave_vocals, 
                     "mean_aplitude_vocals": mean_aplitude_vocals, 
                     "z_cross_vocals": z_cross_vocals, 
                     "min_freq_vocals": min_freq_vocals, 
                     "max_freq_vocals": max_freq_vocals, 
                     "range_freq_vocals": range_freq_vocals,
                     "wave_other": wave_other,
                     "mean_aplitude_other": mean_aplitude_other, 
                     "z_cross_other": z_cross_other, 
                     "min_freq_other": min_freq_other, 
                     "max_freq_other": max_freq_other, 
                     "range_freq_other": range_freq_other,
                     "wave_mixed": wave_mixed,
                     "mean_aplitude_mixed": mean_aplitude_mixed, 
                     "z_cross_mixed": z_cross_mixed, 
                     "min_freq_mixed": min_freq_mixed, 
                     "max_freq_mixed": max_freq_mixed, 
                     "range_freq_mixed": range_freq_mixed, 
                     "beat_times": beat_times
                    }
    new_song = new_song.append(new_song_dict, ignore_index=True)
    return new_song

def mix_tracks(new_song, other_song):
    mix_tracks_rating_df = pd.DataFrame()
    while len(mix_tracks_rating_df) < 1:
        mix_tracks_df = new_song
        mix_tracks_df = mix_tracks_df.append(other_song, ignore_index=True)
        wave_data, bpm_avg = get_wave_data(mix_tracks_df)
        mix_df = get_mix_features(mix_tracks_df)
        result, stems = get_mix_tracks(wave_data, bpm_avg)
        if len(result[0]) == len(result[1]) == len(result[2]) == len(result[3]):
            mix_df = get_stem_info(mix_df, result, stems)
            mixed_song = mix_df["mix"][0]
            mix_tracks_rating_df = mix_tracks_rating_df.append(mix_df, ignore_index=True)
        else:
            continue
    return mixed_song, mix_tracks_rating_df

# def get_mix(youtube_link, start):
#     clean_local_folders()
#     audio_feature_track_names = get_audio_features_db()
#     if not audio_feature_track_names["youtube_link"].isin([f'{youtube_link}-{start}']).any():
#         title, output_filename = extract_wav_from_yt_link(youtube_link)
#         title = f'{title}-{start}'
#         print(title)
#         new_song = update_new_audio_features(output_filename, title)
#         np.save(
#          file_io.FileIO(
#              f'gs://ai_dj_batch627_data/data/audio_features/{title}.npy',
#              'w'), new_song)
#         track_info = {"name": title, 
#                       "youtube_link": f'{youtube_link}-{start}',
#                       "audio_features_file": f'gs://ai_dj_batch627_data/data/audio_features/{title}.npy'
#                       }
#         audio_feature_track_names = audio_feature_track_names.append(track_info, ignore_index=True)
#         # print(audio_feature_track_names["youtube_link"])
#         np.save(
#          file_io.FileIO(
#              f'gs://ai_dj_batch627_data/data/audio_features/audio_features_track_names.csv',
#              'w'), audio_feature_track_names)
#         name = title
#     else:
#         print(audio_feature_track_names.head())

#         name = audio_feature_track_names[audio_feature_track_names["youtube_link"] == youtube_link]["name"].values[0]
#         print(name)
#         new_song = get_audio_features(name)
#     model = pickle.load(open("pipeline.pkl","rb"))
#     predicted_rating = 0
#     n = 0
#     while predicted_rating < 5.0:
#         if n < 5:
#             # other_name = name
#             # while other_name == name:
#             other_name = audio_feature_track_names.sample(1)["name"].values[0]
#             print(other_name)
#             other_song = get_audio_features(other_name)
#             # audio_files = [name, other_song]
#             mixed_song, mix_tracks_rating_df = mix_tracks(new_song, other_song)
#             mix_tracks_predict_df = mix_tracks_rating_df[["bpm_difference", "camelot_distance", "z_cross_diff_original",
#                 "mean_ampl_diff_original", "min_freq_diff_original", "max_freq_diff_original",
#                 "range_freq_diff_original", "n_drums", "n_bass", "n_vocals", "n_other", 
#                 "mean_ampl_mix", "z_cross_mix"]]
#             predicted_rating = model.predict(mix_tracks_predict_df)[0]
#             print(predicted_rating)
#             n += 1
#         else:
#             break
#     final_mix = np.array(mixed_song)
#     # export a mix to a wav file
#     # final_mix = np.array(final_mix)
#     sr = 44100
#     mixed_name = f"{name} - {other_name}"
#     if os.path.isdir(f'{params.MIXED_AUDIO_FOLDER}'):
#         shutil.rmtree(f'{params.MIXED_AUDIO_FOLDER}')
#         os.mkdir(f'{params.MIXED_AUDIO_FOLDER}/')
    
#     write(f"{params.MIXED_AUDIO_FOLDER}{mixed_name}.wav", sr, final_mix)
#     gcp_storage.upload_mixed_audio(f'{mixed_name}.wav')
#     mix_file = f'{params.MIXED_FOLDER}/{mixed_name}.wav'
#     mix_rating_df = mix_tracks_rating_df.drop(columns=["mix"])
#     return mix_file, mixed_name, mix_rating_df
    
def update_model_with_rating(rating, mix_rating_df):
    df = load_rated_mixes()
    mix_rating_df["rating"] = rating
    df = df.append(mix_rating_df, ignore_index=True)
    df.to_csv(f"{params.DATA_FOLDER}/rated_mixes.csv", index=False)
    np.save(
         file_io.FileIO(
             f'gs://ai_dj_batch627_data/data/rated_mixes/rated_mixes.csv',
             'w'), df)
    update_model(df)
    return