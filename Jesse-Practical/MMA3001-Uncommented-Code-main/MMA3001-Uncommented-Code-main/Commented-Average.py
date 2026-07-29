import numpy as np
from PIL import Image
import os
from glob import glob

def average_images(input_dir: str, output_path: str = "averaged.png"):
    """
    Averages a series of PNG images in a directory and saves the result.

    This function reads all PNG files from the specified input directory,
    calculates the element-wise average of their pixel values, and saves
    the resulting averaged image to the specified output path.

    Args:
        input_dir (str): The path to the directory containing the PNG images.
        output_path (str, optional): The path where the averaged image will be saved.
                                     Defaults to "averaged.png".

    Raises:
        ValueError: If no PNG images are found in the specified directory.
    """
    # Get a sorted list of all PNG files in the input directory
    files = sorted(glob(os.path.join(input_dir, "*.png")))
    
    # Raise an error if no PNG files are found
    if not files:
        raise ValueError("No PNG images found in directory.")
    
    # Open the first image to get its dimensions and initialize the accumulator
    first = np.array(Image.open(files[0]), dtype=np.float64)
    accumulator = np.zeros_like(first)
    
    # Iterate through each image file, open it, convert to NumPy array, and add to accumulator
    for f in files:
        accumulator += np.array(Image.open(f), dtype=np.float64)
    
    # Calculate the average by dividing the accumulator by the total number of images
    # Convert the result back to unsigned 8-bit integer format (0-255)
    averaged = (accumulator / len(files)).astype(np.uint8)
    
    # Create a PIL Image object from the averaged NumPy array
    out_img = Image.fromarray(averaged)
    
    # Save the averaged image to the specified output path
    out_img.save(output_path)
    print(f"Averaged image saved to {output_path}")
