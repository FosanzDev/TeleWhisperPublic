from pydub import AudioSegment
from io import BytesIO
import mutagen
import os 

abs_path = os.path.abspath(os.path.abspath(os.curdir))

async def ogg_to_mp3(filename):
    # print(abs_path)
    ogg_file = AudioSegment.from_file(filename, format="ogg")
    ogg_file.export(os.path.splitext(filename)[0]+'.mp3', format="mp3")


async def auto_to_mp3(filename, fileExtension):
    try:
        if fileExtension == 'ogg':
            ogg_to_mp3(filename)
            return 0
        
        elif fileExtension == 'mp3':
            return 0
        
        elif fileExtension == 'opus':
            opusFile = BytesIO(open(filename, 'rb').read())
            file = AudioSegment.from_file(opusFile, codec='opus')
            file.export(f'{filename}.mp3', format="mp3")
            return 0

        file = AudioSegment.from_file(filename, format=fileExtension)
        file.export(f'{filename}.mp3', format="mp3")
        return 0
    except mutagen.MutagenError:
        return 1