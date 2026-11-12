"""Prepare the raw truck/container photos so they blend into the site theme.

- Removes white studio backgrounds (colour-to-alpha on the region connected to
  the image border), so shadows become soft translucent black that works on
  both the dark and the light sections.
- Trims empty margins.
- Builds faint "blueprint" line sketches of each picture, used as decorative
  backgrounds like the technical drawings in the reference poster.

Usage:  python tools/process_images.py <source_dir>
Source dir must contain 2.webp (black truck), 3.webp (container), 4.webp (orange truck).
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage

OUT = Path(__file__).resolve().parent.parent / "static" / "img"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "2.webp": ("truck-container", 0.002),
    "3.webp": ("container-hook", 0.0002),
    "4.webp": ("truck-orange", 0.002),
}


def remove_white_background(img: Image.Image, threshold: int = 200, pocket: float = 0.002) -> Image.Image:
    rgba = np.asarray(img.convert("RGBA")).astype(np.float32)
    rgb, alpha = rgba[..., :3], rgba[..., 3] / 255.0

    # Region of light pixels connected to the image border = background.
    light = rgb.min(axis=2) > threshold
    labels, _ = ndimage.label(light)
    border = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    border = border[border != 0]
    bg = np.isin(labels, border)
    # Also clear large enclosed pure-white pockets (e.g. between crane cables).
    white = rgb.min(axis=2) > 238
    wl, n = ndimage.label(white)
    if n:
        sizes = ndimage.sum(white, wl, index=np.arange(1, n + 1))
        big = np.where(sizes > white.size * pocket)[0] + 1
        bg |= np.isin(wl, big)
    # Grow slightly so anti-aliased fringe pixels are softened too.
    bg_soft = ndimage.binary_dilation(bg, iterations=2)

    # GIMP-style colour-to-alpha against white.
    dist = (255.0 - rgb) / 255.0
    a_new = np.clip(dist.max(axis=2), 0, 1)
    a_new = np.clip((a_new - 0.02) / 0.98, 0, 1)  # kill near-white noise
    safe = np.maximum(a_new, 1e-4)[..., None]
    rgb_new = 255.0 - (255.0 - rgb) / safe
    rgb_new = np.clip(rgb_new, 0, 255)

    out_rgb = np.where(bg_soft[..., None], rgb_new, rgb)
    out_a = np.where(bg_soft, a_new, 1.0) * alpha
    out = np.dstack([out_rgb, out_a * 255.0]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def trim(img: Image.Image, pad: int = 8) -> Image.Image:
    a = np.asarray(img.getchannel("A"))
    ys, xs = np.where(a > 12)
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
           min(xs.max() + pad, img.width), min(ys.max() + pad, img.height))
    return img.crop(box)


def sketch(img: Image.Image) -> Image.Image:
    """White line drawing on transparent background (blueprint feel)."""
    gray = ImageOps.grayscale(img.convert("RGBA").convert("RGB"))
    mask = img.getchannel("A")
    edges = gray.filter(ImageFilter.GaussianBlur(1.2)).filter(ImageFilter.FIND_EDGES)
    e = np.asarray(edges).astype(np.float32)
    e = np.clip((e - 6) * 6, 0, 255)
    e *= (np.asarray(mask) > 40)
    line = np.zeros((img.height, img.width, 4), np.uint8)
    line[..., :3] = 255
    line[..., 3] = e.astype(np.uint8)
    return Image.fromarray(line, "RGBA")


def main(src_dir: Path) -> None:
    for name, (slug, pocket) in SOURCES.items():
        img = Image.open(src_dir / name)
        if img.mode != "RGBA" or np.asarray(img.getchannel("A")).min() == 255:
            img = remove_white_background(img, pocket=pocket)
        img = trim(img)
        img.save(OUT / f"{slug}.webp", "WEBP", quality=90, method=6)
        sk = sketch(img)
        sk.thumbnail((1400, 1400))
        sk.save(OUT / f"{slug}-sketch.webp", "WEBP", quality=80, method=6)
        print("wrote", slug, img.size)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
