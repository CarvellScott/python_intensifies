# PYTHON INTENSIFIES

## Description

A command-line tool for INTENSIFYING images. That is, it opens a file and SHAKES IT VIGOROUSLY. Mostly used for memes.

## Requirements

Pretty much Python3.5+ and pillow. The setup.py should install it for you.

## Installation

    $ pip install .

## Usage:
    
    $ intensify -h

	usage: intensify [-h] [-i IMAGE] [-o OUTPUT] [-s MAX_LENGTH] [-w WIGGLE_LEVEL]

	optional arguments:
	  -h, --help            show this help message and exit
	  -i IMAGE, --image IMAGE
							The image to be INTENSIFIED. Defaults to README.md
	  -o OUTPUT, --output OUTPUT
							The filename to which the output should be saved. Must
							end in ".gif"
	  -s MAX_LENGTH, --max_length MAX_LENGTH
							The output will have dimensions no bigger than this
							value.
	  -w WIGGLE_LEVEL, --wiggle_level WIGGLE_LEVEL
							Amount of shaking on a scale of 0 to 1.

    $ intensify -i python.jpg -w .25 -o danger_noodle.gif


## Changelog
    0.0.1 - 0.0.2:
        * Transparency AND animation is now supported for .gif files used as input.
        * MoviePy, (and by extension, imageio, tqdm, and a copy of ffmpeg) are no longer dependencies.
        * No need for a folder as a package, setup.py just installs a single module now.

## Notes
    * Transparency for .png files used as input is not supported.
