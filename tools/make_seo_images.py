"""Generate the social share image and favicons.

  static/img/og-image.jpg          1200x630 link preview (WhatsApp, Facebook, LinkedIn, X)
  static/img/favicon.ico           16/32/48 px
  static/img/favicon-32.png        32 px
  static/img/apple-touch-icon.png  180 px

Usage: python tools/make_seo_images.py
Uses Windows system fonts (Segoe UI Black / Segoe UI); pass FONT_DIR to override.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "static" / "img"
FONT_DIR = Path(os.environ.get("FONT_DIR", "C:/Windows/Fonts"))
NAVY, NAVY2, ORANGE, WHITE = (11, 31, 77), (19, 48, 110), (245, 119, 15), (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def og_image():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    # faint drafting grid
    for x in range(0, W, 80):
        d.line((x, 0, x, H), fill=(18, 40, 92), width=1)
    for y in range(0, H, 80):
        d.line((0, y, W, y), fill=(18, 40, 92), width=1)
    # road strip with orange kerb
    d.rectangle((0, H - 70, W, H), fill=NAVY2)
    d.rectangle((0, H - 74, W, H - 70), fill=ORANGE)
    for x in range(20, W, 120):
        d.rectangle((x, H - 37, x + 50, H - 33), fill=(120, 140, 180))

    # truck on the right, wheels on the road
    truck = Image.open(IMG / "truck-orange.webp").convert("RGBA")
    tw = 500
    truck = truck.resize((tw, round(truck.height * tw / truck.width)), Image.LANCZOS)
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((620, 300, 1200, 600), fill=(245, 119, 15, 70))
    im.paste(glow.filter(ImageFilter.GaussianBlur(60)), (0, 0), glow.filter(ImageFilter.GaussianBlur(60)))
    im.paste(truck, (W - tw - 12, H - 70 - truck.height + 20), truck)

    # logo (white version) and text
    logo = Image.open(IMG / "logo-dark.webp").convert("RGBA")
    lh = 128
    logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
    im.paste(logo, (64, 48), logo)

    d = ImageDraw.Draw(im)
    d.text((66, 214), "ROAD FREIGHT · MOMBASA · NAIROBI · KENYA", font=font("segoeuib.ttf", 20), fill=ORANGE)
    big = font("seguibl.ttf", 54)
    d.text((64, 248), "NEVER CHASE", font=big, fill=WHITE)
    d.text((64, 308), "A TRUCK AGAIN.", font=big, fill=WHITE)
    d.text((64, 368), "WE CALL YOU FIRST.", font=big, fill=ORANGE)
    d.text((66, 468), "ternionventures.co.ke  ·  +254 724 388677", font=font("segoeui.ttf", 24), fill=(196, 208, 230))
    im.save(IMG / "og-image.jpg", quality=88, optimize=True, progressive=True)
    return im


def icon(size):
    """Navy rounded square, white T with the logo's orange swoosh."""
    s = 512
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=112, fill=NAVY)
    d.arc((60, 70, 470, 420), start=200, end=330, fill=ORANGE, width=34)
    f = font("seguibl.ttf", 360)
    box = d.textbbox((0, 0), "T", font=f)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.text(((s - tw) / 2 - box[0], (s - th) / 2 - box[1] + 34), "T", font=f, fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def main():
    og_image()
    icon(180).save(IMG / "apple-touch-icon.png")
    icon(32).save(IMG / "favicon-32.png")
    icon(48).save(IMG / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote og-image.jpg, apple-touch-icon.png, favicon-32.png, favicon.ico")


if __name__ == "__main__":
    main()
