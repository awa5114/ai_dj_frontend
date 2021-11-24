import streamlit as st
import numpy as np
from ai_dj.trainer import clean_local_folders, get_audio_features_db, extract_wav_from_yt_link, update_new_audio_features, get_audio_features, mix_tracks, update_model_with_rating
from ai_dj import params
import os
import shutil
from tensorflow.python.lib.io import file_io
import pickle
from scipy.io.wavfile import write


start = 0

_, col2, _ = st.columns([1, 2, 1])

with col2:
    st.title("DJ for dummies")

st.markdown("""## Paste the Youtube link of your song below """)
youtube_link = st.text_input('Youtube link', '' )

if st.button('Create my mix!'):
    print('button clicked!')
    st.write('Creating your unique mix 🎉')
    latest_iteration = st.empty()
    bar = st.progress(0)
    latest_iteration.text("Starting engines..")
    bar.progress(10)
    clean_local_folders()
    audio_feature_track_names = get_audio_features_db()
    latest_iteration.text("Downloading youtube link..")
    bar.progress(20)
    if not audio_feature_track_names["youtube_link"].isin([f'{youtube_link}-{start}']).any():
        title, output_filename = extract_wav_from_yt_link(youtube_link)
        title = f'{title}-{start}'
        print(title)
        latest_iteration.text("Extracting audio features from user song..")
        bar.progress(35)
        new_song = update_new_audio_features(output_filename, title)
        np.save(
         file_io.FileIO(
             f'gs://ai_dj_batch627_data/data/audio_features/{title}.npy',
             'w'), new_song)
        track_info = {"name": title, 
                      "youtube_link": f'{youtube_link}-{start}',
                      "audio_features_file": f'gs://ai_dj_batch627_data/data/audio_features/{title}.npy'
                      }
        audio_feature_track_names = audio_feature_track_names.append(track_info, ignore_index=True)
        np.save(
         file_io.FileIO(
             f'gs://ai_dj_batch627_data/data/audio_features/audio_features_track_names.csv',
             'w'), audio_feature_track_names)
        name = title
    else:
        name = audio_feature_track_names[audio_feature_track_names["youtube_link"] == f'{youtube_link}-{start}']["name"].values[0]
        latest_iteration.text("Extracting audio features from user song..")
        bar.progress(35)
        new_song = get_audio_features(name)
    model = pickle.load(open("pipeline.pkl","rb"))
    predicted_rating = 0
    n = 0
    latest_iteration.text("Matching with other song..")
    bar.progress(65)
    while predicted_rating < 5.0:
        if n < 5:
            # other_name = name
            # while other_name == name:
            other_name = audio_feature_track_names.sample(1)["name"].values[0]
            other_song = get_audio_features(other_name)
            # audio_files = [name, other_song]
            mixed_song, mix_tracks_rating_df = mix_tracks(new_song, other_song)
            mix_tracks_predict_df = mix_tracks_rating_df[["bpm_difference", "camelot_distance", "z_cross_diff_original",
                "mean_ampl_diff_original", "min_freq_diff_original", "max_freq_diff_original",
                "range_freq_diff_original", "n_drums", "n_bass", "n_vocals", "n_other", 
                "mean_ampl_mix", "z_cross_mix"]]
            predicted_rating = model.predict(mix_tracks_predict_df)[0]
            print(predicted_rating)
            n += 1
        else:
            break
    latest_iteration.text("Creating mix..")
    bar.progress(80)
    final_mix = np.array(mixed_song)
    # export a mix to a wav file
    sr = 44100
    mixed_name = f"{name} - {other_name}"
    if os.path.isdir(f'{params.MIXED_AUDIO_FOLDER}'):
        shutil.rmtree(f'{params.MIXED_AUDIO_FOLDER}')
        os.mkdir(f'{params.MIXED_AUDIO_FOLDER}/')
    
    write(f"{params.MIXED_AUDIO_FOLDER}{mixed_name}.wav", sr, final_mix)
    mix_file = f'{params.MIXED_FOLDER}/{mixed_name}.wav'
    mix_rating_df = mix_tracks_rating_df.drop(columns=["mix"])
    print(mix_rating_df.head())
        
    bar.progress(95)
    latest_iteration.text("Transforming mix to audio..")
    ## Split and mix
    @st.cache
    def get_mix():
        audio_file = open(f'ai_dj/{mix_file}', 'rb')
        audio_bytes = audio_file.read()
        bar.progress(100)
        latest_iteration.text("Done!")
        return  audio_bytes
    st.write(f"Your song was mixed with {other_name}:")
    st.audio(get_mix(), format='audio/wav')
    
    st.markdown("""### Enjoy the newly created mix by ai_dj!""")

    rating = st.slider("Please give a rating to the track!", 1, 10, 5)

    if st.button("Submit my rating"):
        st.write("Thank you for your feedback, we'll use it to keep improving")
    
# else:
#     st.write('Nothing created so far 😞')

# st.write("###")
