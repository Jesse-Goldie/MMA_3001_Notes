"""
Simple utility to generate noisy images containing the text "MMA3001".

This module creates RGB PNG images with centered text, adds Gaussian noise,
and writes the noisy images to a specified output directory.

The main function is `generate_noisy_images`.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


def generate_noisy_images(
    output_dir: str,
    n_images: int = 20,
    width: int = 800,
    height: int = 400,
    noise_level: float = 0.25
):
    """Generate and save noisy images with the text 'MMA3001' centered.

    This function creates `n_images` RGB images of the given `width` and `height`
    with white background and black centered text "MMA3001". It adds Gaussian
    noise to each image (noise standard deviation is proportional to 255 * noise_level)
    and saves each noisy image as a PNG file in `output_dir` named noisy_###.png.

    Args:
        output_dir (str): Path to directory where images will be saved. Directory
            will be created if it does not exist.
        n_images (int, optional): Number of images to generate. Defaults to 20.
        width (int, optional): Image width in pixels. Defaults to 800.
        height (int, optional): Image height in pixels. Defaults to 400.
        noise_level (float, optional): Relative noise magnitude. Typical values are
            between 0 (no noise) and ~1 (very noisy). Defaults to 0.25.

    Returns:
        None: Images are written to disk. The function prints a short summary on completion.

    Raises:
        OSError: If the output directory cannot be created (e.g., permissions error).
        Any exceptions from PIL.ImageFont.truetype may be suppressed by falling back to
        a default font; other unexpected exceptions are not explicitly handled here.

    Example:
        generate_noisy_images("out_images", n_images=10, width=640, height=480, noise_level=0.2)
    """
    # Ensure the output directory exists. exist_ok=True avoids error if it already exists.
    os.makedirs(output_dir, exist_ok=True)

    # Try to load a common TrueType font. If unavailable, fall back to PIL's default bitmap font.
    # Using a TrueType font gives better control over size and metrics.
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except Exception:
        font = ImageFont.load_default()

    # Main generation loop
    for i in range(n_images):
        # Create a new white RGB image with the requested dimensions.
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)

        # Text to draw and get its bounding box to center it.
        text = "MMA3001"
        # textbbox returns (left, top, right, bottom) for the provided anchor point (0,0).
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Compute position to center the text within the image.
        pos = ((width - text_w) // 2, (height - text_h) // 2)

        # Draw the text in black onto the white background.
        draw.text(pos, text, fill="black", font=font)

        # Create Gaussian noise:
        # - np.random.randn generates samples from standard normal (mean=0, std=1).
        # - Multiply by 255 to scale into the 0-255 image space, then by noise_level.
        # The resulting array has shape (height, width, 3) for RGB channels.
        noise = np.random.randn(height, width, 3) * 255 * noise_level

        # Convert PIL image to numpy array, add noise, clip to [0, 255], then convert back to uint8.
        noisy = np.clip(np.array(img) + noise, 0, 255).astype(np.uint8)

        # Convert back to a PIL Image and save as PNG using a zero-padded index in the filename.
        noisy_img = Image.fromarray(noisy)
        noisy_img.save(os.path.join(output_dir, f"noisy_{i:03d}.png"))

    # Summary printout for the user.
    print(f"Generated {n_images} noisy images in {output_dir}")
