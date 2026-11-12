"""Cut the truck-on-rails picture out of the 'Never Go Off Track' poster.

Removes the poster's own text (it is re-set as live HTML on the site), crops
off the header/tagline, and turns the white studio background transparent.
Usage: python tools/process_track.py "<path to Never Go Off Track.png>"
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_images import OUT, remove_white_background, trim, sketch  # noqa: E402

src = Image.open(sys.argv[1]).convert("RGB")
d = ImageDraw.Draw(src)
d.rectangle((0, 0, src.width, 140), fill="white")        # brand title
d.rectangle((0, 150, 492, 772), fill="white")            # headline + paragraph
d.rectangle((0, 772, 322, 872), fill="white")            # "Clear direction" lines
img = src.crop((0, 220, src.width, 1288))                # drop bottom tagline
img = trim(remove_white_background(img, threshold=215, pocket=0.002))
img.save(OUT / "truck-track.webp", "WEBP", quality=90, method=6)
print("wrote truck-track", img.size)
