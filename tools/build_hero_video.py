"""Build the hero video: ship -> loading -> transport -> warehouse -> delivered.

All scenes share one stage: off-white sky and the navy road/quay band from the
crane clip, so they flow into each other with short crossfades.

  1 Ship       container ship at sea (from the "Why us" photo), drifting right
  2 Loading    the crane clip (first 3.2 s of the source recording)
  3 Transport  container truck on the road, lane markings rushing past
  4 Warehouse  truck pulls up at a receiving warehouse
  5 Delivered  check badge + signed note pop in

Usage:
  python tools/build_hero_video.py "<crane source.mp4>" "<why-us ship image>"
Writes static/video/hero.mp4, hero.webm, hero-poster.jpg and prints the step
start times used by the hero's step indicator.
"""
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "static" / "img"
OUT = ROOT / "static" / "video"

W, H = 1110, 496
FLOOR_Y = 433                     # road band = bottom 12.7 %, same as the crane clip
FPS = 30
XF = 12                           # crossfade frames (0.4 s)
BG = (252, 252, 252)
FLOOR = (19, 39, 76)
NAVY = (11, 31, 77)
ORANGE = (245, 119, 15)


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    return 3 * t * t - 2 * t * t * t


def stage():
    im = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(im).rectangle((0, FLOOR_Y, W, H), fill=FLOOR)
    return im


def road_dashes(im, offset):
    d = ImageDraw.Draw(im)
    y = FLOOR_Y + (H - FLOOR_Y) // 2
    step = 120
    x = -(offset % step)
    while x < W:
        d.rectangle((x, y - 2, x + 46, y + 2), fill=(214, 222, 236))
        x += step


def load_truck(height):
    t = Image.open(IMG / "truck-container.webp").convert("RGBA")
    k = height / t.height
    t = t.resize((round(t.width * k), height), Image.LANCZOS)
    a = np.asarray(t.getchannel("A"))
    rows = np.where((a > 200).any(axis=1))[0]
    wheel_bottom = rows.max()          # ignore the soft shadow under the tyres
    return t, wheel_bottom


# ---------------------------------------------------------------- scene 1: ship
def build_ocean(ship_path):
    src = Image.open(ship_path).convert("RGB")
    band = src.crop((0, 420, src.width, 745))            # ship + wake, below the lettering, above the icons
    water = src.crop((0, 1232, src.width, src.height))   # open water from the bottom of the photo
    pad_h = 240
    pad = Image.new("RGB", (src.width, pad_h))
    y = pad_h
    flip = False
    while y > 0:                                         # stack mirrored water strips upward
        piece = water.transpose(Image.FLIP_TOP_BOTTOM) if flip else water
        y -= piece.height
        pad.paste(piece, (0, y))
        flip = not flip
    # match the added water to the open water beside the ship (left of the stern)
    b_arr = np.asarray(band).astype(np.float32)
    ref = b_arr[0:8, 0:80].reshape(-1, 3).mean(axis=0)
    p_arr = np.asarray(pad).astype(np.float32)
    p_arr = np.clip(p_arr + (ref - p_arr[-24:].reshape(-1, 3).mean(axis=0)), 0, 255)
    pad = Image.fromarray(p_arr.astype(np.uint8))
    # outside the hull (stern-side and bow-side water), fade the band's top rows into the pad
    ship_x0, ship_x1, rows = 96, 1010, 44
    edge = p_arr[-1]
    for i in range(rows):
        w = 1 - (i + 1) / (rows + 1)
        for xs in (slice(0, ship_x0), slice(ship_x1, None)):
            b_arr[i, xs] = b_arr[i, xs] * (1 - w) + edge[xs] * w
    band = Image.fromarray(b_arr.astype(np.uint8))
    canvas = Image.new("RGB", (src.width, pad_h + band.height))
    canvas.paste(pad, (0, 0))
    canvas.paste(band, (0, pad_h))   # inside the hull span, the deck edge itself is the join
    k = 1.2
    return canvas.resize((round(canvas.width * k), round(canvas.height * k)), Image.LANCZOS), round(pad_h * k)


SHADE = Image.new("RGBA", (W, 190), (6, 22, 52, 0))
SHADE.putalpha(Image.linear_gradient("L").resize((W, 190)).point(lambda v: round((255 - v) * 0.62)))


def scene_ship(ocean_and_top, n):
    ocean, ship_top = ocean_and_top
    pan = ocean.width - W
    frames = []
    for i in range(n):
        t = i / (n - 1)
        x = round(pan * (1 - ease_in_out(t)))           # window moves left => ship sails right
        y = max(0, ship_top - 105)                       # ~105 px of open water above the ship
        im = stage()
        im.paste(ocean.crop((x, y, x + W, y + FLOOR_Y)), (0, 0))
        im.paste(SHADE, (0, 0), SHADE)                   # soft top shade hides the water join
        # quay edge
        ImageDraw.Draw(im).rectangle((0, FLOOR_Y - 3, W, FLOOR_Y), fill=(42, 62, 102))
        frames.append(np.asarray(im))
    return frames


# ------------------------------------------------------------- scene 2: loading
def scene_loading(src_mp4):
    tmp = Path(tempfile.mkdtemp()) / "loading.mp4"
    vf = (
        "trim=0:3.2,setpts=PTS-STARTPTS,format=rgb24,"
        "drawbox=x=440:y=171:w=33:h=28:color=0xFCFCFC@1:t=fill,"
        "drawbox=x=452:y=198:w=17:h=5:color=0xFCFCFC@1:t=fill,"
        "crop=740:330:0:130,hflip,"
        "curves=r='0/0.03 0.25/0.25 1/1':g='0/0.12 0.25/0.27 1/1':b='0/0.30 0.25/0.36 1/1',"
        f"scale={W}:{H}:flags=lanczos,fps={FPS}"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src_mp4, "-vf", vf, "-an",
                    "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv444p", str(tmp)], check=True)
    cap = cv2.VideoCapture(str(tmp))
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames


# ----------------------------------------------------------- scene 3: transport
def scene_transport(truck, wb, n):
    frames = []
    for i in range(n):
        t = i / (n - 1)
        im = stage()
        road_dashes(im, i * 22)
        x = round(-120 + 420 * ease_in_out(t))
        y = FLOOR_Y + 6 - wb
        bob = round(math.sin(i * 0.9) * 1)                # tiny road vibration
        im.paste(truck, (x, y + bob), truck)
        frames.append(np.asarray(im))
    return frames


# ----------------------------------------------------------- scene 4/5: warehouse
def warehouse_bg():
    im = stage()
    road_dashes(im, 0)
    d = ImageDraw.Draw(im)
    x0, x1, wall_top, peak = 560, 1090, 196, 120
    # building
    d.polygon([(x0 - 14, wall_top), ((x0 + x1) // 2, peak), (x1 + 14, wall_top)], fill=NAVY)
    d.rectangle((x0, wall_top, x1, FLOOR_Y), fill=(228, 234, 243), outline=NAVY, width=3)
    d.rectangle((x0, wall_top + 18, x1, wall_top + 30), fill=ORANGE)          # brand stripe
    # windows
    for wx in range(x0 + 30, x1 - 40, 70):
        d.rectangle((wx, wall_top + 46, wx + 40, wall_top + 62), fill=(173, 188, 210))
    # roller doors
    doors = [(600, 730), (760, 890), (920, 1050)]
    for j, (a, b) in enumerate(doors):
        top = 268
        if j == 1:                                           # open door: interior with cartons
            d.rectangle((a, top, b, FLOOR_Y), fill=(26, 40, 72))
            for bx, by, bw, bh in [(a + 12, FLOOR_Y - 46, 48, 46), (a + 62, FLOOR_Y - 46, 48, 46),
                                   (a + 36, FLOOR_Y - 88, 48, 42)]:
                d.rectangle((bx, by, bx + bw, by + bh), fill=(196, 152, 98), outline=(150, 112, 68), width=2)
                d.line((bx + bw // 2, by, bx + bw // 2, by + bh), fill=(226, 196, 150), width=4)
            d.rectangle((a, top, b, top + 16), fill=(196, 204, 216))          # rolled-up door
        else:
            d.rectangle((a, top, b, FLOOR_Y), fill=(198, 206, 219), outline=NAVY, width=2)
            for ly in range(top + 12, FLOOR_Y, 13):
                d.line((a + 2, ly, b - 2, ly), fill=(172, 182, 199), width=2)
        d.rectangle((a - 6, FLOOR_Y - 34, a, FLOOR_Y), fill=(30, 30, 30))       # dock bumpers
        d.rectangle((b, FLOOR_Y - 34, b + 6, FLOOR_Y), fill=(30, 30, 30))
    return im


def scene_warehouse(truck, wb, bg, n, arrive=0.82):
    frames = []
    stop_x = 360                                             # cab front ends just past the open door
    start_x = -truck.width - 20
    for i in range(n):
        t = min(1, (i / (n - 1)) / arrive)
        x = round(start_x + (stop_x - start_x) * ease_out(t))
        im = bg.copy()
        im.paste(truck, (x, FLOOR_Y + 6 - wb), truck)
        frames.append(np.asarray(im))
    return frames, stop_x


def draw_badge(im, cx, cy, s):
    if s <= 0:
        return
    big = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.ellipse((20, 20, 380, 380), fill=ORANGE + (255,))
    d.line([(110, 205), (175, 270), (295, 140)], fill=(255, 255, 255, 255), width=44, joint="curve")
    size = max(2, round(100 * s))
    b = big.resize((size, size), Image.LANCZOS)
    shadow = Image.new("RGBA", (size + 30, size + 30), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((15, 22, size + 15, size + 29), fill=(11, 31, 77, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    im.paste(shadow, (cx - size // 2 - 15, cy - size // 2 - 15), shadow)
    im.paste(b, (cx - size // 2, cy - size // 2), b)


def draw_note(im, x, y, alpha):
    if alpha <= 0:
        return
    note = Image.new("RGBA", (120, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(note)
    d.rounded_rectangle((4, 4, 116, 146), radius=6, fill=(255, 255, 255, 255), outline=NAVY + (255,), width=3)
    d.rectangle((40, 0, 80, 14), fill=NAVY + (255,))
    for ly in (36, 54, 72):
        d.line((20, ly, 100, ly), fill=(173, 188, 210, 255), width=5)
    pts = [(20, 112), (32, 98), (42, 118), (55, 100), (66, 116), (80, 104), (100, 110)]
    d.line(pts, fill=ORANGE + (255,), width=5, joint="curve")
    d.line((18, 126, 102, 126), fill=NAVY + (255,), width=2)
    note.putalpha(note.getchannel("A").point(lambda v: round(v * alpha)))
    im.paste(note, (x, y), note)


def scene_delivered(truck, wb, bg, stop_x, n):
    frames = []
    for i in range(n):
        t = i / (n - 1)
        im = bg.copy()
        im.paste(truck, (stop_x, FLOOR_Y + 6 - wb), truck)
        # badge pops: 0 -> 1.12 -> 1
        p = min(1, t / 0.28)
        s = 0 if t < 0.05 else (1.12 * ease_out(p) if p < 1 else 1.12 - 0.12 * min(1, (t - 0.28) / 0.12))
        draw_badge(im, 825, 205, s)
        # signed note slides up next to it
        q = max(0, min(1, (t - 0.2) / 0.3))
        draw_note(im, 905, round(150 + 30 * (1 - ease_out(q))), q)
        frames.append(np.asarray(im))
    return frames


# ---------------------------------------------------------------- assemble
def crossfade(a, b, n=XF):
    out = []
    for i in range(n):
        w = (i + 1) / (n + 1)
        out.append((a[i].astype(np.float32) * (1 - w) + b[i].astype(np.float32) * w).astype(np.uint8))
    return out


def main(src_mp4, ship_img):
    truck, wb = load_truck(232)
    scenes = [
        ("Ship", scene_ship(build_ocean(ship_img), 90)),
        ("Loading", scene_loading(src_mp4)),
        ("Transport", scene_transport(truck, wb, 90)),
    ]
    bg = warehouse_bg()
    wh, stop_x = scene_warehouse(truck, wb, bg, 90)
    scenes.append(("Warehouse", wh))
    scenes.append(("Delivered", scene_delivered(truck, wb, bg, stop_x, 84)))

    timeline, starts = [], []
    for k, (name, fr) in enumerate(scenes):
        if k == 0:
            starts.append((name, 0.0))
            timeline.extend(fr[:-XF])
            prev_tail = fr[-XF:]
            continue
        starts.append((name, round((len(timeline) + XF / 2) / FPS, 2)))
        timeline.extend(crossfade(prev_tail, fr[:XF]))
        timeline.extend(fr[XF:-XF])
        prev_tail = fr[-XF:]
    # loop: last scene's tail fades back into the first frame
    first = scenes[0][1][0]
    timeline.extend(crossfade(prev_tail, [first] * XF))

    OUT.mkdir(parents=True, exist_ok=True)
    raw = b"".join(f.tobytes() for f in timeline)
    common = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an"]
    subprocess.run(common + ["-c:v", "libx264", "-crf", "21", "-preset", "slow", "-pix_fmt", "yuv420p",
                             "-movflags", "+faststart", str(OUT / "hero.mp4")], input=raw, check=True)
    subprocess.run(common + ["-c:v", "libvpx-vp9", "-crf", "33", "-b:v", "0", "-row-mt", "1",
                             str(OUT / "hero.webm")], input=raw, check=True)
    Image.fromarray(timeline[0]).save(OUT / "hero-poster.jpg", quality=85)
    print(f"frames={len(timeline)} duration={len(timeline) / FPS:.2f}s")
    print("starts:", starts)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
