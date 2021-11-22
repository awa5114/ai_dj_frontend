from ai_dj import gcp_storage
from os import path
from pydub import AudioSegment
from pydub.playback import play
from ai_dj.params import DOWNLOADED_FOLDER, TEMP_DATA_FOLDER

def convert_mp3_to_wav(file):
    # change file extension for output file
    gcp_storage.get_mp3(file)
    output_file = file.replace(f'{TEMP_DATA_FOLDER}/', "").replace("mp3", "wav")    
    #convert from mp3 to wav                                                    
    sound = AudioSegment.from_mp3(f'{TEMP_DATA_FOLDER}/{file}')
    sound.export(f'{DOWNLOADED_FOLDER}/{output_file}', format="wav")
    return output_file