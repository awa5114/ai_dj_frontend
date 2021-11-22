from spleeter.separator import Separator
from ai_dj.params import DOWNLOADED_FOLDER
from ai_dj import gcp_storage
import madmom
import librosa

def split_tracks(audio_files, n_stems, start=0):
    mix_data = {}
    for audio_file in audio_files:
        mix_data[audio_file] = {}

        # load audio with madmom
        audio_file = str(audio_file)
        file_path = f'{DOWNLOADED_FOLDER}/{audio_file}'
        stop = start+60
        audio, sr = madmom.io.audio.load_ffmpeg_file(file_path, sample_rate=44100, dtype=float, num_channels=2, start=start, stop=stop)
        audio = madmom.audio.signal.normalize(audio)
        
        # beat tracking
        proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
        act = madmom.features.beats.RNNBeatProcessor()(file_path)
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