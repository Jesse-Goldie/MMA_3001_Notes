"""Generate noisy images and produce an averaged (denoised) image.

This module provides a small script-style entry point that uses two helper
modules to generate a set of noisy images in a directory and then compute
their pixel-wise average to create a denoised output image.

The primary behavior is executed when the module is run as a script:
1. generate_noisy_images creates a number of noisy images in an output
   directory.
2. average_images reads the images from that directory and writes a single
   averaged image to disk.

Dependencies:
    - generator.generate_noisy_images(output_dir: str, n_images: int)
    - averager.average_images(input_dir: str, output_path: str)

Args (script-level variables used when run as __main__):
    output_dir (str): Directory where noisy images will be written. Default:
        "generated_images".
    n_images (int): Number of noisy images to generate. Default: 30.
    output_path (str): File path for the averaged output image. Default:
        "denoised.png".

Raises:
    Any exceptions raised by generator.generate_noisy_images or
    averager.average_images (for example, file I/O or image processing
    errors) are propagated to the caller.

Example:
    Run from the command line:
        python main.py
"""

from generator import generate_noisy_images
from averager import average_images

if __name__ == "__main__":
    output_dir = "generated_images"
    generate_noisy_images(output_dir, n_images=30)
    average_images(output_dir, output_path="denoised.png")
