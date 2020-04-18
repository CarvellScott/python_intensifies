# PYTHON INTENSIFIES

## Description

A command-line tool for INTENSIFYING images. That is, it opens a file and SHAKES IT VIGOROUSLY. Mostly used for memes.

## Requirements

Pretty much Python3.5+ and Pillow. The setup.py should install it for you.

## Installation
`$ pip install python-intensifies`

## Usage:

This is basically a command-line tool; just supply a list of images as input. Each of the output images will end in `-intensifies.gif`.
`$ intensify input0.png input1.png input2.png`

The "wiggle level" can be set anywhere between 0.0 to 1.0. The more wiggle, the more intense the shaking, however the image(s) will be zoomed in to ensure no borders show.
`$ intensify -w .25 input0.png input1.png input2.png`

## Changelog
    0.1.0 - 0.2.0:
        * Upgraded Pillow to 7.0.0.
    0.0.4 - 0.1.0:
        * Added support for bulk intensification; instead of specifying input via -i, multiple files can be specified at the command line.
		* Removed the "--output" argument. Every output now follows a convention of "*-intensifies.gif".
		* Fixed a bug that prevented images from resizing correctly.
        * Fixed a minor security issue as a result of not using the latest Pillow.
    0.0.3 - 0.0.4:
        * If you're reading this, you can now install this via pypi.
    0.0.2 - 0.0.3:
        * Re-added the FPS parameter I forgot to document removing. Initially it was because Pillow is limited in framerates it can animate, but turns out it's very useful for reducing filesize of emojis.
    0.0.1 - 0.0.2:
        * Transparency AND animation is now supported for .gif files used as input.
        * MoviePy, (and by extension, imageio, tqdm, and a copy of ffmpeg) are no longer dependencies.
        * No need for a folder as a package, setup.py just installs a single module now.

## Notes
    * Transparency for .png files used as input is not supported.
