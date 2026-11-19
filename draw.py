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
    # sun, low in the open sky right of the flags
    d.ellipse([x0 + w - 58, y0 + 96, x0 + w - 14, y0 + 140], fill=SUN)
    # skyline silhouette
    base = y0 + h - 40
    buildings = [(0, 46), (34, 70), (74, 52), (108, 84), (150, 60),
                 (186, 92), (226, 58), (262, 76), (300, 50), (336, 66)]
    for bx, bh in buildings:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 34, base],
                    fill=(90, 107, 125))
    # red carpet
    d.rectangle([x0, base, x0 + w, y0 + h], fill=RED)
    d.rectangle([x0, base, x0 + w, base + 3], fill=GOLD)
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
    heights = [26, 42, 58, 74, 96]
    for i, bh in enumerate(heights):
        bx = x0 + 18 + i * 58
        col = GREEN if i == 4 else (110, 168, 110)
        d.rectangle([bx, base - bh, bx + 38, base], fill=col)
    d.line([x0 + 10, base, x0 + w - 10, base], fill=INK, width=2)
    # growth arrow, kept clear of the "$83" label and the tallest bar
    d.line([x0 + 104, y0 + 72, x0 + 238, y0 + 32], fill=RED, width=4)
    d.polygon([(x0 + 238, y0 + 32), (x0 + 220, y0 + 30),
               (x0 + 230, y0 + 46)], fill=RED)


def gaza_art(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SAND, outline=INK, width=2)
    d.text((x0 + 12, y0 + 8), "CEASEFIRE LINE", font=font(SANS_B, 15),
           fill=RED)
    for i in range(8):
        sx = x0 + 14 + i * 34
        d.line([sx, y0 + 32, sx + 20, y0 + 32], fill=RED, width=3)
    d.ellipse([x0 + w - 44, y0 + 10, x0 + w - 12, y0 + 42], fill=SUN)
    base = y0 + h - 10
    for tx, tw, th in [(30, 84, 52), (130, 96, 62), (238, 70, 44)]:
        d.polygon([(x0 + tx, base), (x0 + tx + tw / 2, base - th),
                   (x0 + tx + tw, base)], fill=(200, 155, 106),
                  outline=(120, 85, 50))
        d.line([x0 + tx + tw / 2, base - th, x0 + tx + tw / 2, base],
               fill=(120, 85, 50), width=2)


def gta_art(d, x0, y0, w, h):
    bands = [(246, 160, 77), (226, 99, 94), (91, 58, 117)]
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * h / 3, x0 + w, y0 + (i + 1) * h / 3],
                    fill=col)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=2)
    # skyline
    base = y0 + h
    for bx, bh in [(150, 34), (186, 52), (226, 40), (266, 60)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 36, base],
                    fill=(42, 33, 56))
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
    # red date band
    d.rectangle([0, 88, W, 134], fill=RED)
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
    for it in items:
        d.text((24, y), "\u2022", font=font(SANS_B, 19), fill=GOLD)
        d.text((48, y), it, font=font(SANS, 19), fill=(255, 255, 255))
        y += 26

    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
    print("wrote", OUT)
