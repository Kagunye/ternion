"""Scaled side-view vehicle drawings for the "Fleet sizes" section.

Every vehicle is drawn at the same scale (S px per metre) in an SVG that is
1000 units wide, so the trucks compare at true relative size, with dimension
lines like a technical drawing.
"""
from django.utils.html import escape
from django.utils.safestring import mark_safe

S = 40          # px per metre
X0 = 175        # where the front of every vehicle starts
W = 1000        # viewBox width
XR = 905        # height-dimension line x

ORANGE = "#f5770f"
ORANGE_D = "#d9620a"
CAB = "#0b1f4d"
DARK = "#121212"
GLASS = "#8d979e"
STEEL = "#c4c4c4"
INK = "currentColor"

ICONS = [
    "M6 9l6-3 6 3v7l-6 3-6-3z M6 9l6 3 6-3 M12 12v7",                 # parcel
    "M12 5v14 M6 8.5l12 7 M6 15.5l12-7",                               # cold chain
    "M5 9h14 M7 9l1 9h8l1-9 M9 9V7a3 3 0 0 1 6 0v2",                    # retail
    "M3 8h11v8H3z M14 11h4l3 3v2h-7z M7 18.5a1.5 1.5 0 1 0 0.01 0 M17 18.5a1.5 1.5 0 1 0 0.01 0",  # delivery
]


class Drawing:
    def __init__(self, max_h):
        self.top = 74
        self.G = self.top + max_h * S
        self.H = self.G + 34
        self.p = []

    def x(self, m):
        return round(X0 + m * S, 1)

    def y(self, h):
        return round(self.G - h * S, 1)

    def poly(self, pts, fill, extra=""):
        s = " ".join(f"{self.x(m)},{self.y(h)}" for m, h in pts)
        self.p.append(f'<polygon points="{s}" fill="{fill}" {extra}/>')

    def rect(self, m0, h0, m1, h1, fill, extra=""):
        x, y = self.x(m0), self.y(max(h0, h1))
        w, h = abs(m1 - m0) * S, abs(h1 - h0) * S
        self.p.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>')

    def wheel(self, m, r):
        cx, cy = self.x(m), self.y(r)
        R = r * S
        self.p.append(
            f'<circle cx="{cx}" cy="{cy}" r="{R + 3:.1f}" fill="{DARK}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="#1b1b1b"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * .55:.1f}" fill="{STEEL}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * .42:.1f}" fill="#9a9a9a"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * .16:.1f}" fill="#3a3a3a"/>'
        )

    def shadow(self, m0, m1):
        cx = (self.x(m0) + self.x(m1)) / 2
        rx = (m1 - m0) * S / 2 + 20
        self.p.append(f'<ellipse cx="{cx}" cy="{self.G + 2}" rx="{rx:.1f}" ry="9" fill="url(#fsShadow)"/>')

    # ---- branding on the cargo body -------------------------------------
    def branding(self, m0, h0, m1, h1, icons=True):
        bh = (h1 - h0) * S
        k = bh * 0.42 / 32                       # logo mark scale
        mx = self.x(m0) + bh * 0.22
        my = self.y(h1) + bh * 0.24
        self.p.append(
            f'<g transform="translate({mx:.1f},{my:.1f}) scale({k:.3f})">'
            f'<path d="M4 6h14v6h-8v14H4z" fill="#fff"/>'
            f'<path d="M20 6h8v20h-8z" fill="none" stroke="#fff" stroke-width="2.5"/></g>'
        )
        fs = bh * 0.13
        tx = mx + 31 * k
        self.p.append(
            f'<text x="{tx:.1f}" y="{my + 24 * k:.1f}" fill="#fff" font-family="Unbounded, sans-serif" '
            f'font-weight="700" font-size="{fs:.1f}" letter-spacing=".06em">TERNION</text>'
        )
        if not icons:
            return
        size = bh * 0.26
        gap = size * 0.45
        start = tx + fs * 7.4
        end = self.x(m1) - bh * 0.15
        n = int((end - start + gap) // (size + gap))
        for i, d in enumerate(ICONS[:max(0, n)]):
            ix = start + i * (size + gap)
            iy = my + (32 * k - size) / 2 + 2 * k
            sc = size / 24
            self.p.append(
                f'<g transform="translate({ix:.1f},{iy:.1f}) scale({sc:.3f})" fill="none" stroke="#fff" '
                f'stroke-width="{1.4 / sc * 0.9:.2f}" stroke-linecap="round" stroke-linejoin="round">'
                f'<rect x="0.5" y="0.5" width="23" height="23"/><g transform="translate(3 3) scale(.75)"><path d="{d}"/></g></g>'
            )

    def cargo_box(self, m0, h0, m1, h1, icons=True):
        self.rect(m0, h0, m1, h1, ORANGE)
        self.rect(m0, h0, m1, h0 + 0.12, ORANGE_D)
        self.rect(m0, h1 - 0.06, m1, h1, ORANGE_D)
        self.branding(m0, h0, m1, h1, icons)

    # ---- annotations ------------------------------------------------------
    def length_dim(self, m0, m1, h_top, label):
        y = self.y(h_top) - 30
        x0, x1 = self.x(m0), self.x(m1)
        self.p.append(
            f'<g class="dim" stroke="{INK}" stroke-width="1.2">'
            f'<path d="M{x0} {y} H{x1} M{x0} {y - 7} V{self.y(h_top)} M{x1} {y - 7} V{self.y(h_top)}"/></g>'
            f'<text class="dim-t" x="{(x0 + x1) / 2:.1f}" y="{y - 12}" text-anchor="middle">{escape(label)}</text>'
        )

    def height_dim(self, m_end, h0, h1, label):
        x = self.x(m_end)
        y0, y1 = self.y(h0), self.y(h1)
        self.p.append(
            f'<g class="dim" stroke="{INK}" stroke-width="1.2" fill="none">'
            f'<path d="M{x + 6} {y1} H{XR + 8} M{x + 6} {y0} H{XR + 8} M{XR} {y1} V{y0}"/></g>'
            f'<text class="dim-t" x="{XR + 16}" y="{(y0 + y1) / 2 + 7:.1f}">{escape(label)}</text>'
        )

    def callout(self, volume, sub, target_m, target_h, label_h):
        ly = self.y(label_h)
        tx, ty = self.x(target_m), self.y(target_h)
        self.p.append(
            f'<text class="vol" x="6" y="{ly - 10}">V = {escape(volume)} m<tspan dy="-9" font-size=".6em">3</tspan></text>'
            f'<text class="vol-sub" x="6" y="{ly + 22}" dy="0">{escape(sub)}</text>'
            f'<path class="dim" d="M0 {ly} H120 L{tx} {ty}" stroke="{INK}" stroke-width="1.2" fill="none"/>'
            f'<circle cx="{tx}" cy="{ty}" r="3.5" fill="{ORANGE}"/>'
        )

    def svg(self, label):
        defs = (
            '<defs><radialGradient id="fsShadow"><stop offset="0" stop-color="#000" stop-opacity=".28"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
        )
        return mark_safe(
            f'<svg class="fs-svg" viewBox="0 0 {W} {self.H:.0f}" role="img" aria-label="{escape(label)}">'
            f'{defs}{"".join(self.p)}</svg>'
        )


# ---- cabs ------------------------------------------------------------------
def heavy_cab(d, spoiler_to):
    d.poly([(0, .55), (0, 2.25), (.1, 2.95), (.35, 3.1), (2.3, 3.1), (2.3, .55)], CAB)
    if spoiler_to > 3.15:
        d.poly([(.75, 3.1), (1.25, spoiler_to - .04), (2.3, spoiler_to), (2.3, 3.1)], CAB)
    d.poly([(.05, 2.15), (.15, 2.88), (.45, 2.95), (.45, 2.15)], GLASS)
    d.poly([(.62, 2.15), (.62, 2.92), (1.55, 2.92), (1.55, 2.15)], GLASS)
    d.rect(0, 1.55, 2.3, 1.68, ORANGE)
    d.rect(1.62, .75, 1.65, 2.95, DARK)
    d.rect(-.12, 1.95, -.02, 2.7, DARK)
    d.rect(-.06, .42, .95, .85, DARK)
    d.rect(-.03, .95, .28, 1.12, "#ffcf87")
    d.rect(1.0, .6, 1.55, .7, STEEL)


def light_cab(d):
    d.poly([(0, .45), (0, 1.0), (.55, 1.18), (1.05, 2.15), (1.95, 2.25), (1.95, .45)], CAB)
    d.poly([(.62, 1.22), (1.08, 2.05), (1.4, 2.1), (1.4, 1.22)], GLASS)
    d.poly([(1.5, 1.22), (1.5, 2.1), (1.85, 2.13), (1.85, 1.22)], GLASS)
    d.rect(0, 1.0, 1.95, 1.08, ORANGE)
    d.rect(-.05, .38, .7, .65, DARK)
    d.rect(-.02, .78, .25, .92, "#ffcf87")


# ---- vehicles ----------------------------------------------------------------
def semi():
    d = Drawing(3.9)
    d.shadow(-.1, 16.2)
    d.rect(.3, .75, 16.1, .98, "#2e2e2e")
    d.rect(10.2, .62, 12.0, .72, STEEL)
    d.cargo_box(2.5, 1.25, 16.1, 3.9)
    heavy_cab(d, 3.85)
    for m in (.95, 3.55, 4.75):
        d.wheel(m, .5)
    for m in (12.75, 13.95, 15.15):
        d.wheel(m, .5)
    d.length_dim(2.5, 16.1, 3.9, "13.6 m")
    d.height_dim(16.1, 1.25, 3.9, "2.65 m")
    d.callout("82", "20 t · 33 pallets", .4, 2.6, 3.45)
    return d.svg("Semi-trailer, 13.6 m body, 82 cubic metres")


def rigid():
    d = Drawing(3.5)
    d.shadow(-.1, 9.5)
    d.rect(.3, .72, 9.35, .95, "#2e2e2e")
    d.rect(3.4, .6, 5.6, .7, STEEL)
    d.cargo_box(2.45, 1.15, 9.35, 3.5)
    heavy_cab(d, 3.45)
    for m in (.95, 6.85, 8.05):
        d.wheel(m, .5)
    d.length_dim(2.45, 9.35, 3.5, "6.9 m")
    d.height_dim(9.35, 1.15, 3.5, "2.35 m")
    d.callout("45", "10 t · 18 pallets", .4, 2.6, 3.1)
    return d.svg("Rigid truck, 6.9 m body, 45 cubic metres")


def light_truck():
    d = Drawing(2.8)
    d.shadow(-.1, 5.6)
    d.rect(.4, .55, 5.4, .72, "#2e2e2e")
    d.cargo_box(2.05, .85, 5.05, 2.8)
    light_cab(d)
    d.wheel(.85, .36)
    d.wheel(4.25, .36)
    d.length_dim(2.05, 5.05, 2.8, "3 m")
    d.height_dim(5.05, .85, 2.8, "1.95 m")
    d.callout("9", "1.5 t · 4 pallets", .75, 1.5, 2.4)
    return d.svg("Light box truck, 3 m body, 9 cubic metres")


def panel_van():
    d = Drawing(1.85)
    d.shadow(-.1, 4.7)
    d.poly([(0, .35), (0, .82), (.85, 1.08), (1.55, 1.75), (4.45, 1.85), (4.6, 1.72), (4.6, .35)], ORANGE)
    d.poly([(.98, 1.1), (1.55, 1.62), (2.25, 1.66), (2.25, 1.1)], GLASS)
    d.rect(2.32, .45, 2.35, 1.62, ORANGE_D)
    d.rect(-.05, .28, .75, .55, DARK)
    d.rect(3.9, .28, 4.65, .5, DARK)
    d.rect(-.02, .7, .22, .82, "#ffcf87")
    d.rect(1.95, .95, 2.15, 1.0, DARK)
    d.branding(2.55, .9, 4.4, 1.6, icons=False)
    d.wheel(.8, .32)
    d.wheel(3.75, .32)
    d.length_dim(2.3, 4.5, 1.85, "2.2 m")
    d.height_dim(4.6, .4, 1.8, "1.4 m")
    d.callout("5", "0.8 t · parcels", .6, 1.0, 1.8)
    return d.svg("Panel van, 2.2 m cargo area, 5 cubic metres")


def vehicles():
    return [
        {"name": "Semi-trailer", "use": "Long-haul full loads, Mombasa to Nairobi", "svg": semi()},
        {"name": "Rigid truck", "use": "Regional distribution, part loads", "svg": rigid()},
        {"name": "Light truck", "use": "City deliveries, moving, small batches", "svg": light_truck()},
        {"name": "Panel van", "use": "Express parcels and last mile", "svg": panel_van()},
    ]
