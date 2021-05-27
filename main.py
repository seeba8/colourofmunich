#!/usr/local/bin/python3

import glob
import os
import shutil
import os.path
import urllib.request
import time
from PIL import Image, ImageDraw
from colorthief import ColorThief


def load_sky() -> str:
    print("loading image")
    if os.path.exists(os.sep.join([".", "img"])):
        shutil.rmtree(os.sep.join([".", "img"]))
    if not os.path.exists(os.sep.join([".", "img"])):
        os.mkdir(os.sep.join([".", "img"]))
    fname = os.sep.join([".", "img", "sky_" + str(int(time.time())) + ".jpg"])
    urllib.request.urlretrieve(
        "https://www.meteo.physik.uni-muenchen.de/DokuWiki/lib/exe/fetch.php?cache=&media=garching.jpg", fname)
    with Image.open(fname) as img:
        w, h = img.size

        # remove Munich
        img = img.crop((0, 25, w, h-150))
        img.save(fname)
    return fname


def get_sky() -> str:
    sky_list = glob.glob(os.sep.join([".", "img", "sky_*.jpg"]))
    if len(sky_list) == 0:
        return load_sky()
    else:
        filename = sky_list[0].split(os.sep)[-1]
        print(filename)
        try:
            timestamp = int(filename[4:-4])
            if timestamp < int(time.time()) - 60 * 30:
                return load_sky()
            else:
                return sky_list[0]
        except ValueError:
            return load_sky()


def show_dominant_colour(image_path):
    w, h = 400, 300
    colorthief = ColorThief(image_path)
    dominant = colorthief.get_color(quality=5)
    avg_img = Image.new("RGB", (w, h), dominant)
    avg_img.show()

def show_palette(image_path, count_colour=2):
    w, h = 400, 300
    colorthief = ColorThief(image_path)
    palette = colorthief.get_palette(quality=5, color_count=count_colour)
    avg_img = Image.new("RGB", (w, h), palette[0])
    draw = ImageDraw.Draw(avg_img)
    for i in range(1, len(palette)):
        draw.rectangle((int(i*w/len(palette)), 0,
                        int((i+1)*w/len(palette)) + 1, h),
                       fill=palette[i])
    avg_img.show()

def main():
    sky_path = get_sky()
    show_palette(sky_path)


if __name__ == '__main__':
    main()
