from __future__ import unicode_literals
import youtube_dl

class YoutubeDownloader:
    
    def __init__(self, yt_link):
        self.yt_link = yt_link
        self.ydl_opts = {
            'outtmpl': 'ai_dj/data/downloaded_music/%(title)s-%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }],
        }
        
    def download_song(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.yt_link])


    def download_metadata(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            meta = ydl.extract_info(self.yt_link, download=False)
        title = meta["title"]
        song_id = meta["id"]
        output_filename = f'{title}-{song_id}.wav'
        return title, song_id, output_filename, self.yt_link
    
def download_wav_and_metadata(yt_link):
    ydl_opts = {
        'outtmpl': 'ai_dj/data/downloaded_music/%(title)s-%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
            }],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_link])
        meta = ydl.extract_info(yt_link, download=False)
    title = meta["title"]
    song_id = meta["id"]
    output_filename = f'{title}-{song_id}.wav'
    return title, output_filename