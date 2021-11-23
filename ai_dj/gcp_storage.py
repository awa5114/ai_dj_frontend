from google.cloud import storage
import os
from ai_dj import params


def get_mp3(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_blob_name = f'{params.MP3_DATA_FOLDER}/{file}'
    blob = bucket.blob(source_blob_name)
    destination_file_name = f'{params.TEMP_DATA_FOLDER}/{file}'
    blob.download_to_filename(destination_file_name)
    
def upload_mp3_wav(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    destination_file_name = f'{params.WAV_DATA_FOLDER}/{file}'
    blob = bucket.blob(destination_file_name)
    source_file_name = f'{params.DOWNLOADED_FOLDER}/{file}'
    blob.upload_from_filename(source_file_name)

def upload_youtube_wav(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    destination_file_name = f'{params.AUDIO_DATA_FOLDER}{file}'
    blob = bucket.blob(destination_file_name)
    source_file_name = f'{params.DOWNLOADED_FOLDER}/{file}'
    blob.upload_from_filename(source_file_name)
    
def get_audio_features_csv():
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_blob_name = f'{params.AUDIO_FEATURES_FOLDER}/{params.AUDIO_FEATURES_FILE}'
    blob = bucket.blob(source_blob_name)
    destination_file_name = f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}'
    blob.download_to_filename(destination_file_name)

def upload_audio_features_csv():
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    destination_file_name = f'{params.AUDIO_FEATURES_FOLDER}/{params.AUDIO_FEATURES_FILE}'
    blob = bucket.blob(destination_file_name)
    source_file_name = f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}'
    blob.upload_from_filename(source_file_name)
  
def get_youtube_wav(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_blob_name = f'{params.YT_DOWNLOAD_FOLDER}{file}'
    blob = bucket.blob(source_blob_name)
    destination_file_name = f'{params.TEMP_DATA_FOLDER}/{file}'
    blob.download_to_filename(destination_file_name)
    
def upload_stems(folder):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_folder_name = f'{params.SPLIT_DATA_FOLDER}{folder}'
    for filename in os.listdir(source_folder_name):
        destination_file_name = f'{params.STEMS_FOLDER}/{folder}/{filename}'
        blob = bucket.blob(destination_file_name)
        source_file_name = f'{source_folder_name}/{filename}'
        print(source_file_name)
        blob.upload_from_filename(source_file_name)
        
def get_stems(folder):
    if not os.path.exists(f'{params.TEMP_STEMS_FOLDER}{folder}/'):
        os.mkdir(f'{params.TEMP_STEMS_FOLDER}{folder}/')
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_blob_name = f'{params.STEMS_FOLDER}/{folder}'
    blobs = bucket.list_blobs(prefix=source_blob_name)
    for blob in blobs:
        file = blob.name.replace("data/stems/", "")
        print(file)
        destination_file_name = f'{params.TEMP_STEMS_FOLDER}/{file}'
        blob.download_to_filename(destination_file_name)
        
def upload_mixed_audio(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    destination_file_name = f'{params.MIXED_FOLDER}/{file}'
    blob = bucket.blob(destination_file_name)
    source_file_name = f'{params.MIXED_AUDIO_FOLDER}/{file}'
    blob.upload_from_filename(source_file_name)
    
def get_mixed_audio(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    source_blob_name = f'{params.MIXED_FOLDER}/{file}'
    blob = bucket.blob(source_blob_name)
    destination_file_name = f'{params.TEMP_MIXED_FOLDER}/{file}'
    blob.download_to_filename(destination_file_name)
  
## TEST ##
#file = "Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30.wav"
# file = "64_kygo_combined2.wav"
# #folder = "Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30"
# get_mixed_audio(file)
## TEST ##