"""Utilities to average PNG images in a directory into a single image.

This module provides a single function, `average_images`, which computes a
pixel-wise mean of all PNG images in a directory and writes the resulting
image to disk.

Note:
    The function assumes all images have the same dimensions and number of
    channels. If image modes differ (for example, some images are "RGBA" and
    others are "RGB"), errors or unexpected results may occur. The function
    accumulates pixel values in float64 to avoid overflow before converting
    back to uint8 for saving.
"""

import numpy as np
from PIL import Image
import os
from glob import glob


def average_images(input_dir: str, output_path: str = "averaged.png"):
    """Compute the pixel-wise average of all PNG images in a directory.

    This function searches for PNG files in ``input_dir``, loads each image
    as a NumPy array with dtype ``float64`` (to avoid overflow while
    accumulating), computes the mean across images for every pixel, converts
    the result back to ``uint8``, and saves the averaged image to
    ``output_path``.

    Args:
        input_dir (str): Path to the directory containing PNG images.
        output_path (str): Path where the averaged image will be saved.
            Defaults to ``"averaged.png"``.

    Raises:
        ValueError: If no PNG images are found in ``input_dir``.

    Returns:
        None: The averaged image is written to disk at ``output_path``.

    Example:
        >>> average_images("generated_images", output_path="denoised.png")

    Notes:
        - All input images must share the same shape (height, width, channels).
        - The function does not perform any explicit mode conversion; to be
          robust across modes, convert images to a common mode (e.g. "RGB")
          before calling this function.
    """

    files = sorted(glob(os.path.join(input_dir, "*.png")))
    if not files:
        raise ValueError("No PNG images found in directory.")

    # Use the first image to determine the shape and datatype for accumulation.
    first = np.array(Image.open(files[0]), dtype=np.float64)
    accumulator = np.zeros_like(first)

    for f in files:
        accumulator += np.array(Image.open(f), dtype=np.float64)

    averaged = (accumulator / len(files)).astype(np.uint8)
    out_img = Image.fromarray(averaged)
    out_img.save(output_path)

    print(f"Averaged image saved to {output_path}")
