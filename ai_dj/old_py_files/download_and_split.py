import youtube_dl
from spleeter.separator import Separator
import os

def download(links):
    ydl_args = {
        'outtmpl': 'ai_dj/data/%(title)s.%(ext)s',
        'extractaudio': True,
        'format': 'bestaudio',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }
            ],
        }
    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        results = ydl.download(links)


    filepaths = []
    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        for link in links:
            filepath = ydl.prepare_filename(ydl.extract_info(link))
            filepaths.append(filepath)
    return filepaths 

def separate():
    separator = Separator('spleeter:5stems')
    for filepath in filepaths:
        separator.separate_to_file(filepath, 'data')


if __name__=="__main__":
    links = [
        "https://www.youtube.com/watch?v=SF8DGbfOFig",
        "https://www.youtube.com/watch?v=Q77vdqA0hnM",
        "https://www.youtube.com/watch?v=1zmxNRc1FXY&ab_channel=MyLifelikeaSoundtrackMyLifelikeaSoundtrack",
        "https://www.youtube.com/watch?v=VIeY1J1M9Ts&ab_channel=VanillaVanilla",
        "https://www.youtube.com/watch?v=L-2CyO8pc0E",
        "https://www.youtube.com/watch?v=xarC5jAiO7w",
        "https://www.youtube.com/watch?v=q5rliCxX8xc",
        "https://www.youtube.com/watch?v=deIhypT_55A",
        "https://www.youtube.com/watch?v=SKUk9RUacDQ",
        "https://www.youtube.com/watch?v=nXOSgekiAJc"
    ]  
    filepaths = download(links)
