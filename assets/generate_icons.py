#!/usr/bin/env python3
"""
Generates native .ico and .icns icons for Windows and macOS builds.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw

def create_app_icon():
    base_dir = Path(__file__).resolve().parent.parent
    resources_dir = base_dir / "src" / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)

    # Master high-res canvas
    size = (1024, 1024)
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    draw.ellipse([32, 32, 992, 992], fill=(30, 41, 59, 255), outline=(99, 102, 241, 255), width=24)

    # Waveform graphics
    bars = [200, 350, 550, 750, 600, 850, 400, 650, 300, 150]
    bar_width = 48
    spacing = 36
    start_x = 110

    for i, height in enumerate(bars):
        x0 = start_x + i * (bar_width + spacing)
        y0 = 512 - (height // 2)
        x1 = x0 + bar_width
        y1 = 512 + (height // 2)
        draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(129, 140, 248, 255))

    # Save PNG
    png_path = resources_dir / "icon.png"
    img.save(png_path, format="PNG")

    # Generate Windows ICO
    ico_path = resources_dir / "icon.ico"
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format="ICO", sizes=ico_sizes)

    # Generate macOS ICNS
    icns_path = resources_dir / "icon.icns"
    try:
        img.save(icns_path, format="ICNS")
    except Exception:
        # Fallback if Pillow-ICNS isn't native on OS
        img.save(icns_path, format="PNG")

    print(f"Icons successfully generated at: {resources_dir}")

if __name__ == "__main__":
    create_app_icon()