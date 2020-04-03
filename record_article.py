import queue
import sys
import os

import sounddevice as sd
import soundfile as sf
import numpy

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


def record(wave_file, sentence, text_file, name):
    try:
        # Make sure the file is opened before recording anything:
        with sf.SoundFile(wave_file, mode='x', samplerate=22000, channels=1) as file:
            with sd.InputStream(samplerate=22000, device=sd.default.device, channels=1, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(wave_file))

    file = open(text_file, "+a")
    file.write(name + '\n')
    file.write(sentence + '\n')
    file.close()


name = 'cau_10.wav'
text_file = 'vnexpress/so_hoa/so_hoa.txt'
sentence = 'Cô đã gọi tổng đài và được khuyên là "khởi động lại modem", nhưng trình trạng vẫn không cải thiện nhiều'
wave_file = 'vnexpress/so_hoa/' + name
if os.path.exists(wave_file):
    os.remove(wave_file)

if not os.path.isdir(os.getcwd() + '/vnexpress/so_hoa'):
    os.mkdir(os.getcwd() + '/vnexpress/so_hoa')

record(wave_file, sentence, text_file, name)