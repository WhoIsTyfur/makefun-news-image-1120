"""Draw the entry image: one page summing up Friday 20 November 2026.

Run locally (needs Pillow and Windows fonts):  python art/draw.py [out.png]
The output is committed as art/entry.png, which main.py copies.
All story text lives in art/stories.py; every text box here wraps its
text and raises if it would not fit, so nothing is ever clipped.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stories as ST  # noqa: E402

S = 2                      # supersampling factor
W = H = 1024
FONTS = r"C:\Windows\Fonts"

PAPER = (247, 243, 234)
INK = (22, 24, 30)
GREY = (92, 96, 104)
RULE = (40, 40, 44)
RED = (178, 34, 38)

REGION_COL = {
    "Europe": (31, 87, 160),
    "Asia": (190, 40, 45),
    "Middle East": (196, 120, 20),
    "Africa": (36, 128, 72),
    "Americas": (112, 64, 160),
    "Oceania": (20, 132, 140),
    "Global": (80, 84, 92),
}

_font_cache = {}
ERRORS = []


def font(name, size):
    key = (name, size)
    if key not in _font_cache:
        files = {
            "serif": "georgia.ttf", "serifb": "georgiab.ttf",
            "serifi": "georgiai.ttf", "sans": "segoeui.ttf",
            "sansb": "segoeuib.ttf", "sanssb": "seguisb.ttf",
            "cond": "bahnschrift.ttf",
        }
        _font_cache[key] = ImageFont.truetype(os.path.join(FONTS, files[name]), int(size * S))
    return _font_cache[key]


class Page:
    def __init__(self):
        self.im = Image.new("RGB", (W * S, H * S), PAPER)
        self.d = ImageDraw.Draw(self.im)

    # --- primitives in 1024-space -------------------------------------
    def rect(self, x, y, w, h, fill=None, outline=None, width=1):
        self.d.rectangle([x * S, y * S, (x + w) * S - 1, (y + h) * S - 1],
                         fill=fill, outline=outline, width=int(width * S))

    def rrect(self, x, y, w, h, r, fill=None, outline=None, width=1):
        self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], r * S,
                                 fill=fill, outline=outline, width=int(width * S))

    def line(self, pts, fill=INK, width=1):
        self.d.line([(px * S, py * S) for px, py in pts], fill=fill, width=max(1, int(width * S)))

    def poly(self, pts, fill=None, outline=None):
        self.d.polygon([(px * S, py * S) for px, py in pts], fill=fill, outline=outline)

    def ellipse(self, x, y, w, h, fill=None, outline=None, width=1):
        self.d.ellipse([x * S, y * S, (x + w) * S, (y + h) * S], fill=fill,
                       outline=outline, width=int(width * S))

    def circle(self, cx, cy, r, fill=None, outline=None, width=1):
        self.ellipse(cx - r, cy - r, 2 * r, 2 * r, fill, outline, width)

    def text(self, x, y, s, f, fill=INK, anchor="la"):
        self.d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)

    def tw(self, s, f):
        return self.d.textlength(s, font=f) / S

    def wrap(self, s, f, width):
        words, lines, cur = s.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.tw(t, f) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        for ln in lines:
            if self.tw(ln, f) > width:
                raise ValueError("word too wide: %r" % ln)
        return lines

    def para(self, x, y, s, f, width, lh, max_lines, fill=INK, what=""):
        lines = self.wrap(s, f, width)
        if len(lines) > max_lines:
            ERRORS.append("overflows %d lines (%s): %r" % (max_lines, what, s))
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, f, fill)
        return len(lines)

    def fit_line(self, x, y, s, f, width, fill=INK, what=""):
        if self.tw(s, f) > width:
            ERRORS.append("too wide (%s): %r %.0f>%d" % (what, s, self.tw(s, f), width))
        self.text(x, y, s, f, fill)

    def badge(self, x, y, s, size=11, fill=RED, fg=(255, 255, 255), pad=5, bold="sansb"):
        f = font(bold, size)
        w = self.tw(s, f) + 2 * pad
        h = size + 2 * pad - 2
        self.rect(x, y, w, h, fill=fill)
        self.text(x + pad, y + h / 2, s, f, fg, anchor="lm")
        return w

    def numdot(self, cx, cy, n, col, r=9, size=11):
        self.circle(cx, cy, r, fill=col)
        self.text(cx, cy + 0.5, str(n), font("sansb", size), (255, 255, 255), anchor="mm")


# ---------------------------------------------------------------------
# illustrations: each draws inside (x, y, w, h)
# ---------------------------------------------------------------------

def il_kyiv(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(18, 28, 56))
    for i in range(40):  # stars
        sx = x + (i * 97) % w
        sy = y + (i * 53) % (h * 0.45)
        p.circle(sx, sy, 0.8, fill=(200, 210, 240))
    # skyline
    bx = x
    k = 0
    while bx < x + w:
        bw = 14 + (k * 7) % 18
        bh = 30 + (k * 23) % 40
        p.rect(bx, y + h * 0.62 - bh, bw, bh + 2, fill=(10, 16, 34))
        for wy in range(int(y + h * 0.62 - bh + 6), int(y + h * 0.62 - 4), 9):
            for wx in range(int(bx + 3), int(bx + bw - 3), 6):
                if (wx * 7 + wy * 3 + k) % 5 == 0:
                    p.rect(wx, wy, 2, 3, fill=(250, 210, 110))
        bx += bw + 2
        k += 1
    # river
    p.rect(x, y + h * 0.62, w, h * 0.38, fill=(28, 52, 92))
    # three bridges
    by = y + h * 0.66
    for i in range(3):
        cx0 = x + w * (0.08 + i * 0.31)
        cw = w * 0.26
        p.rect(cx0, by - 3, cw, 5, fill=(200, 205, 215))
        for j in range(3):
            ax = cx0 + j * cw / 3
            p.d.arc([ax * S, (by - 2) * S, (ax + cw / 3) * S, (by + 22) * S], 180, 360,
                    fill=(200, 205, 215), width=int(3 * S))
        # strike flash
        fx = cx0 + cw * 0.55
        p.circle(fx, by - 8, 11, fill=(250, 120, 30))
        p.circle(fx, by - 8, 6, fill=(255, 230, 120))
    # missile trails
    for i in range(5):
        sx = x + w * (0.1 + 0.2 * i)
        p.line([(sx, y + 4), (sx + w * 0.12, y + h * 0.38)], fill=(250, 200, 120), width=1.5)
        p.circle(sx + w * 0.12, y + h * 0.38, 2.2, fill=(255, 240, 200))


def il_cyclone(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(48, 110, 170))
    # coast (land, upper-left)
    p.poly([(x, y), (x + w * 0.42, y), (x + w * 0.30, y + h * 0.35), (x + w * 0.18, y + h * 0.7),
            (x, y + h * 0.85)], fill=(226, 214, 170))
    p.text(x + 8, y + h * 0.48, "ODISHA", font("sansb", 12), (90, 80, 50))
    p.text(x + w - 10, y + h - 10, "BAY OF BENGAL", font("sansb", 10), (190, 215, 240), anchor="rd")
    cx, cy = x + w * 0.64, y + h * 0.52
    for k in range(4):
        r0 = 14 + k * 15
        p.d.arc([(cx - r0) * S, (cy - r0) * S, (cx + r0) * S, (cy + r0) * S],
                k * 70, k * 70 + 250, fill=(235, 245, 255), width=int(4 * S))
    p.circle(cx, cy, 8, fill=(235, 245, 255))
    # track to the coast
    lx, ly = x + w * 0.30, y + h * 0.36
    for t in range(8):
        a = t / 8
        p.circle(cx + (lx - cx) * a, cy + (ly - cy) * a, 1.6, fill=(255, 255, 255))
    p.circle(lx, ly, 5, fill=RED, outline=(255, 255, 255), width=1.5)
    # rain streaks
    for i in range(14):
        rx = x + w * 0.35 + (i * 37) % (w * 0.6)
        ry = y + 8 + (i * 29) % (h - 20)
        p.line([(rx, ry), (rx - 4, ry + 9)], fill=(190, 215, 240), width=1)


def il_markets(p, x, y, w, h, rows=(), title=""):
    p.rect(x, y, w, h, fill=(20, 24, 36))
    for gy in range(int(y + 20), int(y + h), 22):
        p.line([(x, gy), (x + w, gy)], fill=(40, 46, 62), width=1)
    pts = []
    n = 14
    for i in range(n):
        px = x + 10 + i * (w * 0.40) / (n - 1)
        base = y + h * 0.25 + (i / (n - 1)) ** 1.6 * h * 0.58
        jitter = (-8 if i % 3 == 1 else 5 if i % 3 == 2 else 0)
        pts.append((px, base + jitter))
    p.line(pts, fill=(235, 60, 60), width=3)
    ex, ey = pts[-1]
    p.poly([(ex - 7, ey - 4), (ex + 6, ey + 7), (ex - 8, ey + 9)], fill=(235, 60, 60))
    if title:
        p.text(x + 8, y + 6, title, font("sansb", 11), (240, 200, 90))
    f = font("sansb", 17)
    step = (h - 30) / max(1, len(rows))
    for i, (name, val) in enumerate(rows):
        ry = y + 6 + i * step
        p.text(x + w * 0.49, ry, name, f, (235, 238, 245))
        p.text(x + w - 10, ry, val, f, (255, 110, 100), anchor="ra")


def il_flags_ukeu(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(232, 236, 244))
    # simplified union flag (left half)
    fx, fy, fw, fh = x + 6, y + 8, w * 0.42, h - 16
    p.rect(fx, fy, fw, fh, fill=(20, 40, 110))
    p.line([(fx, fy), (fx + fw, fy + fh)], fill=(255, 255, 255), width=7)
    p.line([(fx, fy + fh), (fx + fw, fy)], fill=(255, 255, 255), width=7)
    p.line([(fx, fy), (fx + fw, fy + fh)], fill=(200, 30, 40), width=2.5)
    p.line([(fx, fy + fh), (fx + fw, fy)], fill=(200, 30, 40), width=2.5)
    p.rect(fx + fw / 2 - 7, fy, 14, fh, fill=(255, 255, 255))
    p.rect(fx, fy + fh / 2 - 7, fw, 14, fill=(255, 255, 255))
    p.rect(fx + fw / 2 - 4, fy, 8, fh, fill=(200, 30, 40))
    p.rect(fx, fy + fh / 2 - 4, fw, 8, fill=(200, 30, 40))
    # EU
    ex = x + w - 6 - w * 0.42
    p.rect(ex, fy, w * 0.42, fh, fill=(0, 51, 153))
    ecx, ecy, er = ex + w * 0.21, fy + fh / 2, min(w * 0.42, fh) * 0.32
    for i in range(12):
        a = i * math.pi / 6
        p.circle(ecx + er * math.cos(a), ecy + er * math.sin(a), 2.4, fill=(255, 204, 0))
    # handshake arrows
    mx = x + w / 2
    p.line([(mx - 10, y + h / 2), (mx + 10, y + h / 2)], fill=INK, width=2)
    p.poly([(mx + 10, y + h / 2 - 5), (mx + 16, y + h / 2), (mx + 10, y + h / 2 + 5)], fill=INK)
    p.poly([(mx - 10, y + h / 2 - 5), (mx - 16, y + h / 2), (mx - 10, y + h / 2 + 5)], fill=INK)


def il_cop(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(220, 236, 236))
    gx, gy, gr = x + w * 0.30, y + h * 0.55, h * 0.36
    p.circle(gx, gy, gr, fill=(70, 140, 200))
    p.poly([(gx - gr * 0.5, gy - gr * 0.6), (gx + gr * 0.1, gy - gr * 0.7), (gx + gr * 0.3, gy - gr * 0.1),
            (gx - gr * 0.1, gy + gr * 0.4), (gx - gr * 0.6, gy + gr * 0.1)], fill=(90, 170, 90))
    # thermometer
    tx = x + w * 0.62
    p.rrect(tx, y + 10, 10, h - 34, 5, fill=(255, 255, 255), outline=GREY, width=1)
    p.rect(tx + 3, y + h * 0.35, 4, h * 0.45, fill=RED)
    p.circle(tx + 5, y + h - 18, 9, fill=RED)
    # clock
    cx, cy, r = x + w * 0.84, y + h * 0.5, h * 0.26
    p.circle(cx, cy, r, fill=(255, 255, 255), outline=INK, width=2)
    p.line([(cx, cy), (cx, cy - r * 0.7)], fill=INK, width=2)
    p.line([(cx, cy), (cx + r * 0.5, cy + r * 0.1)], fill=INK, width=2)


def il_field_missile(p, x, y, w, h):
    p.rect(x, y, w, h * 0.55, fill=(200, 220, 235))
    p.rect(x, y + h * 0.55, w, h * 0.45, fill=(120, 160, 90))
    for i in range(5):
        tx = x + w * (0.08 + i * 0.22)
        p.poly([(tx, y + h * 0.55), (tx + 7, y + h * 0.30), (tx + 14, y + h * 0.55)], fill=(50, 100, 60))
    mx, my = x + w * 0.42, y + h * 0.70
    p.poly([(mx, my), (mx + w * 0.30, my - 8), (mx + w * 0.34, my - 4), (mx + w * 0.30, my + 1)],
           fill=(110, 115, 120))
    p.poly([(mx + 6, my - 2), (mx - 4, my - 12), (mx + 2, my - 1)], fill=(90, 95, 100))
    p.ellipse(mx - 12, my - 2, 36, 10, fill=(90, 70, 50))


def il_tanks(p, x, y, w, h):
    p.rect(x, y, w, h * 0.6, fill=(240, 215, 160))
    p.rect(x, y + h * 0.6, w, h * 0.4, fill=(214, 184, 120))
    p.circle(x + w * 0.82, y + h * 0.25, 12, fill=(250, 190, 60))
    for i in range(3):
        tx, ty = x + w * (0.08 + i * 0.30), y + h * 0.62
        p.rrect(tx, ty, w * 0.22, 12, 4, fill=(70, 85, 55))
        p.rect(tx + w * 0.05, ty - 9, w * 0.11, 10, fill=(85, 100, 65))
        p.line([(tx + w * 0.15, ty - 5), (tx + w * 0.26, ty - 9)], fill=(70, 85, 55), width=3)
        for k in range(4):
            p.circle(tx + 5 + k * w * 0.05, ty + 13, 3, fill=(40, 45, 35))


def il_crowd(p, x, y, w, h, sign=""):
    p.rect(x, y, w, h, fill=(232, 228, 222))
    for i in range(11):
        cx = x + 10 + i * (w - 20) / 10
        cy = y + h * 0.62 + (i % 2) * 6
        col = (40, 44, 52) if i % 3 else (90, 40, 40)
        p.circle(cx, cy - 12, 6, fill=col)
        p.rrect(cx - 7, cy - 5, 14, 26, 5, fill=col)
    if sign:
        f = font("sansb", 12)
        sw = p.tw(sign, f) + 12
        sx = x + w * 0.55 - sw / 2
        p.line([(sx + sw / 2, y + 38), (sx + sw / 2, y + h * 0.55)], fill=(100, 70, 40), width=2)
        p.rect(sx, y + 18, sw, 22, fill=(255, 255, 255), outline=RED, width=2)
        p.text(sx + sw / 2, y + 29, sign, f, RED, anchor="mm")


def il_bars(p, x, y, w, h, up=True, col=RED):
    p.rect(x, y, w, h, fill=(240, 236, 228))
    n = 6
    vals = [0.35, 0.42, 0.40, 0.55, 0.62, 0.80] if up else [0.80, 0.70, 0.72, 0.55, 0.45, 0.30]
    bw = (w - 30) / n
    for i, v in enumerate(vals):
        bh = v * (h - 18)
        p.rect(x + 15 + i * bw + 3, y + h - 8 - bh, bw - 6, bh, fill=col if i == n - 1 else (150, 156, 166))
    p.line([(x + 10, y + h - 8), (x + w - 10, y + h - 8)], fill=INK, width=1.5)


def il_building(p, x, y, w, h, sky=(214, 226, 238)):
    p.rect(x, y, w, h, fill=sky)
    bx, bw = x + w * 0.18, w * 0.64
    p.poly([(bx - 6, y + h * 0.34), (bx + bw / 2, y + 8), (bx + bw + 6, y + h * 0.34)], fill=(245, 245, 245),
           outline=GREY)
    p.rect(bx, y + h * 0.34, bw, 6, fill=(245, 245, 245))
    for i in range(6):
        p.rect(bx + 6 + i * (bw - 12) / 5 - 4, y + h * 0.34 + 6, 8, h * 0.44, fill=(250, 250, 250), outline=(190, 190, 195))
    p.rect(bx - 10, y + h * 0.78, bw + 20, h * 0.22, fill=(205, 205, 210))


def il_derrick(p, x, y, w, h):
    for i in range(int(h)):
        t = i / h
        p.rect(x, y + i, w, 1, fill=(int(250 - 40 * t), int(170 - 60 * t), int(90 - 40 * t)))
    p.rect(x, y + h * 0.80, w, h * 0.20, fill=(120, 80, 50))
    dx, dy = x + w * 0.5, y + 8
    base = y + h * 0.80
    p.line([(dx - 22, base), (dx, dy), (dx + 22, base)], fill=(40, 30, 30), width=3)
    for k in range(1, 5):
        yy = dy + (base - dy) * k / 5
        half = 22 * k / 5
        p.line([(dx - half, yy), (dx + half, yy)], fill=(40, 30, 30), width=1.5)
    p.circle(x + w * 0.82, y + h * 0.45, 11, fill=(255, 220, 140))


def il_ballot(p, x, y, w, h, col=(30, 70, 150)):
    p.rect(x, y, w, h, fill=(226, 232, 242))
    bx, by, bw, bh = x + w * 0.30, y + h * 0.42, w * 0.40, h * 0.48
    p.rect(bx, by, bw, bh, fill=col)
    p.rect(bx + bw * 0.25, by + 4, bw * 0.5, 4, fill=(10, 20, 40))
    p.poly([(bx + bw * 0.32, by + 6), (bx + bw * 0.38, by - h * 0.30), (bx + bw * 0.72, by - h * 0.26),
            (bx + bw * 0.66, by + 6)], fill=(255, 255, 255), outline=GREY)
    p.line([(bx + bw * 0.45, by - h * 0.12), (bx + bw * 0.50, by - h * 0.06), (bx + bw * 0.62, by - h * 0.22)],
           fill=RED, width=2.5)


def il_cricket(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(96, 160, 80))
    p.ellipse(x + w * 0.1, y + h * 0.15, w * 0.8, h * 1.2, fill=(120, 180, 96))
    p.rect(x + w * 0.42, y + h * 0.3, w * 0.16, h * 0.7, fill=(210, 190, 130))
    for i in range(3):
        p.rect(x + w * 0.46 + i * 6, y + h * 0.18, 3, 22, fill=(250, 245, 230))
    p.poly([(x + w * 0.18, y + h * 0.85), (x + w * 0.24, y + h * 0.88), (x + w * 0.38, y + h * 0.30),
            (x + w * 0.34, y + h * 0.28)], fill=(220, 190, 120))
    p.circle(x + w * 0.75, y + h * 0.40, 6, fill=(190, 30, 30))


def il_ship_fire(p, x, y, w, h):
    p.rect(x, y, w, h * 0.6, fill=(220, 210, 200))
    p.rect(x, y + h * 0.6, w, h * 0.4, fill=(50, 90, 130))
    sx, sy = x + w * 0.12, y + h * 0.52
    p.poly([(sx, sy), (sx + w * 0.76, sy), (sx + w * 0.70, sy + 16), (sx + 6, sy + 16)], fill=(120, 40, 40))
    p.rect(sx + w * 0.55, sy - 16, w * 0.14, 16, fill=(235, 235, 235))
    for i in range(4):
        fx = sx + w * (0.15 + 0.08 * i)
        p.poly([(fx, sy), (fx + 6, sy - 22 - (i % 2) * 8), (fx + 12, sy)], fill=(250, 130, 30))
        p.poly([(fx + 3, sy), (fx + 6, sy - 10), (fx + 9, sy)], fill=(255, 220, 90))
    p.ellipse(sx + w * 0.10, y + 6, w * 0.36, h * 0.25, fill=(120, 120, 120))


def il_flag(p, x, y, w, h, stripes, vertical=False, emblem=None):
    p.rect(x, y, w, h, fill=(235, 235, 235))
    n = len(stripes)
    for i, c in enumerate(stripes):
        if vertical:
            p.rect(x + i * w / n, y, w / n + 1, h, fill=c)
        else:
            p.rect(x, y + i * h / n, w, h / n + 1, fill=c)
    if emblem:
        emblem(p, x, y, w, h)


def il_pill(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(226, 238, 248))
    cx, cy = x + w * 0.4, y + h * 0.5
    p.rrect(cx - 40, cy - 14, 80, 28, 14, fill=(255, 255, 255), outline=(60, 80, 120), width=2)
    p.d.rounded_rectangle([(cx - 40) * S, (cy - 14) * S, cx * S, (cy + 14) * S], 14 * S, fill=(40, 90, 170))


def il_gavel(p, x, y, w, h):
    """A judge's gavel striking its block, on a parliament-red ground."""
    p.rect(x, y, w, h, fill=(200, 40, 40))
    p.rect(x, y + h * 0.80, w, h * 0.20, fill=(150, 25, 30))
    # yellow star (Vietnam), right side
    sx, sy, r = x + w * 0.80, y + h * 0.42, h * 0.26
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
    p.poly(pts, fill=(255, 215, 0))
    # sound block
    p.rrect(x + w * 0.30, y + h * 0.70, w * 0.30, h * 0.14, 3, fill=(110, 70, 40))
    # gavel: handle then head, tilted
    hx, hy = x + w * 0.44, y + h * 0.64
    p.line([(hx, hy - 6), (hx + w * 0.22, hy - h * 0.48)], fill=(140, 95, 55), width=5)
    p.poly([(hx - 22, hy - 20), (hx + 2, hy - 34), (hx + 14, hy - 12), (hx - 10, hy + 2)], fill=(120, 78, 44))
    p.poly([(hx - 26, hy - 18), (hx - 20, hy - 22), (hx - 8, hy + 0), (hx - 14, hy + 4)], fill=(212, 175, 55))


def il_virus(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(236, 230, 240))
    cx, cy, r = x + w * 0.5, y + h * 0.52, h * 0.30
    for i in range(10):
        a = i * math.pi / 5
        p.line([(cx + r * math.cos(a), cy + r * math.sin(a)),
                (cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a))], fill=(140, 40, 90), width=2.5)
        p.circle(cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a), 3, fill=(140, 40, 90))
    p.circle(cx, cy, r, fill=(190, 70, 120))
    p.circle(cx - r * 0.3, cy - r * 0.2, r * 0.18, fill=(220, 120, 160))
    p.circle(cx + r * 0.3, cy + r * 0.25, r * 0.14, fill=(220, 120, 160))


def il_football(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(70, 150, 80))
    for i in range(6):
        if i % 2:
            p.rect(x + i * w / 6, y, w / 6, h, fill=(80, 162, 90))
    p.rect(x + 6, y + 6, w - 12, h - 12, outline=(240, 240, 240), width=1.5)
    p.line([(x + w / 2, y + 6), (x + w / 2, y + h - 6)], fill=(240, 240, 240), width=1.5)
    p.circle(x + w / 2, y + h / 2, h * 0.22, outline=(240, 240, 240), width=1.5)
    bx, by = x + w * 0.70, y + h * 0.55
    p.circle(bx, by, 8, fill=(255, 255, 255), outline=INK, width=1)
    p.circle(bx, by, 3, fill=INK)


def il_bag(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(238, 232, 220))
    bx, by, bw, bh = x + w * 0.32, y + h * 0.34, w * 0.36, h * 0.56
    p.d.arc([(bx + bw * 0.25) * S, (by - bh * 0.35) * S, (bx + bw * 0.75) * S, (by + bh * 0.25) * S],
            180, 360, fill=INK, width=int(2.5 * S))
    p.rect(bx, by, bw, bh, fill=(40, 110, 170))
    p.rect(bx + 6, by + 10, 10, 18, fill=(250, 200, 80))
    p.rect(bx + 20, by + 6, 12, 22, fill=(230, 90, 60))


def il_port_strike(p, x, y, w, h):
    p.rect(x, y, w, h * 0.55, fill=(70, 60, 70))
    p.rect(x, y + h * 0.55, w, h * 0.45, fill=(40, 80, 110))
    for i in range(3):  # cranes
        cx = x + w * (0.15 + 0.25 * i)
        p.line([(cx, y + h * 0.55), (cx, y + h * 0.18), (cx + 22, y + h * 0.18)], fill=(200, 160, 60), width=2.5)
    ex, ey = x + w * 0.70, y + h * 0.42
    p.circle(ex, ey, 18, fill=(250, 120, 30))
    p.circle(ex, ey, 10, fill=(255, 225, 120))
    p.ellipse(ex - 30, ey - 40, 50, 24, fill=(110, 105, 110))


def il_chip(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(24, 34, 30))
    cx, cy, cs = x + w * 0.32, y + h * 0.5, h * 0.36
    for i in range(5):
        o = -cs + (i + 0.5) * 2 * cs / 5
        p.line([(cx - cs - 8, cy + o), (cx + cs + 8, cy + o)], fill=(200, 170, 80), width=2)
        p.line([(cx + o, cy - cs - 8), (cx + o, cy + cs + 8)], fill=(200, 170, 80), width=2)
    p.rect(cx - cs, cy - cs, 2 * cs, 2 * cs, fill=(60, 180, 90))
    p.rect(cx - cs * 0.5, cy - cs * 0.5, cs, cs, fill=(30, 120, 60))
    pts = [(x + w * 0.62, y + h * 0.2), (x + w * 0.72, y + h * 0.35), (x + w * 0.78, y + h * 0.3),
           (x + w * 0.9, y + h * 0.78)]
    p.line(pts, fill=(240, 70, 60), width=3)
    ex, ey = pts[-1]
    p.poly([(ex - 7, ey - 3), (ex + 3, ey + 8), (ex + 6, ey - 6)], fill=(240, 70, 60))


def il_board(p, x, y, w, h):
    p.rect(x, y, w, h, fill=(150, 110, 70))
    p.rect(x + 5, y + 5, w - 10, h - 10, fill=(34, 62, 50))
    f = font("serifi", 17)
    p.text(x + w * 0.62, y + h * 0.66, "ζ(s) = 0", f, (240, 240, 230), anchor="mm")


def il_flag_mx(p, x, y, w, h):
    il_flag(p, x, y, w, h, [(0, 104, 71), (255, 255, 255), (206, 17, 38)], vertical=True)
    cx, cy = x + w / 2, y + h / 2
    p.circle(cx, cy, h * 0.17, fill=(150, 100, 50))
    p.circle(cx, cy, h * 0.09, fill=(90, 130, 60))


def il_cnau(p, x, y, w, h):
    """China and Australia flags, simplified, with a handshake arrow."""
    p.rect(x, y, w, h, fill=(232, 236, 244))
    fy, fh, fw = y + 8, h - 16, w * 0.40
    cx0 = x + 6
    p.rect(cx0, fy, fw, fh, fill=(222, 41, 16))

    def star(sx, sy, r, col):
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.42
            pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
        p.poly(pts, fill=col)

    star(cx0 + fw * 0.22, fy + fh * 0.32, fh * 0.20, (255, 222, 0))
    for k, (dx, dy) in enumerate([(0.42, 0.14), (0.50, 0.30), (0.50, 0.52), (0.42, 0.68)]):
        star(cx0 + fw * dx, fy + fh * dy, fh * 0.07, (255, 222, 0))
    ax0 = x + w - 6 - fw
    p.rect(ax0, fy, fw, fh, fill=(0, 33, 125))
    q = (ax0, fy, fw / 2, fh / 2)
    p.line([(q[0], q[1]), (q[0] + q[2], q[1] + q[3])], fill=(255, 255, 255), width=3)
    p.line([(q[0], q[1] + q[3]), (q[0] + q[2], q[1])], fill=(255, 255, 255), width=3)
    p.rect(q[0] + q[2] / 2 - 2.5, q[1], 5, q[3], fill=(228, 0, 43))
    p.rect(q[0], q[1] + q[3] / 2 - 2.5, q[2], 5, fill=(228, 0, 43))
    star(ax0 + fw * 0.25, fy + fh * 0.76, fh * 0.12, (255, 255, 255))
    for dx, dy in [(0.75, 0.25), (0.62, 0.50), (0.86, 0.45), (0.75, 0.82)]:
        star(ax0 + fw * dx, fy + fh * dy, fh * 0.06, (255, 255, 255))
    mx = x + w / 2
    p.line([(mx - 10, y + h / 2), (mx + 10, y + h / 2)], fill=INK, width=2)
    p.poly([(mx + 10, y + h / 2 - 5), (mx + 16, y + h / 2), (mx + 10, y + h / 2 + 5)], fill=INK)
    p.poly([(mx - 10, y + h / 2 - 5), (mx - 16, y + h / 2), (mx - 10, y + h / 2 + 5)], fill=INK)


ILLUS = {
    "cnau": il_cnau, "board": il_board, "flag_mx": il_flag_mx,
    "virus": il_virus, "football": il_football, "bag": il_bag, "port_strike": il_port_strike,
    "chip": il_chip,
    "kyiv": il_kyiv, "cyclone": il_cyclone, "markets": il_markets, "ukeu": il_flags_ukeu,
    "cop": il_cop, "field_missile": il_field_missile, "tanks": il_tanks, "crowd": il_crowd,
    "bars": il_bars, "building": il_building, "derrick": il_derrick, "ballot": il_ballot,
    "cricket": il_cricket, "ship_fire": il_ship_fire, "flag": il_flag, "pill": il_pill,
    "gavel": il_gavel,
}


def illus(p, spec, x, y, w, h):
    """Draw one illustration, clipped to its own box."""
    name, kw = spec[0], (spec[1] if len(spec) > 1 else {})
    before = p.im.copy()
    ILLUS[name](p, x, y, w, h, **kw)
    box = (int(x * S), int(y * S), int((x + w) * S), int((y + h) * S))
    inside = p.im.crop(box)
    p.im.paste(before)
    p.im.paste(inside, box[:2])


# ---------------------------------------------------------------------
# schematic world map (equirectangular, coarse continent outlines)
# ---------------------------------------------------------------------
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-95, 72), (-80, 64), (-62, 58), (-55, 48), (-66, 44), (-76, 35), (-81, 25),
     (-90, 29), (-97, 26), (-97, 19), (-88, 15), (-78, 8), (-84, 9), (-92, 15), (-105, 20), (-112, 30),
     (-118, 34), (-124, 42), (-124, 49), (-133, 56), (-150, 60), (-165, 60)],
    # Greenland
    [(-55, 82), (-25, 82), (-20, 70), (-42, 60), (-52, 66)],
    # South America
    [(-78, 8), (-60, 10), (-50, 0), (-35, -6), (-39, -15), (-48, -26), (-58, -38), (-65, -42), (-68, -54),
     (-74, -50), (-72, -30), (-70, -18), (-81, -5)],
    # Europe + Asia
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (5, 54), (10, 58), (5, 62), (15, 69), (30, 71), (50, 69),
     (70, 73), (100, 77), (140, 73), (180, 69), (178, 62), (160, 60), (142, 52), (135, 43), (128, 35),
     (121, 31), (120, 23), (108, 21), (105, 10), (100, 14), (98, 8), (100, 2), (95, 16), (90, 22),
     (80, 15), (77, 8), (72, 20), (67, 25), (57, 25), (56, 27), (50, 30), (48, 29), (52, 24), (59, 22),
     (54, 17), (44, 12), (38, 22), (34, 28), (35, 33), (36, 36), (28, 37), (26, 40), (22, 37), (18, 40),
     (12, 44), (8, 44), (3, 43), (-2, 37)],
    # Africa
    [(-17, 21), (-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 12), (40, -2), (40, -15),
     (35, -24), (20, -35), (17, -29), (12, -17), (13, -5), (9, 4), (-8, 4), (-16, 12)],
    # Arabia filled by Eurasia polygon; Madagascar
    [(44, -13), (50, -15), (47, -25), (43, -22)],
    # Australia
    [(114, -22), (122, -18), (131, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37),
     (141, -38), (131, -31), (116, -35), (114, -29)],
    # New Zealand
    [(172, -34), (178, -38), (174, -42), (166, -46), (170, -44)],
    # UK
    [(-5, 50), (1, 51), (-2, 56), (-5, 58), (-6, 55)],
    # Japan
    [(130, 31), (135, 34), (140, 36), (141, 41), (143, 44), (140, 41), (136, 37), (131, 34)],
    # Indonesia (Sumatra, Borneo)
    [(95, 5), (106, -6), (102, -5), (98, 0)],
    [(109, 1), (117, 7), (119, 0), (116, -4), (110, -3)],
]


def draw_map(p, x, y, w, h, pins):
    p.rect(x, y, w, h, fill=(30, 52, 82))
    lon0, lon1, lat0, lat1 = -170, 180, -50, 78

    def proj(lon, lat):
        return x + (lon - lon0) / (lon1 - lon0) * w, y + (lat1 - lat) / (lat1 - lat0) * h

    for c in CONTINENTS:
        p.poly([proj(a, b) for a, b in c], fill=(214, 200, 160))
    placed = []
    for n, lon, lat, region in pins:
        px, py = proj(lon, lat)
        for qx, qy in placed:  # nudge apart overlapping pins
            if abs(qx - px) < 15 and abs(qy - py) < 15:
                py += 15
        placed.append((px, py))
        p.numdot(px, py, n, REGION_COL[region], r=7.5, size=9)


# ---------------------------------------------------------------------
# page layout
# ---------------------------------------------------------------------

def render(out_path):
    p = Page()
    M = 16
    CW = W - 2 * M

    # top line
    p.text(M, 8, "THE WORLD IN ONE DAY", font("sansb", 12), RED)
    p.text(W - M, 8, ST.TOPLINE, font("sansb", 12), INK, anchor="ra")
    p.rect(M, 26, CW, 3, fill=RULE)
    # masthead
    ms = ST.MAST_SIZE
    while p.tw("Friday 20 November 2026", font("serifb", ms)) > CW - 8:
        ms -= 1
    p.text(W / 2, 26 + (ST.MAST_SIZE - ms) * 0.6, "Friday 20 November 2026", font("serifb", ms), INK, anchor="ma")
    p.text(W / 2, 122, ST.SUBLINE, font("serifi", 17), INK, anchor="ma")
    p.rect(M, 148, CW, 1.5, fill=RULE)

    # timeline strip (UTC)
    y = 153
    p.rect(M, y, 80, 42, fill=RED)
    p.text(M + 40, y + 21, "THE DAY", font("sansb", 12), (255, 255, 255), anchor="md")
    p.text(M + 40, y + 23, "IN UTC", font("sansb", 12), (255, 255, 255), anchor="ma")
    n = len(ST.TIMELINE)
    cw = (CW - 86) / n
    for i, (t, lab) in enumerate(ST.TIMELINE):
        cx = M + 86 + i * cw
        if i:
            p.rect(cx, y + 4, 1, 34, fill=(190, 186, 176))
        p.text(cx + cw / 2, y, t, font("serifb", 18), RED, anchor="ma")
        if p.tw(lab, font("sans", 13)) > cw - 6:
            raise ValueError("timeline label too long: " + lab)
        p.text(cx + cw / 2, y + 23, lab, font("sans", 13), INK, anchor="ma")
    p.rect(M, 200, CW, 1.5, fill=RULE)

    # region bar: how many stories from each region
    y = 205
    counts = {}
    for d in ST.LEADS + ST.TILES:
        counts[d["region"]] = counts.get(d["region"], 0) + 1
    for b in ST.BRIEFS:
        counts[b[3]] = counts.get(b[3], 0) + 1
    order = ["Europe", "Asia", "Middle East", "Africa", "Americas", "Oceania", "Global"]
    regions = [(r_, counts[r_]) for r_ in order if r_ in counts]
    total = sum(cnt for _, cnt in regions)
    if ("%d STORIES" % total) not in ST.TOPLINE or ("%d REGIONS" % len(regions)) not in ST.TOPLINE:
        ERRORS.append("TOPLINE counts disagree: %d stories, %d regions" % (total, len(regions)))
    tot = sum(max(cnt, 3) for _, cnt in regions)
    rx = M
    for name, cnt in regions:
        rw = CW * max(cnt, 3) / tot
        p.rect(rx, y, rw - 2, 18, fill=REGION_COL[name])
        p.text(rx + rw / 2 - 1, y + 9, "%s %d" % (name, cnt), font("sansb", 12), (255, 255, 255), anchor="mm")
        rx += rw

    # three leads
    y = 229
    IH = 110
    gap = 14
    lw = (CW - 2 * gap) / 3
    for i, s in enumerate(ST.LEADS):
        x = M + i * (lw + gap)
        illus(p, s["ill"], x, y, lw, IH)
        p.badge(x + 7, y + 7, s["tag"], size=17, fill=RED)
        if s.get("src_tag"):
            f = font("sansb", 12)
            tw = p.tw(s["src_tag"], f) + 10
            p.rect(x + 6, y + IH - 23, tw, 17, fill=(15, 15, 20))
            p.text(x + 11, y + IH - 14.5, s["src_tag"], f, (255, 255, 255), anchor="lm")
        ty = y + IH + 6
        p.numdot(x + 9, ty + 8, s["n"], REGION_COL[s["region"]], r=9, size=11)
        p.fit_line(x + 23, ty + 1, s["place"].upper(), font("sansb", 12), lw - 24, REGION_COL[s["region"]], "lead place")
        p.para(x, ty + 19, s["head"], font("serifb", 23), lw, 27, 2, INK, "lead head")
        p.para(x, ty + 76, s["dek"], font("sans", 14), lw, 18, 3, (40, 42, 48), "lead dek")

    p.rect(M, 482, CW, 1.5, fill=RULE)
    # tiles: two rows of five
    tw_ = (CW - 4 * 12) / 5
    for i, s in enumerate(ST.TILES):
        r, c = divmod(i, 5)
        x = M + c * (tw_ + 12)
        ty = 489 + r * 140
        illus(p, s["ill"], x, ty, tw_, 54)
        p.badge(x + 5, ty + 5, s["tag"], size=13, fill=RED)
        p.numdot(x + 8, ty + 66, s["n"], REGION_COL[s["region"]], r=8, size=10)
        p.fit_line(x + 20, ty + 59, s["place"].upper(), font("sansb", 11), tw_ - 20, REGION_COL[s["region"]], "tile place")
        p.para(x, ty + 75, s["head"], font("serifb", 17), tw_, 20, 2, INK, "tile head")
        p.para(x, ty + 117, s["dek"], font("sans", 13), tw_, 16, 1, (40, 42, 48), "tile dek")

    p.rect(M, 772, CW, 1.5, fill=RULE)
    # map + one-liners
    y = 777
    p.text(M, y, "WHERE IT HAPPENED", font("sansb", 12), RED)
    mw, mh = 276, 138
    draw_map(p, M, y + 18, mw, mh, ST.PINS)
    lx = M + mw + 14
    p.text(lx, y, "ALSO ON FRIDAY 20 NOVEMBER", font("sansb", 12), RED)
    colw = (W - M - lx - 14) / 2
    fb = font("sansb", 14)
    fr = font("sans", 14)
    per = (len(ST.BRIEFS) + 1) // 2
    if per > 9:
        raise ValueError("too many briefs")
    for i, (n, place, txt, region) in enumerate(ST.BRIEFS):
        c, r = divmod(i, per)
        bx = lx + c * (colw + 14)
        by = y + 17 + r * 16.6
        p.text(bx, by, "%d" % n, fb, REGION_COL[region])
        px = bx + 21
        p.text(px, by, place, fb, INK)
        tx = px + p.tw(place + " ", fb)
        p.fit_line(tx, by, txt, fr, bx + colw - tx, INK, "brief %d" % n)

    # date check
    y = 959
    p.rect(M, y - 5, CW, 2 * 16 + 9, outline=RED, width=1.5)
    p.text(M + 8, y, "DATE CHECK", font("sansb", 12), RED)
    p.para(M + 94, y, ST.DATE_CHECK, font("sans", 12), CW - 104, 16, 2, INK, "date check")
    p.text(M, 1007, ST.FOOT_L, font("sans", 11), GREY)
    p.text(W - M, 1007, ST.FOOT_R, font("sans", 11), GREY, anchor="ra")

    if ERRORS:
        raise SystemExit("layout errors:\n  " + "\n  ".join(ERRORS))
    out = p.im.resize((W, H), Image.LANCZOS)
    out = out.quantize(colors=ST.COLORS, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    out.save(out_path, optimize=True)
    return out


if __name__ == "__main__":
    dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
