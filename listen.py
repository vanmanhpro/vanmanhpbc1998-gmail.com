import sounddevice as sd
import soundfile as sf
import sys

def async_playback(filename):
    data, sr = sf.read(filename)
    sd.play(data, sr)
    return data, sr

async_playback(f'vnexpress/thoi_su/cau_{sys.argv[1]}.wav')