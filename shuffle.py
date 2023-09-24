from PIL import Image, ImageDraw, ImageFont, ImageGrab
import random
import pygame
import glob
import time
from functools import partial

FOLDER_WITH_PICTURES = "/home/user/nasapictures/"
FOLDER_WITH_FONTS = "/usr/share/fonts/"
INITIAL_IMAGE = "image2.png"

with open("shuffle.py", "r") as f:
    TEXT = f.read()

with open("russian_words.txt", "r") as f:
    RUSSIAN_WORDS = f.read().split("\n")

with open("english_words.txt", "r") as f:
    ENGLISH_WORDS = f.read().split("\n")


def display_image(image: Image.Image):
    screen.blit(
        pygame.image.fromstring(image.tobytes(), image.size, image.mode), (0, 0)
    )
    pygame.display.update()
    clock.tick(60)
    return random.randint(0, 10000) == 10000

def shuffle_pixels(image: Image.Image):
    width, height = image.size
    pixels = image.load()
    match random.randint(0, 2):
        case 0:
            for i in reversed(range(1, width * height)):
                j = random.randint(i, (width * height) - 1)
                x1, y1 = i % width, i // width
                x2, y2 = j % width, j // width
                pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

                if i % width == 0:
                    display_image(image)
        case 1:
            for i in range(1, width * height):
                j = random.randint(0, i)
                x1, y1 = i % width, i // width
                x2, y2 = j % width, j // width
                pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

                if i % width == 0:
                    display_image(image)
        case 2:
            for i in range(width * height):
                j = random.randint(0, (width * height) - 1)
                k = random.randint(0, (width * height) - 1)
                x1, y1 = k % width, k // width
                x2, y2 = j % width, j // width
                pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

                if i % width == 0:
                    display_image(image)


def shuffle_rows(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    array = [list(pixels[x, y] for x in range(width)) for y in range(height)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        j = random.randint(i, height - 1) if case else random.randint(0, i)
        array[i], array[j] = array[j], array[i]
        for x in reversed(range(width)) if case() else range(width):
            pixels[x, i], pixels[x, j] = pixels[x, j], pixels[x, i]
        if display_image(image):
            break


def shuffle_columns(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        j = random.randint(i, width - 1) if case else random.randint(0, i)
        for y in reversed(range(height)) if case() else range(height):
            pixels[i, y], pixels[j, y] = pixels[j, y], pixels[i, y]
        if display_image(image):
            break


def duplicate_rows(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    array = [list(pixels[x, y] for x in range(width)) for y in range(height)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    repeat = array[0]
    for i in reversed(range(height)) if case() else range(height):
        if random.randint(0, 20) == 20:
            repeat = array[i]
        for y in reversed(range(width)) if case() else range(width):
            pixels[y, i] = repeat[y]
        if display_image(image):
            break


def duplicate_columns(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    columns = [list(pixels[x, y] for y in range(height)) for x in range(width)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    repeat = columns[0]
    for i in reversed(range(width)) if case() else range(width):
        if random.randint(0, 20) == 20:
            repeat = columns[i]
        for y in reversed(range(height)) if case() else range(height):
            pixels[i, y] = repeat[y]
        if display_image(image):
            break


def sort_pixels_in_columns(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    columns = [list(pixels[x, y] for y in range(height)) for x in range(width)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        srtd = sorted(columns[i], reverse=case_2())
        for y in reversed(range(height)) if case() else range(height):
            pixels[i, y] = srtd[y]
        if display_image(image):
            break


def sort_pixels_in_row(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    array = [list(pixels[x, y] for x in range(width)) for y in range(height)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        srtd = sorted(array[i], reverse=case_2())
        for y in reversed(range(width)) if case() else range(width):
            pixels[y, i] = srtd[y]
        if display_image(image):
            break

def correct_sort_pixels_in_row(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    array = [list(pixels[x, y] for x in range(width)) for y in range(height)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        srtd = sorted(array[i], key=lambda x: sum(x), reverse=case_2())
        for y in reversed(range(width)) if case() else range(width):
            pixels[y, i] = srtd[y]
        if display_image(image):
            break

def correct_sort_pixels_in_columns(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    columns = [list(pixels[x, y] for y in range(height)) for x in range(width)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        srtd = sorted(columns[i], key=lambda x: sum(x), reverse=case_2())
        for y in reversed(range(height)) if case() else range(height):
            pixels[i, y] = srtd[y]
        if display_image(image):
            break

def sort_pixels_by_brightness_in_row(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    array = [list(pixels[x, y] for x in range(width)) for y in range(height)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        srtd = sorted(array[i], key=lambda x: 0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2], reverse=case_2())
        for y in reversed(range(width)) if case() else range(width):
            pixels[y, i] = srtd[y]
        if display_image(image):
            break

def sort_pixels_by_brightness_in_columns(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    columns = [list(pixels[x, y] for y in range(height)) for x in range(width)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        srtd = sorted(columns[i], key=lambda x: 0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2], reverse=case_2())
        for y in reversed(range(height)) if case() else range(height):
            pixels[i, y] = srtd[y]
        if display_image(image):
            break

def shuffle_colors_in_pixel_row(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        for j in reversed(range(height)) if case() else range(height):
            pixel = list(pixels[i, j])
            random.shuffle(pixel)
            pixels[i, j] = tuple(pixel)
        if display_image(image):
            break


def shuffle_colors_in_pixel_column(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        for j in reversed(range(width)) if case() else range(width):
            pixel = list(pixels[j, i])
            random.shuffle(pixel)
            pixels[j, i] = tuple(pixel)
        if display_image(image):
            break


def sort_colors_in_pixel_row(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        for j in reversed(range(height)) if case() else range(height):
            pixel = sorted(list(pixels[i, j]), reverse=case_2())
            pixels[i, j] = tuple(pixel)
        if display_image(image):
            break

def sort_colors_in_pixel_column(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        for j in reversed(range(width)) if case() else range(width):
            pixel = sorted(list(pixels[j, i]), reverse=case_2())
            pixels[j, i] = tuple(pixel)
        if display_image(image):
            break

def reverse_pixels_in_row(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    array = [list(pixels[x, y] for x in range(width)) for y in range(height)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, partial(random.choice, (True, False)))
    )
    for i in reversed(range(height)) if case() else range(height):
        rvrsd = list(reversed(array[i]))
        for y in reversed(range(width)) if case() else range(width):
            pixels[y, i] = rvrsd[y] if case_2() else array[i][y]
        if display_image(image):
            break

def reverse_pixels_in_columns(image: Image.Image):
    pixels = image.load()
    width, height = image.size
    columns = [list(pixels[x, y] for y in range(height)) for x in range(width)]
    case = random.choice(
        (lambda: True, lambda: False, partial(random.choice, (True, False)))
    )
    case_2 = random.choice(
        (lambda: True, partial(random.choice, (True, False)))
    )
    for i in reversed(range(width)) if case() else range(width):
        rvrsd = list(reversed(columns[i]))
        for y in reversed(range(height)) if case() else range(height):
            pixels[i, y] = rvrsd[y] if case_2() else columns[i][y]
        if display_image(image):
            break

def shuffle_image(image_path: str):
    global screen, clock

    image = Image.open(image_path)
    image = image.resize((1920, 1080))

    pygame.init()
    screen = pygame.display.set_mode(image.size, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pictures = glob.glob(FOLDER_WITH_PICTURES + "/*.*")
    while True:
        effect = random.choice(
            (
                shuffle_rows,
                shuffle_columns,
                shuffle_pixels,
                duplicate_columns,
                duplicate_rows,
                sort_pixels_in_row,
                sort_pixels_in_columns,
                correct_sort_pixels_in_row,
                correct_sort_pixels_in_columns,
                sort_pixels_by_brightness_in_columns,
                sort_pixels_by_brightness_in_row,
                shuffle_colors_in_pixel_row,
                shuffle_colors_in_pixel_column,
                sort_colors_in_pixel_row,
                sort_colors_in_pixel_column,
                reverse_pixels_in_row,
                reverse_pixels_in_columns,
            )
        )
        effect(image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    image.save(f"{int(time.time())}.png")

        if random.randint(0, 2) == 0:
            for i in range(random.randint(3, 15)):
                if random.randint(0, 2) == 0:
                    picture = ImageGrab.grab().resize(
                        (
                            random.randint(1, image.width),
                            random.randint(1, image.height),
                        )
                    )
                else:
                    picture = Image.open(random.choice(pictures)).resize(
                        (
                            random.randint(1, image.width),
                            random.randint(1, image.height),
                        )
                    )
                x = random.randint(0, image.width)
                y = random.randint(0, image.height)
                image.paste(picture, (x, y))
                display_image(image)
                if random.randint(0, 5) == 5:
                    xx = random.randint(-50, 50)
                    yy = random.randint(-50, 50)
                    for o in range(random.randint(1, 10)):
                        x += xx
                        y += yy
                        image.paste(picture, (x, y))
                        display_image(image)
        if random.randint(0, 2) == 0:
            for i in range(random.randint(1, 10)):
                match random.randint(0, 2):
                    case 0:
                        start = random.randint(0, len(TEXT.split("\n")) - 1)
                        end = random.randint(start, len(TEXT.split("\n")))
                        text = "\n".join(TEXT.split("\n")[start:end])
                    case 1:
                        text = random.choice(("\n", "", " ")).join(
                            random.choice(ENGLISH_WORDS)
                            for i in range(random.randint(1, 15))
                        )
                    case 2:
                        text = random.choice(("\n", "", " ")).join(
                            random.choice(RUSSIAN_WORDS)
                            for i in range(random.randint(1, 15))
                        )
                try:
                    font = ImageFont.FreeTypeFont(
                        random.choice(
                            glob.glob(FOLDER_WITH_FONTS + "/*/*.ttf", recursive=True)
                        ),
                        random.randint(10, 25),
                        encoding="utf-8",
                    )
                    ImageDraw.ImageDraw(image).text(
                        (
                            random.randint(-image.width // 2, image.width),
                            random.randint(-image.height // 2, image.height),
                        ),
                        text,
                        font=font,
                        fill=(
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255),
                        ),
                    )
                except Exception as e:
                    ...
                display_image(image)


if __name__ == "__main__":
    shuffle_image(INITIAL_IMAGE)
