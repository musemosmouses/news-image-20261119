#!/usr/bin/env python3
"""Draw 'The World in One Image - 19 November 2026'.

One editorial front-page image, 1024x1024 PNG, drawn with PIL only.
Deterministic: fixed geometry, no randomness, no timestamps, no network.
Run: python3 draw.py  ->  writes entry.png beside this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
RED = (163, 22, 33)
INK = (20, 20, 20)
GOLD = (198, 158, 60)
GREY = (90, 90, 90)
SKY = (188, 214, 232)
SUN = (242, 193, 78)
GREEN = (26, 127, 75)
SAND = (234, 223, 195)
CLOUD = (255, 255, 255)
SKY2 = (168, 202, 228)
SKY3 = (146, 190, 220)
TENT = (214, 172, 118)
TENT_D = (178, 138, 88)
BUSH = (122, 148, 84)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(d, y, text, fnt, fill, x0=0, x1=W):
    w = fnt.getlength(text)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def star(d, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def cloud(d, x, y, s):
    """A small flat-bottomed cloud from overlapping ellipses."""
    d.ellipse([x, y, x + 34 * s, y + 16 * s], fill=CLOUD)
    d.ellipse([x + 10 * s, y - 8 * s, x + 34 * s, y + 10 * s], fill=CLOUD)
    d.ellipse([x + 22 * s, y - 2 * s, x + 46 * s, y + 14 * s], fill=CLOUD)
    d.rectangle([x, y + 8 * s, x + 46 * s, y + 16 * s], fill=CLOUD)


def bird(d, x, y, s):
    """A tiny two-stroke gull, drawn as one polyline."""
    d.line([(x, y), (x + 6 * s, y - 5 * s), (x + 12 * s, y)],
           fill=INK, width=2)
    d.line([(x + 12 * s, y), (x + 18 * s, y - 5 * s), (x + 24 * s, y)],
           fill=INK, width=2)


def figure(d, x, y, s, fill):
    """A tiny walking person: head, body, legs, one arm forward."""
    d.ellipse([x - 3 * s, y - 16 * s, x + 3 * s, y - 10 * s], fill=fill)
    d.line([x, y - 10 * s, x, y], fill=fill, width=3)
    d.line([x, y, x - 5 * s, y + 9 * s], fill=fill, width=3)
    d.line([x, y, x + 6 * s, y + 8 * s], fill=fill, width=3)
    d.line([x, y - 8 * s, x + 7 * s, y - 3 * s], fill=fill, width=2)


def brief_icon(d, idx, cx, cy):
    """One small gold icon per 'THE DAY IN BRIEF' item, centred on (cx, cy)."""
    g = GOLD
    if idx == 0:  # Crimea Bridge: arc deck with two posts
        d.arc([cx - 9, cy - 4, cx + 9, cy + 12], 180, 360, fill=g, width=2)
        d.line([cx - 9, cy + 4, cx + 9, cy + 4], fill=g, width=2)
        d.line([cx - 6, cy + 4, cx - 6, cy + 9], fill=g, width=2)
        d.line([cx + 6, cy + 4, cx + 6, cy + 9], fill=g, width=2)
    elif idx == 1:  # Voyager 1: four-point star
        star(d, cx, cy, 10, 3, g)
    elif idx == 2:  # EU loan: coin with a euro sign
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=g, width=2)
        d.text((cx - 5, cy - 8), "\u20ac", font=font(SANS_B, 14), fill=g)
    elif idx == 3:  # North Korea missiles: rocket with a trail
        d.polygon([(cx, cy - 10), (cx + 4, cy + 2), (cx - 4, cy + 2)],
                  fill=g)
        d.line([cx, cy + 3, cx, cy + 10], fill=g, width=2)
    elif idx == 4:  # Myanmar verdict: scales of justice
        d.line([cx, cy - 9, cx, cy + 9], fill=g, width=2)
        d.line([cx - 9, cy - 6, cx + 9, cy - 6], fill=g, width=2)
        d.arc([cx - 11, cy - 2, cx - 3, cy + 6], 0, 180, fill=g, width=2)
        d.arc([cx + 3, cy - 2, cx + 11, cy + 6], 0, 180, fill=g, width=2)
    elif idx == 5:  # Cyclone Akvan: spiral
        d.arc([cx - 9, cy - 9, cx + 9, cy + 9], 0, 270, fill=g, width=2)
        d.arc([cx - 5, cy - 5, cx + 5, cy + 5], 90, 360, fill=g, width=2)
    else:  # Van Gogh sale: framed picture with a sun
        d.rectangle([cx - 9, cy - 8, cx + 9, cy + 8], outline=g, width=2)
        d.ellipse([cx - 1, cy - 5, cx + 5, cy + 1], fill=g)


def flag_us(d, x, y, w=84, h=50):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK)
    for i in range(7):
        sy = y + i * h / 7
        if i % 2 == 0:
            d.rectangle([x, sy, x + w, sy + h / 7], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            px = x + 5 + c * 8
            py = y + 5 + r * 8
            d.ellipse([px, py, px + 3, py + 3], fill=(255, 255, 255))


def flag_cn(d, x, y, w=84, h=50):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK)
    star(d, x + 16, y + 15, 11, 4.5, (255, 222, 0))
    for sx, sy in [(34, 8), (42, 15), (42, 25), (34, 31)]:
        star(d, x + sx, y + sy, 4.5, 1.8, (255, 222, 0))


def flag_ru(d, x, y, w=84, h=50):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def lead_art(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY, outline=INK, width=2)
    # sky gradient: three soft bands, lighter at the horizon
    d.rectangle([x0 + 2, y0 + 2, x0 + w - 2, y0 + 72], fill=SKY3)
    d.rectangle([x0 + 2, y0 + 72, x0 + w - 2, y0 + 150], fill=SKY2)
    d.rectangle([x0 + 2, y0 + 150, x0 + w - 2, y0 + h - 42], fill=SKY)
    # clouds and gulls in the open sky, clear of the flags
    cloud(d, x0 + 14, y0 + 30, 1.0)
    cloud(d, x0 + 150, y0 + 95, 0.8)
    bird(d, x0 + 100, y0 + 92, 1.0)
    bird(d, x0 + 205, y0 + 105, 0.8)
    bird(d, x0 + 295, y0 + 85, 0.7)
    # sun with short rays, low in the open sky right of the flags
    sx, sy = x0 + w - 36, y0 + 118
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(sx + 26 * math.cos(a), sy + 26 * math.sin(a)),
                (sx + 34 * math.cos(a), sy + 34 * math.sin(a))],
               fill=SUN, width=3)
    d.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=SUN)
    # skyline silhouette, with lit windows and an antenna on the tallest
    base = y0 + h - 40
    buildings = [(0, 46), (34, 70), (74, 52), (108, 84), (150, 60),
                 (186, 92), (226, 58), (262, 76), (300, 50), (336, 66)]
    for bx, bh in buildings:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 34, base],
                    fill=(90, 107, 125))
        for wy in range(base - bh + 8, base - 8, 14):
            for wx in (x0 + bx + 6, x0 + bx + 20):
                d.rectangle([wx, wy, wx + 6, wy + 7], fill=(242, 193, 78))
    d.line([x0 + 186 + 17, base - 92, x0 + 186 + 17, base - 108],
           fill=INK, width=3)
    d.ellipse([x0 + 186 + 14, base - 112, x0 + 186 + 20, base - 106],
              fill=RED)
    # red carpet with a gold diamond at each end, clear of the label
    d.rectangle([x0, base, x0 + w, y0 + h], fill=RED)
    d.rectangle([x0, base, x0 + w, base + 3], fill=GOLD)
    for dx in (x0 + 14, x0 + w - 26):
        d.polygon([(dx + 6, base + 12), (dx + 12, base + 20),
                   (dx + 6, base + 28), (dx, base + 20)], fill=GOLD)
    centered(d, base + 9, "SHENZHEN", font(SANS_B, 20), (255, 255, 255),
             x0, x0 + w)
    # three flagpoles with flags
    for fx, draw_flag in [(x0 + 48, flag_us), (x0 + 148, flag_cn),
                          (x0 + 248, flag_ru)]:
        d.line([fx + 4, y0 + 18, fx + 4, base], fill=INK, width=4)
        d.ellipse([fx, y0 + 12, fx + 8, y0 + 20], fill=GOLD)
        draw_flag(d, fx + 6, y0 + 20)


def ipo_art(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 244, 238),
                outline=INK, width=2)
    d.text((x0 + 12, y0 + 8), "$83", font=font(SANS_B, 30), fill=GREEN)
    d.text((x0 + 96, y0 + 16), "A SHARE", font=font(SANS_B, 18), fill=INK)
    base = y0 + h - 12
    # faint gridlines behind the bars
    for gy in (base - 32, base - 64, base - 96):
        d.line([x0 + 10, gy, x0 + w - 10, gy], fill=(205, 220, 205),
               width=1)
    heights = [26, 42, 58, 74, 96]
    for i, bh in enumerate(heights):
        bx = x0 + 18 + i * 58
        col = GREEN if i == 4 else (110, 168, 110)
        d.rectangle([bx, base - bh, bx + 38, base], fill=col)
        d.ellipse([bx + 15, base - bh - 4, bx + 23, base - bh + 4],
                  fill=GREEN)
    d.line([x0 + 10, base, x0 + w - 10, base], fill=INK, width=2)
    # "$81.3bn raised" chip, top right (figure from the panel body text),
    # drawn after the gridlines and bars so it sits clean on top
    d.rounded_rectangle([x0 + 196, y0 + 10, x0 + w - 10, y0 + 34],
                        radius=10, fill=GREEN)
    d.text((x0 + 206, y0 + 13), "$81.3bn", font=font(SANS_B, 15),
           fill=(255, 255, 255))
    # growth arrow, kept clear of the chip and the tallest bar
    d.line([x0 + 104, y0 + 72, x0 + 205, y0 + 40], fill=RED, width=4)
    d.polygon([(x0 + 205, y0 + 40), (x0 + 187, y0 + 38),
               (x0 + 197, y0 + 54)], fill=RED)
    # ticker chip, in the free space above the first bars
    d.text((x0 + 14, y0 + 48), "NASDAQ: ANT",
           font=font(SANS_B, 13), fill=GREEN)


def gaza_art(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SAND, outline=INK, width=2)
    d.text((x0 + 12, y0 + 8), "CEASEFIRE LINE", font=font(SANS_B, 15),
           fill=RED)
    # dashed ceasefire line with small red posts hanging below each dash
    for i in range(8):
        sx = x0 + 14 + i * 34
        d.line([sx, y0 + 32, sx + 20, y0 + 32], fill=RED, width=3)
        d.line([sx + 10, y0 + 32, sx + 10, y0 + 40], fill=RED, width=2)
    d.ellipse([x0 + w - 44, y0 + 10, x0 + w - 12, y0 + 42], fill=SUN)
    cloud(d, x0 + 18, y0 + 52, 0.7)
    base = y0 + h - 10
    # low hills on the horizon, behind the tents
    d.ellipse([x0 - 20, base - 34, x0 + 90, base - 6], fill=(222, 205, 168))
    d.ellipse([x0 + 210, base - 30, x0 + w + 10, base - 6],
              fill=(222, 205, 168))
    # tents: trapezoid canvas, centre pole, flap line, ground shadow
    for tx, tw, th in [(30, 84, 52), (130, 96, 62), (238, 70, 44)]:
        d.ellipse([x0 + tx - 6, base - 4, x0 + tx + tw + 6, base + 4],
                  fill=(200, 185, 150))
        d.polygon([(x0 + tx, base), (x0 + tx + 14, base - th),
                   (x0 + tx + tw - 14, base - th), (x0 + tx + tw, base)],
                  fill=TENT, outline=(120, 85, 50))
        d.line([x0 + tx + tw / 2, base - th - 8,
                x0 + tx + tw / 2, base - th], fill=(120, 85, 50), width=2)
        d.polygon([(x0 + tx + tw / 2 - 7, base),
                   (x0 + tx + tw / 2, base - 22),
                   (x0 + tx + tw / 2 + 7, base)], fill=TENT_D)
    # small bushes between the tents, and people fleeing (see body text)
    for bx in (x0 + 118, x0 + 224):
        d.ellipse([bx, base - 16, bx + 18, base - 4], fill=BUSH)
        d.ellipse([bx + 8, base - 22, bx + 24, base - 8], fill=BUSH)
    figure(d, x0 + 292, base - 12, 1.0, (90, 60, 40))
    figure(d, x0 + 306, base - 10, 0.85, (90, 60, 40))


def gta_art(d, x0, y0, w, h):
    bands = [(246, 160, 77), (226, 99, 94), (91, 58, 117)]
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * h / 3, x0 + w, y0 + (i + 1) * h / 3],
                    fill=col)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=2)
    # low sunset sun and a few stars in the dusk band
    d.ellipse([x0 + 118, y0 + 14, x0 + 162, y0 + 58], fill=(255, 214, 120))
    for sx, sy in [(x0 + 30, y0 + 16), (x0 + 200, y0 + 22),
                   (x0 + 280, y0 + 12), (x0 + 96, y0 + 30)]:
        star(d, sx, sy, 5, 2, (255, 255, 255))
    # skyline
    base = y0 + h
    for bx, bh in [(150, 34), (186, 52), (226, 40), (266, 60)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 36, base],
                    fill=(42, 33, 56))
        for wy in range(base - bh + 8, base - 6, 12):
            d.rectangle([x0 + bx + 6, wy, x0 + bx + 12, wy + 6],
                        fill=(255, 214, 120))
    # road along the bottom, with a small car driving into the sunset
    d.rectangle([x0, base - 16, x0 + w, base], fill=(30, 28, 38))
    for dx in range(8, w - 8, 28):
        d.rectangle([x0 + dx, base - 8, x0 + dx + 14, base - 6],
                    fill=(255, 255, 255))
    d.rectangle([x0 + 96, base - 34, x0 + 142, base - 18],
                fill=(220, 60, 60))
    d.rectangle([x0 + 106, base - 44, x0 + 132, base - 34],
                fill=(220, 60, 60))
    d.ellipse([x0 + 102, base - 20, x0 + 114, base - 8], fill=(20, 20, 20))
    d.ellipse([x0 + 126, base - 20, x0 + 138, base - 8], fill=(20, 20, 20))
    # palm tree: curved fronds from the crown
    cx, cy = x0 + 58, base - 66
    d.line([x0 + 46, base, cx, cy], fill=(70, 45, 20), width=7)
    fronds = [((10, -30), (28, -52)), ((6, -58), (30, -66)),
              ((30, -96), (52, -92)), ((86, -96), (66, -92)),
              ((104, -60), (84, -66)), ((100, -34), (84, -48))]
    for (ex, ey), (mx, my) in fronds:
        pts = []
        for t in [i / 12 for i in range(13)]:
            px = (1 - t) ** 2 * cx + 2 * (1 - t) * t * (cx + mx) + t ** 2 * (x0 + ex)
            py = (1 - t) ** 2 * cy + 2 * (1 - t) * t * (cy + my) + t ** 2 * (base + ey)
            pts.append((px, py))
        d.line(pts, fill=(30, 90, 50), width=5)
    # a second, smaller palm on the right, in front of the skyline
    cx2, cy2 = x0 + 296, base - 40
    d.line([x0 + 290, base, cx2, cy2], fill=(70, 45, 20), width=5)
    for (ex, ey) in [(268, -18), (276, -44), (306, -48), (322, -22)]:
        d.line([(cx2, cy2), (x0 + ex, base + ey)], fill=(30, 90, 50),
               width=4)
    d.text((x0 + 12, y0 + h - 34), "VICE CITY",
           font=font(SANS_B, 16), fill=(255, 255, 255))
    d.text((x0 + w - 108, y0 + 18), "VI", font=font(SERIF_B, 72),
           fill=(255, 255, 255))


def panel(d, x0, y0, w, headline, body, art_fn):
    art_h = 130
    art_fn(d, x0, y0, w, art_h)
    y = y0 + art_h + 10
    for line in wrap(headline, font(SANS_B, 26), w):
        d.text((x0, y), line, font=font(SANS_B, 26), fill=INK)
        y += 30
    y += 4
    for line in wrap(body, font(SANS, 19), w):
        d.text((x0, y), line, font=font(SANS, 19), fill=(40, 40, 40))
        y += 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=4)

    # masthead
    d.rectangle([0, 0, W, 88], fill=NAVY)
    centered(d, 16, "THE WORLD IN ONE IMAGE", font(SERIF_B, 50),
             (255, 255, 255))
    # red date band, edged with a thin gold rule
    d.rectangle([0, 88, W, 134], fill=RED)
    d.rectangle([0, 134, W, 137], fill=GOLD)
    centered(d, 96, "THURSDAY 19 NOVEMBER 2026", font(SANS_B, 34),
             (255, 255, 255))

    # lead story
    lead_art(d, 24, 146, 372, 302)
    tx = 420
    d.text((tx, 150), "SUMMIT IN SHENZHEN", font=font(SANS_B, 22), fill=RED)
    y = 184
    for line in wrap("TRUMP, XI & PUTIN MEET IN SHENZHEN",
                     font(SERIF_B, 44), 580):
        d.text((tx, y), line, font=font(SERIF_B, 44), fill=INK)
        y += 52
    d.line([tx, y + 6, 1000, y + 6], fill=RED, width=3)
    y += 22
    sub = ("The first three-way meeting of the three leaders, at the "
           "APEC China 2026 summit. Xi hugged Trump on the tarmac "
           "on arrival.")
    for line in wrap(sub, font(SANS, 22), 580):
        d.text((tx, y), line, font=font(SANS, 22), fill=(40, 40, 40))
        y += 29
    d.text((tx, 416), "SHENZHEN  •  APEC CHINA 2026",
           font=font(SANS_B, 18), fill=GREY)

    # divider
    d.line([24, 466, 1000, 466], fill=INK, width=2)

    # three panels
    panel(d, 24, 478, 320,
          "ANTHROPIC IPO SMASHES RECORDS",
          "Priced at $83 a share, $81.3bn raised - the biggest IPO "
          "ever. Nasdaq debut today, ticker ANT.",
          ipo_art)
    panel(d, 352, 478, 320,
          "ISRAEL PUSHES INTO CENTRAL GAZA",
          "Rare ground operation beyond the ceasefire line. Dozens "
          "flee their tents.",
          gaza_art)
    panel(d, 680, 478, 320,
          "GTA VI ROLLS OUT WORLDWIDE",
          "Gamers return to Vice City as the blockbuster begins "
          "its global rollout.",
          gta_art)

    # divider
    d.line([24, 770, 1000, 770], fill=INK, width=2)

    # ticker
    d.rectangle([0, 782, W, H], fill=NAVY)
    d.text((24, 796), "THE DAY IN BRIEF", font=font(SANS_B, 24),
           fill=GOLD)
    d.line([24, 824, 240, 824], fill=GOLD, width=2)
    # dotted world-map strip in the empty navy space, right of the heading
    for (mx0, mx1, my0, my1) in [(700, 760, 796, 808), (720, 745, 810, 820),
                                 (830, 855, 796, 804), (835, 865, 806, 820),
                                 (880, 970, 796, 812), (930, 960, 816, 822)]:
        for mx in range(mx0, mx1, 8):
            for my in range(my0, my1, 6):
                if (mx + my) // 8 % 3:
                    d.rectangle([mx, my, mx + 3, my + 3], fill=GOLD)
    items = [
        "Crimea Bridge attacked again - traffic suspended",
        "NASA's Voyager 1 reaches one light-day from Earth after ~50 years",
        "EU proposes a 45 billion euro loan for Ukraine",
        "North Korea fires ballistic missiles after US-South Korea drill",
        "Myanmar faces historic genocide verdict at UN court over Rohingya",
        "Cyclone Akvan nears India",
        "Van Gogh painting sells for record $190.4m",
    ]
    y = 832
    for i, it in enumerate(items):
        brief_icon(d, i, 34, y + 10)
        d.text((48, y), it, font=font(SANS, 19), fill=(255, 255, 255))
        y += 26

    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
    print("wrote", OUT)
