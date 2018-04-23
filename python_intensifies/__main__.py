#!/usr/bin/env python
import argparse
import random
import sys
import numpy as np
import moviepy.editor as mpy
from PIL import Image, ImageDraw

def lerp(a, b, t):
    return (1 - t) * a + t * b


def get_crop_frame(image, max_wiggle, tx, ty):
    pic_width, pic_height = image.size
    wiggle_room_x = max_wiggle * .5 * pic_width
    wiggle_room_y = max_wiggle * .5 * pic_height
    cropped_width = pic_width - wiggle_room_x
    cropped_height = pic_height - wiggle_room_y

    left = int(tx * wiggle_room_x)
    top = int(ty * wiggle_room_y)
    right = left + cropped_width
    bottom = top + cropped_height

    return left, top, right, bottom


class ImageShaker:
    def __init__(self):
        self.img = None
        self.max_wiggle = .1875

    def make_frame(self, progress):
        img = self.img
        max_wiggle = self.max_wiggle
        tx = random.random()
        ty = random.random()
        cropped = img.crop(get_crop_frame(img, max_wiggle, tx, ty))
        return np.array(cropped)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", type=argparse.FileType("rb"), required=True, help="The image to be INTENSIFIED")
    parser.add_argument("-o", "--output", type=str, required=True, help="The filename to which the output should be saved")
    parser.add_argument("-s", "--max_side_length", type=int, required=False, default=0, help="Ensures the output has dimensions no bigger than this value.")
    parser.add_argument("-w", "--wiggle_level", type=float, required=False, default=.1875, help="Amount of shaking on a scale of 0 to 1.")
    args = parser.parse_args()

    testpic = Image.open(args.image)
    
    testpic_width, testpic_height = testpic.size
    max_side_length = max(testpic_width, testpic_height)
    wiggle_level = args.wiggle_level
    desired_max_side_length = args.max_side_length
    if max_side_length > desired_max_side_length and desired_max_side_length > 0:
        visible_percentage_of_image = (1 - wiggle_level / 2)
        scale_factor = desired_max_side_length / (visible_percentage_of_image * max_side_length)
        scaled_size = (int(scale_factor * testpic_width), int(scale_factor * testpic_height))
        testpic = testpic.resize(scaled_size, Image.BILINEAR)

    shaker = ImageShaker()
    shaker.img = testpic
    shaker.max_wiggle = wiggle_level 
    duration = 1
    clip = mpy.VideoClip(shaker.make_frame, duration=duration)
    clip.write_gif(args.output, fps=60, opt="OptimizePlus", fuzz=10)


if __name__ == "__main__":
    main()
