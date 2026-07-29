import numpy as np
from PIL import Image
import os
from glob import glob

def average_images(input_dir: str, output_path: str = "averaged.png"):
    files = sorted(glob(os.path.join(input_dir, "*.png")))
    if not files:
        raise ValueError("No PNG images found in directory.")
    first = np.array(Image.open(files[0]), dtype=np.float64)
    accumulator = np.zeros_like(first)
    for f in files:
        accumulator += np.array(Image.open(f), dtype=np.float64)
    averaged = (accumulator / len(files)).astype(np.uint8)
    out_img = Image.fromarray(averaged)
    out_img.save(output_path)
    print(f"Averaged image saved to {output_path}")
