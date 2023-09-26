import pyaudio
from PIL import Image, ImageDraw
import pygame
import numpy as np

import random
import struct

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()

def display_image(image: Image.Image, db):
    screen.blit(
        pygame.image.fromstring(image.tobytes(), image.size, image.mode), (0, 0)
    )
    pygame.display.update()
    # clock.tick(max(db // 2, 1))

img_height = 1080
img_width = 1920

img = Image.new("RGB", (1920, 1080))
draw = ImageDraw.Draw(img)


CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

window = np.blackman(CHUNK)


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

try:
    while True:
        data = stream.read(CHUNK)
        # print(len(data))
        # data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
        # data_int = list(map(lambda x: int(x / 2), data_int))
        """        R = data_int[data_int[0]]
                G = data_int[data_int[1]]
                B = data_int[data_int[2]]
                X = data_int[data_int[3]] + data_int[data_int[4]] + data_int[data_int[5]] + data_int[data_int[6]] + data_int[data_int[7]] + data_int[data_int[8]] + data_int[data_int[9]] + data_int[data_int[10]]
                Y = data_int[data_int[11]] + data_int[data_int[12]] + data_int[data_int[13]] + data_int[data_int[14]]
                XX = data_int[data_int[15]] + data_int[data_int[16]] + data_int[data_int[17]] + data_int[data_int[18]] + data_int[data_int[19]] + data_int[data_int[20]] + data_int[data_int[21]] + data_int[data_int[22]]
                YY = data_int[data_int[23]] + data_int[data_int[24]] + data_int[data_int[25]] + data_int[data_int[26]]
                WIDTH = data_int[data_int[27]]
        """        
        
        indata = np.array(struct.unpack("%dh" % (len(data) / 2), data)) * window
        fftData = abs(np.fft.rfft(indata)) ** 2
        which = fftData[1:].argmax() + 1
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1 : which + 2 :])
            x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 - y0)
            thefreq = (which + x1) * RATE / CHUNK
            # print(f"The freq IS {thefreq} Hz.")
        else:
            thefreq = which * RATE / CHUNK
            # print(f"The freq {thefreq} Hz.")
        audio_data = np.frombuffer(data, dtype=np.int16)  # Convert audio data to NumPy array
        normalized_audio = audio_data / 32768.0
        rms = np.sqrt(np.mean(normalized_audio**2))
        db = 100 - abs(20 * np.log10(rms))
        # print(f"dB Level: {db:.2f} dB")
        if np.isnan(thefreq):
            continue
        R = G = B = int(db) * 3
        # print(R)
        db = int(db)
        thefreq = abs(int(thefreq))
        if random.randint(0, 1):
            draw.ellipse((thefreq, random.randint(0, 1080), random.randint(thefreq, thefreq * 2), random.randint(0, 1080)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=int(db))
        else:
            draw.line((thefreq, random.randint(0, 1080), random.randint(thefreq, thefreq * 2), random.randint(0, 1080)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=int(db))
        display_image(img, db)
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()

p.terminate()
pygame.quit()

"""import wave
import sys

import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

with wave.open('output.wav', 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

    print('Recording...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        wf.writeframes(stream.read(CHUNK))
    print('Done')

    stream.close()
    p.terminate()"""