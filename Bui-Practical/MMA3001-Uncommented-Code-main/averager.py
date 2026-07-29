"""The code generates a set of noisy PNG images 
(via generate_noisy_images from generator.py) and then computes 
a pixel-wise average of all PNGs in a directory to produce a single 
"averaged" image (used as a simple denoised result). 
Running main.py will create 30 images in generated_images and save 
the averaged output as denoised.png."""

import numpy as np
from PIL import Image
import os
from glob import glob

def average_images(input_dir: str, output_path: str = "averaged.png"):
    #Finds all PNG files in given input directory and sorts them
    files = sorted(glob(os.path.join(input_dir, "*.png")))
    if not files:
        #Raises error if no PNGs are found
        raise ValueError("No PNG images found in directory.")

    #Opens first image and converts it to a dtype float64NumPy array  
    #to get shape and initialise accumalator array
    first = np.array(Image.open(files[0]), dtype=np.float64)
    accumulator = np.zeros_like(first)

    #Loops through PNG files, opens each, converts it to a float64 NumPy 
    #array 
    for f in files:
        accumulator += np.array(Image.open(f), dtype=np.float64)

    #Divides accumulator by number of files to compute the pixel-wise mean,
    #casts, the restuls back to a uint8, converts it back to a PIL image and
    #saves it to the output path
    averaged = (accumulator / len(files)).astype(np.uint8)
    out_img = Image.fromarray(averaged)
    out_img.save(output_path)
    
    print(f"Averaged image saved to {output_path}")
