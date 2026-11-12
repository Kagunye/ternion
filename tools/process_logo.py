"""Extract the Ternion logo from the content PDF and make web versions.

logo.webp       original colours, transparent background (for light sections)
logo-dark.webp  navy lettering/swoosh turned white (for the dark header/footer)
Usage: python tools/process_logo.py "<content pdf>"
"""
import base64
import re
import sys
import zlib
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_images import OUT, remove_white_background, trim  # noqa: E402

data = Path(sys.argv[1]).read_bytes()
# first embedded RGB image (ASCII85 + Flate) is the logo
m = re.search(rb'<<[^>]*?/Subtype /Image[^>]*?>>\s*stream', data, re.S)
hdr = data[data.rfind(b'obj', 0, m.start()):m.end()]
w = int(re.search(rb'/Width (\d+)', hdr).group(1))
h = int(re.search(rb'/Height (\d+)', hdr).group(1))
start = m.end()
raw = re.sub(rb'\s', b'', data[start:data.index(b'endstream', start)])
raw = raw.removeprefix(b'<~').removesuffix(b'~>')
img = Image.frombytes('RGB', (w, h), zlib.decompress(base64.a85decode(raw))[: w * h * 3])

logo = trim(remove_white_background(img, threshold=225), pad=4)
logo.save(OUT / 'logo.webp', 'WEBP', quality=92, method=6)

# dark-background variant: navy -> white, except inside the truck and the tagline pill
a = np.asarray(logo).astype(np.int16).copy()
r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
lum = 0.3 * r + 0.59 * g + 0.11 * b
navy = (b > r + 20) & (lum < 95)
H, W = navy.shape
yy, xx = np.mgrid[0:H, 0:W]
truck = (xx > W * 0.31) & (xx < W * 0.82) & (yy < H * 0.52)
pill = yy > H * 0.84
mask = navy & ~truck & ~pill
a[mask, 0:3] = 255
Image.fromarray(a.astype(np.uint8), 'RGBA').save(OUT / 'logo-dark.webp', 'WEBP', quality=92, method=6)
print('wrote logo', logo.size)
