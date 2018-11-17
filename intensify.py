#!/usr/bin/env python
import os
import argparse
import random
from PIL import Image, ImageSequence


def _get_crop_frame(image, max_wiggle, tx, ty):
    """
    Based on on the max_wiggle, determines a cropping frame.
    """
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


def _shake_frame(img, max_wiggle):
    tx = random.random()
    ty = random.random()
    cropped = img.crop(_get_crop_frame(img, max_wiggle, tx, ty))
    return cropped


def main():
    # Use the most recently added file to the directory as a default input.
    files = [f for f in os.listdir() if os.path.isfile(f)]
    files_and_times = zip(files, map(lambda i: os.path.getmtime(i), files))
    mr_file = max(files_and_times, key=lambda i: i[1])[0]
    default_output_file = os.path.splitext(mr_file)[0] + "-intensifies.gif"

    # Use those defaults to minimize number of required arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--image",
        type=argparse.FileType("rb"),
        default=mr_file,
        help="The image to be INTENSIFIED. Defaults to {}".format(mr_file)
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=default_output_file,
        help=("The filename to which the output should be saved. "
              "Must end in \".gif\"")
    )
    parser.add_argument(
        "-s",
        "--max_length",
        type=int,
        required=False,
        default=0,
        help="The output will have dimensions no bigger than this value."
    )
    parser.add_argument(
        "-w",
        "--wiggle_level",
        type=float,
        required=False,
        default=.1875,
        help="Amount of shaking on a scale of 0 to 1."
    )
    parser.add_argument(
        "-f",
        "--fps",
        type=int,
        required=False,
        default=50,
        help="Frame rate of the output in frames per second. Max is 50."
    )
    args = parser.parse_args()

    input_pic = Image.open(args.image)
    wiggle_level = args.wiggle_level
    fps = max(1, min(50, args.fps))
    print("Intensifying image, please wait...")

    # SHAKE VIGOROUSLY
    # ...I really want to shake ImageSequence.Iterator vigorously for how it
    # doesn't get along with lists very well.
    sequence = ImageSequence.Iterator(input_pic)
    frames = [im.copy() for im in sequence]
    if len(frames) > 1:
        frames = [_shake_frame(im, wiggle_level) for im in frames]
    else:
        frames = [_shake_frame(frames[0], wiggle_level) for i in range(fps)]

    # Shrink the pic to requested size
    input_pic_width, input_pic_height = input_pic.size
    max_length = max(input_pic_width, input_pic_height)
    desired_length = args.max_length
    scaled_w = scaled_h = 1
    if max_length > desired_length and desired_length > 0:
        visibility = (1 - wiggle_level / 2)
        scale_factor = desired_length / (visibility * max_length)
        scaled_w = int(scale_factor * input_pic_width)
        scaled_h = int(scale_factor * input_pic_height)

    if scaled_w != 1 or scaled_h != 1:
        scaled_size = (scaled_w, scaled_h)
        frames = [im.resize(scaled_size, Image.NEAREST) for im in frames]

    # PIL saves gifs weirdly, but I'll deal with it.
    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=(1000 // fps),
        loop=0,
        disposal=3
    )


if __name__ == "__main__":
    main()
