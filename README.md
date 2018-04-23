# PYTHON INTENSIFIES

## Description

A command-line tool for INTENSIFYING images. (That is, it opens a file and SHAKES VIGOROUSLY)

## Requirements

So far the script has been tested on Python3.5 running in the Windows Subsystem for Linux. The only requirement is moviepy, though moviepy may have its own additional requirements.

## Installation

    $ pip install .

## Usage:
    
    $ intensify -h
    usage: intensify [-h] -i IMAGE -o OUTPUT [-s MAX_SIDE_LENGTH]
                     [-w WIGGLE_LEVEL]

    optional arguments:
      -h, --help            show this help message and exit
      -i IMAGE, --image IMAGE
                            The image to be INTENSIFIED
      -o OUTPUT, --output OUTPUT
                            The filename to which the output should be saved
      -s MAX_SIDE_LENGTH, --max_side_length MAX_SIDE_LENGTH
                            Ensures the output has dimensions no bigger than this
                            value.
      -w WIGGLE_LEVEL, --wiggle_level WIGGLE_LEVEL
                            Amount of shaking on a scale of 0 to 1.


    $ intensify -i python.jpg -w .25 -o danger_noodle.gif

    [MoviePy] Building file danger_noodle.gif with imageio
     98%|███████████████████████████████████████████████████████████████████████████████▋ | 60/61 [00:02<00:00, 20.64it/s]

## Notes

* Choosing a smaller maximum side length will result in faster processing, as will higher wiggle level.
* Transparency is not supported yet.
