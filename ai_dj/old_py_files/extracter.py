from ai_dj import gcp_storage, neighbour_songs
from ai_dj.audio_features import AudioFeatureExtracter
from ai_dj.split_audio import SpleeterSeparator
import os
import shutil
from google.cloud import storage
import pandas as pd

from ai_dj import params

## Clean local folders
def clean_local_folders():
    local_folders = params.LOCAL_FOLDERS
    for folder in local_folders:
        if os.path.isdir(f'{params.DATA_FOLDER}/{folder}'):
                shutil.rmtree(f'{params.DATA_FOLDER}/{folder}')
        os.mkdir(f'{params.DATA_FOLDER}/{folder}/')
                
## Get youtube_link from app
def get_youtube_link():
    youtube_link = "https://www.youtube.com/watch?v=xF-UznUkhP8"
    return youtube_link

## Extract youtube_wav file & audiofeatures + upload to the folder
def extract_features_and_upload(youtube_link):
    features_extracter = AudioFeatureExtracter()
    output_file, bpm, key = features_extracter.youtube_audio_features(youtube_link)
    gcp_storage.upload_youtube_wav(output_file)
    return output_file, bpm, key

## Extract mp3 file & audiofeatures + upload to the folder
def extract_mp3_features_and_upload(mp3_file):
    features_extracter = AudioFeatureExtracter()
    output_file = features_extracter.mp3_audio_features(mp3_file)
    print(output_file)
    #gcp_storage.upload_mp3_wav(output_file)
    return output_file

## Split into stems
def split_into_stems(file):
    gcp_storage.get_youtube_wav(file)
    temp_file = f"{params.DOWNLOADED_FOLDER}/{file}"
    separator = SpleeterSeparator(temp_file)
    separator.split_song()

## Find 2 other songs
def get_neighbor_songs(output_file, bpm, key):
    neighbours = neighbour_songs.filter_bpm_keys(output_file, bpm, key)
    two_songs = neighbour_songs.select_songs(neighbours)
    return two_songs

## Split 2 other songs into stems
# use split_into_stems()

## Determine which stems to mix


## Create mix from stems


## Update app

# Get MP3 audio file names
def get_mp3_file_names():
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_blob_name = params.MP3_DATA_FOLDER
    blobs = bucket.list_blobs(prefix=source_blob_name)
    mp3_files = []
    for blob in blobs:
        file = blob.name.replace("data/audio/", "")
        mp3_files.append(file)
    return mp3_files



if __name__=='__main__':
    """get Youtube link features and update audio_features.csv"""
    gcp_storage.get_audio_features_csv()
    yt_link = get_youtube_link()
    audio_df = pd.read_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}', index_col=0)
    if not yt_link in audio_df["youtube_link"].values:
        clean_local_folders()
        output_file, bpm, key = extract_features_and_upload(yt_link)
        print(output_file)
    else:
        bpm = audio_df[audio_df["youtube_link"] == yt_link]["BPM"].values[0]
        key = audio_df[audio_df["youtube_link"] == yt_link]["key"].values[0]
        output_file = audio_df[audio_df["youtube_link"] == yt_link]["output_file"].values[0]
    gcp_storage.upload_audio_features_csv()
    two_songs = get_neighbor_songs(output_file, bpm, key)
    print(two_songs["output_file"])
    
    """get mp3_file features and update audio_features.csv"""
    # gcp_storage.get_audio_features_csv()
    # audio_df = pd.read_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}', index_col=0)
    # mp3_files = get_mp3_file_names()
    # for mp3_file in mp3_files:
    #     output_file_name = mp3_file.replace(".mp3", ".wav")    
    #     if not output_file_name in audio_df["output_file"].values:
    #         clean_local_folders()
    #         if mp3_file.endswith(".mp3"):
    #             extract_mp3_features_and_upload(mp3_file)
    # gcp_storage.upload_audio_features_csv()
    