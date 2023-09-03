#!/usr/bin/env python
import argparse
import io
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


def _intensify_filename(filename):
    """
    Derives a filename used to save an intensified image.
    """
    input_filepath = pathlib.Path(filename)
    suffix = input_filepath.stem + "-intensifies"
    output_filename = suffix + ".gif"
    return output_filename


def intensify(image_fp, desired_length=0, wiggle_level=.1875, fps=50):
    """
    Reads in an image from the given file-like object and creates an animated
    gif in which it shakes vigorously.

    Arguments:
        image_fp (file): This is an open file-like object that holds the image
        data.
        desired_length (int): Represents the max length in pixels of the output
        image
        wiggle_level (float): A number between 0 and 1 that represents the
        maximum offset of the image between frames.
        fps (integer): frames per second of the output image.
    Returns:
        An io.BytesIO object containing the new gif, ready to be read.
    """
    random.seed("Determinism for the win")
    input_pic = Image.open(image_fp)
    fps = max(1, min(50, fps))
    wiggle_level = max(0, min(1, wiggle_level))

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

    output_fp = io.BytesIO()
    # PIL saves gifs weirdly, but I'll deal with it.
    frames[0].save(
        output_fp,
        format="gif",
        save_all=True,
        append_images=frames[1:],
        duration=(1000 // fps),
        loop=0,
        disposal=3
    )
    output_fp.seek(0)
    return output_fp


def _get_argument_parser():
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
    return parser


def _main():
    parser = _get_argument_parser()
    parsed_args = parser.parse_args()
    images = parsed_args.image
    for i, image_fp in enumerate(parsed_args.image):
        input_filename = image_fp.name
        progress_msg_fmt = "Intensifying image {}/{}, please wait..."
        print(progress_msg_fmt.format(i + 1, len(images)))
        intensified_fp = intensify(image_fp,
                                    desired_length=parsed_args.size,
                                    wiggle_level=parsed_args.wiggle_level,
                                    fps=parsed_args.fps)

        output_filename = _intensify_filename(input_filename)
        with open(output_filename, "wb") as f:
            f.write(intensified_fp.read())
        print("Output written to {}".format(output_filename))


if __name__ == "__main__":
    _main()
