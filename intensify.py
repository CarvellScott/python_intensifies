#!/usr/bin/env python
import argparse
import pathlib
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


def _intensify(image_fp, parsed_args):
    desired_length = parsed_args.size
    wiggle_level = parsed_args.wiggle_level
    input_pic = Image.open(image_fp)
    fps = max(1, min(50, parsed_args.fps))

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
    curr_max_length = max(input_pic_width, input_pic_height)
    scaled_w = scaled_h = 1
    if curr_max_length > desired_length and desired_length > 0:
        scale_factor = desired_length / curr_max_length
        scaled_w = int(scale_factor * input_pic_width)
        scaled_h = int(scale_factor * input_pic_height)

    if scaled_w != 1 or scaled_h != 1:
        scaled_size = (scaled_w, scaled_h)
        frames = [im.resize(scaled_size, Image.NEAREST) for im in frames]

    # Derive output filename
    input_filepath = pathlib.Path(image_fp.name)
    suffix = input_filepath.stem + "-intensifies"
    output_filename = suffix + ".gif"

    # PIL saves gifs weirdly, but I'll deal with it.
    frames[0].save(
        output_filename,
        save_all=True,
        append_images=frames[1:],
        duration=(1000 // fps),
        loop=0,
        disposal=3
    )
    return output_filename


def intensify(parsed_args):
    for image_fp in parsed_args.image:
        input_filename = image_fp.name
        print("Intensifying {}, please wait...".format(input_filename))
        output_filename = _intensify(image_fp, parsed_args)
        print("Output written to {}".format(output_filename))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image",
        type=argparse.FileType("rb"),
        nargs="+",
        help="One or more images to be INTENSIFIED."
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        required=False,
        default=0,
        help=(
            "The output image(s) will be scaled down to have dimensions no"
            "bigger than this value (in pixels)."
        )
    )
    parser.add_argument(
        "-w",
        "--wiggle_level",
        type=float,
        required=False,
        default=.1875,
        help=(
            "Amount of shaking on a scale of 0.0 to 1.0. "
            "The more wiggle, the more the image will be zoomed in to ensure "
            "no borders show."
        )
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
    intensify(args)


if __name__ == "__main__":
    main()
