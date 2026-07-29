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
    os.makedirs(output_dir, exist_ok=True)
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    for i in range(n_images):
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)
        text = "MMA3001"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pos = ((width - text_w) // 2, (height - text_h) // 2)
        draw.text(pos, text, fill="black", font=font)
        noise = np.random.randn(height, width, 3) * 255 * noise_level
        noisy = np.clip(np.array(img) + noise, 0, 255).astype(np.uint8)
        noisy_img = Image.fromarray(noisy)
        noisy_img.save(os.path.join(output_dir, f"noisy_{i:03d}.png"))

    print(f"Generated {n_images} noisy images in {output_dir}")
