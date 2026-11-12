"""Hero video from the text-free shots in the first 26 s of the source recording,
plus the drawn warehouse / delivered scenes so the journey ends at handover.

  1 Ship       20.1-22.8 s  top-down container ship at sea
  2 Loading     0.0-2.9 s   crane lifting the container
  3 Transport  12.5-13.8 s  top-down truck on the road (slowed to ~2.6 s)
  4 Warehouse  drawn        truck pulls up at the receiving warehouse
  5 Delivered  drawn        check badge + signed note

Every other part of 0-26 s carries the source site's headlines/service text and
is not used. The cursor overlay, speed label and source nav bar are painted out.

Usage: python tools/build_hero_story.py "<source.mp4>"
Writes static/video/hero.mp4 / hero.webm / hero-poster.jpg and prints step times.
"""
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_hero_video as drawn  # noqa: E402  (warehouse/delivered scenes)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "video"
SW, SH = 740, 460                 # source frame
W, H = 1280, 796                  # output, same shape as the source (1.61:1)
FPS = 30
XF = 12                           # 0.4 s crossfades
SKY = (252, 252, 252)
CUR = (436, 168, 476, 210)        # cursor overlay box in source pixels (x0, y0, x1, y1)

# shadows -> Ternion navy (same curve as the earlier hero clip)
_x = np.arange(256) / 255.0
def _curve(pts):
    xs, ys = zip(*pts)
    return np.clip(np.interp(_x, xs, ys) * 255, 0, 255).astype(np.uint8)
LUT = np.stack([_curve([(0, .03), (.25, .25), (1, 1)]),
                _curve([(0, .12), (.25, .27), (1, 1)]),
                _curve([(0, .30), (.25, .36), (1, 1)])], axis=-1)


def navy(f):
    return np.stack([LUT[..., c][f[..., c]] for c in range(3)], axis=-1)


def grab(src, start, dur, extra=""):
    """Decode a section of the source as RGB frames (30 fps)."""
    vf = f"trim={start}:{start + dur},setpts=PTS-STARTPTS,fps={FPS}{extra}"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return list(np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3).copy())


def fit(f, crop=None):
    if crop:
        x0, y0, x1, y1 = crop
        f = f[y0:y1, x0:x1]
    return cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)


def remove_static_cursor(frames, pad=3):
    """Cursor stays put while the picture moves under it: mask low-variance pixels
    inside the cursor box that differ from their surroundings, then inpaint."""
    x0, y0, x1, y1 = CUR
    stack = np.stack([f[y0:y1, x0:x1].astype(np.float32) for f in frames])
    std = stack.std(axis=0).mean(axis=-1)
    mean = stack.mean(axis=0)
    local = cv2.medianBlur(mean.astype(np.uint8), 9).astype(np.float32)
    diff = np.abs(mean - local).mean(axis=-1)
    mask = ((std < 10) & (diff > 7)).astype(np.uint8) * 255
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=pad)
    full = np.zeros((SH, SW), np.uint8)
    full[y0:y1, x0:x1] = mask
    return [cv2.inpaint(f, full, 4, cv2.INPAINT_TELEA) for f in frames], int(mask.astype(bool).sum())


def shot_ship(src):
    frames = grab(src, 20.1, 2.7)
    frames, n = remove_static_cursor(frames)
    print("ship cursor pixels:", n)
    # crop so the ship sits right of centre (text overlays the left of the hero)
    return [fit(f, (0, 44, 600, 417)) for f in frames]


def shot_loading(src):
    frames = grab(src, 0.0, 2.9)
    out = []
    for f in frames:
        f[:36] = SKY                                     # source site's nav bar
        f[171:199, 440:473] = SKY                        # cursor (on plain sky here)
        f[198:203, 452:469] = SKY
        out.append(fit(navy(f[:, ::-1])))                # mirror: crane on the right
    return out


def shot_transport(src):
    # slow the 1.3 s shot to ~2.6 s with frame blending
    frames = grab(src, 12.5, 1.3, ",setpts=2*PTS,minterpolate=fps=30:mi_mode=blend")
    for f in frames:
        f[24:50, 8:70] = np.median(f[52:62, 8:70].reshape(-1, 3), axis=0)   # "xx KM/H" label, filled with the sky beside it
    frames, n = remove_static_cursor(frames)             # road pans under the fixed cursor
    print("transport cursor pixels:", n)
    return [fit(navy(f[:, ::-1])) for f in frames]


def drawn_to_frame(f):
    """Drawn scenes are 1110x496; widen to 1280 and add sky above."""
    g = cv2.resize(f, (W, round(f.shape[0] * W / f.shape[1])), interpolation=cv2.INTER_LANCZOS4)
    canvas = np.full((H, W, 3), SKY, np.uint8)
    canvas[H - g.shape[0]:] = g
    return canvas


def crossfade(a, b, n=XF):
    return [(a[i].astype(np.float32) * (1 - (i + 1) / (n + 1)) +
             b[i].astype(np.float32) * ((i + 1) / (n + 1))).astype(np.uint8) for i in range(n)]


def main(src):
    truck, wb = drawn.load_truck(232)
    bg = drawn.warehouse_bg()
    wh, stop_x = drawn.scene_warehouse(truck, wb, bg, 90)
    dl = drawn.scene_delivered(truck, wb, bg, stop_x, 84)
    scenes = [
        ("Ship", shot_ship(src)),
        ("Loading", shot_loading(src)),
        ("Transport", shot_transport(src)),
        ("Warehouse", [drawn_to_frame(f) for f in wh]),
        ("Delivered", [drawn_to_frame(f) for f in dl]),
    ]
    timeline, starts, tail = [], [], None
    for k, (name, fr) in enumerate(scenes):
        if k == 0:
            starts.append((name, 0.0))
            timeline.extend(fr[:-XF])
        else:
            starts.append((name, round((len(timeline) + XF / 2) / FPS, 2)))
            timeline.extend(crossfade(tail, fr[:XF]))
            timeline.extend(fr[XF:-XF])
        tail = fr[-XF:]
    timeline.extend(crossfade(tail, [scenes[0][1][0]] * XF))   # seamless loop

    raw = b"".join(f.tobytes() for f in timeline)
    common = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an"]
    subprocess.run(common + ["-c:v", "libx264", "-crf", "22", "-preset", "slow", "-pix_fmt", "yuv420p",
                             "-movflags", "+faststart", str(OUT / "hero.mp4")], input=raw, check=True)
    subprocess.run(common + ["-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0", "-row-mt", "1",
                             str(OUT / "hero.webm")], input=raw, check=True)
    cv2.imwrite(str(OUT / "hero-poster.jpg"), cv2.cvtColor(timeline[0], cv2.COLOR_RGB2BGR),
                [cv2.IMWRITE_JPEG_QUALITY, 84])
    print(f"frames={len(timeline)} duration={len(timeline) / FPS:.2f}s")
    print("starts:", starts)


if __name__ == "__main__":
    main(sys.argv[1])
