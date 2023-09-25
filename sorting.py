from PIL import Image
import glob
import random

MAX_THRESHOLD = 0.8
MIN_THRESHOLD = 0.2
ROW = False
REVERSED = True

random_nasa_picture = random.choice(glob.glob("/home/user/nasapictures/*.*"))
image = Image.open(random_nasa_picture)
width, height = image.size
pixels = image.load()

ARRAY = {i: [] for i in range(height if ROW else width)}
START = -1
END = -1

for i in range(height if ROW else width):
    for o in range(width if ROW else height):
        pixel = pixels[o, i] if ROW else pixels[i, o]
        pixel = list(map(lambda x: x / 255, pixel))
        brightness = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
        if brightness > MIN_THRESHOLD and MAX_THRESHOLD > brightness:
            if START == -1:
                START = o
            END = o
        elif START != -1:
            if START != END:
                ARRAY[i].append((START, END))
            START = -1
            END = -1
    if START != -1:
        if START != END:
            ARRAY[i].append((START, END))
        START = -1
        END = -1

for i in ARRAY:
    for line in ARRAY[i]:
        start, end = line
        pixel_array = []
        for o in range(start, end):
            pixel_array.append(pixels[o, i] if ROW else pixels[i, o])
        pixel_array = sorted(pixel_array, key=lambda pixel: 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2], reverse=REVERSED)
        for o, pixel in zip(range(start, end), pixel_array):
            image.putpixel((o, i) if ROW else (i, o), pixel)

image.show()