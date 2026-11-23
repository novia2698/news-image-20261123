#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261123 entry.

Renders entry.png: a one-page newspaper front page that sums up the
world news of Monday 23 November 2026 in six illustrated stories plus an
"also today" ticker. Run once on the builder machine (Pillow is fine here);
the shipped main.py is stdlib-only and only copies the finished PNG.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1920, 1200
PAPER = (248, 245, 238)
INK = (16, 28, 46)
NAVY = (16, 28, 46)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
GREY = (90, 96, 104)
CARD_LINE = (205, 200, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_ship(d, x, y, w, h):
    """Cargo ship on waves, smoke and flames above the deck."""
    sea_y = y + int(h * 0.72)
    # sky smoke
    for cx, cy, r in ((x + w * 0.30, y + h * 0.16, 26),
                      (x + w * 0.42, y + h * 0.10, 32),
                      (x + w * 0.55, y + h * 0.15, 24)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 122, 126))
    # flames
    flame = [(x + w * 0.30, y + h * 0.42), (x + w * 0.36, y + h * 0.22),
             (x + w * 0.42, y + h * 0.42), (x + w * 0.48, y + h * 0.26),
             (x + w * 0.54, y + h * 0.42)]
    d.polygon(flame, fill=(230, 110, 20))
    d.polygon([(x + w * 0.36, y + h * 0.42), (x + w * 0.40, y + h * 0.30),
               (x + w * 0.45, y + h * 0.42)], fill=(245, 190, 40))
    # containers
    d.rectangle([x + w * 0.24, y + h * 0.42, x + w * 0.40, y + h * 0.56],
                fill=(178, 34, 34))
    d.rectangle([x + w * 0.42, y + h * 0.42, x + w * 0.58, y + h * 0.56],
                fill=(31, 78, 121))
    d.rectangle([x + w * 0.60, y + h * 0.42, x + w * 0.72, y + h * 0.56],
                fill=(30, 107, 74))
    # hull
    d.polygon([(x + w * 0.14, y + h * 0.56), (x + w * 0.86, y + h * 0.56),
               (x + w * 0.78, sea_y + 14), (x + w * 0.22, sea_y + 14)],
              fill=(16, 28, 46))
    d.rectangle([x + w * 0.14, y + h * 0.56, x + w * 0.86, y + h * 0.60],
                fill=(178, 34, 34))
    # waves
    for i in range(5):
        wx = x + w * (0.08 + 0.18 * i)
        d.arc([wx, sea_y + 4, wx + 90, sea_y + 34], 0, 180,
              fill=(31, 78, 121), width=6)
    d.rectangle([x, sea_y + 26, x + w, y + h], fill=(31, 78, 121))


def draw_drone_strike(d, x, y, w, h):
    """Apartment block with a drone above and an explosion flash."""
    bx, by = x + w * 0.18, y + h * 0.30
    bw, bh = w * 0.44, h * 0.62
    d.rectangle([bx, by, bx + bw, by + bh], fill=(70, 76, 84))
    d.rectangle([bx, by, bx + bw, by + 14], fill=(52, 56, 62))
    for r in range(4):
        for c in range(3):
            wx = bx + 16 + c * (bw - 32) / 2
            wy = by + 26 + r * (bh - 40) / 3
            lit = (r == 1 and c == 1)
            d.rectangle([wx, wy, wx + 26, wy + 20],
                        fill=(245, 190, 40) if lit else (210, 214, 218))
    # explosion star on the roof corner
    ex, ey = bx + bw - 6, by - 6
    pts = []
    for i in range(12):
        ang = math.pi * i / 6
        rr = 42 if i % 2 == 0 else 18
        pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
    d.polygon(pts, fill=(245, 170, 30))
    d.polygon([(ex, ey - 14), (ex + 10, ey + 8), (ex - 10, ey + 8)],
              fill=(230, 110, 20))
    # drone top-right
    dx, dy = x + w * 0.72, y + h * 0.22
    d.ellipse([dx - 12, dy - 12, dx + 12, dy + 12], fill=(16, 28, 46))
    for sx, sy in ((-30, -18), (30, -18), (-30, 18), (30, 18)):
        d.line([dx, dy, dx + sx, dy + sy], fill=(16, 28, 46), width=4)
        d.ellipse([dx + sx - 14, dy + sy - 4, dx + sx + 14, dy + sy + 4],
                  outline=(16, 28, 46), width=3)
    d.line([dx, dy + 14, dx, dy + 44], fill=(16, 28, 46), width=3)


def draw_globe(d, x, y, w, h):
    """Globe with a rising thermometer: the planet heating up."""
    cx, cy, r = x + w * 0.40, y + h * 0.52, int(h * 0.36)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(31, 110, 140))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(16, 28, 46), width=4)
    for k in (-0.55, 0.0, 0.55):
        d.arc([cx - r + 26, cy - r, cx + r - 26, cy + r],
              90 + k * 90, 270 + k * 90, fill=(255, 255, 255), width=3)
    d.ellipse([cx - r * 0.55, cy - r * 0.62, cx - r * 0.10, cy - r * 0.18],
              fill=(30, 107, 74))
    d.ellipse([cx + r * 0.05, cy + r * 0.10, cx + r * 0.60, cy + r * 0.55],
              fill=(30, 107, 74))
    # thermometer
    tx = x + w * 0.82
    d.rounded_rectangle([tx - 12, y + h * 0.12, tx + 12, y + h * 0.78],
                        radius=12, fill=(255, 255, 255),
                        outline=(16, 28, 46), width=3)
    d.ellipse([tx - 24, y + h * 0.72, tx + 24, y + h * 0.94],
              fill=(255, 255, 255), outline=(16, 28, 46), width=3)
    d.rounded_rectangle([tx - 7, y + h * 0.34, tx + 7, y + h * 0.76],
                        radius=7, fill=(220, 60, 40))
    d.ellipse([tx - 16, y + h * 0.74, tx + 16, y + h * 0.90],
              fill=(220, 60, 40))
    for i, frac in enumerate((0.20, 0.40, 0.60)):
        ty = y + h * frac
        d.line([tx + 12, ty, tx + 24, ty], fill=(16, 28, 46), width=3)


def draw_scales(d, x, y, w, h):
    """Scales of justice."""
    cx = x + w * 0.50
    top = y + h * 0.12
    d.line([cx, top, cx, y + h * 0.82], fill=(16, 28, 46), width=8)
    d.ellipse([cx - 12, top - 12, cx + 12, top + 12], fill=(178, 150, 40))
    d.line([x + w * 0.16, top + 18, x + w * 0.84, top + 18],
           fill=(16, 28, 46), width=7)
    for side in (-1, 1):
        px = cx + side * w * 0.34
        py = top + 18
        d.polygon([(px - 8, py), (px + 8, py), (px, py + 52)],
                  outline=(16, 28, 46), width=3)
        d.line([px - 8, py, px - 58, py + 52], fill=(16, 28, 46), width=3)
        d.line([px + 8, py, px + 58, py + 52], fill=(16, 28, 46), width=3)
        d.arc([px - 58, py + 40, px + 58, py + 96], 0, 180,
              fill=(178, 150, 40), width=7)
    d.rectangle([cx - 70, y + h * 0.82, cx + 70, y + h * 0.90],
                fill=(16, 28, 46))
    d.rectangle([cx - 90, y + h * 0.90, cx + 90, y + h * 0.95],
                fill=(178, 150, 40))


def draw_factory(d, x, y, w, h):
    """Factory with sawtooth roof, chimney smoke and flames."""
    fx, fy = x + w * 0.16, y + h * 0.42
    fw, fh = w * 0.56, h * 0.48
    # chimney
    chx = fx + fw * 0.72
    d.rectangle([chx, y + h * 0.10, chx + 34, fy + fh], fill=(90, 96, 104))
    for cx, cy, r in ((chx + 8, y + h * 0.06, 18), (chx + 26, y - 2, 22),
                      (chx - 6, y + h * 0.02, 14)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 152, 156))
    # sawtooth roof + body
    d.polygon([(fx, fy + 40), (fx + fw * 0.25, fy), (fx + fw * 0.25, fy + 40),
               (fx + fw * 0.50, fy), (fx + fw * 0.50, fy + 40),
               (fx + fw * 0.75, fy), (fx + fw * 0.75, fy + 40),
               (fx + fw, fy + 40), (fx + fw, fy + fh), (fx, fy + fh)],
              fill=(52, 56, 62))
    for i in range(3):
        wx = fx + 18 + i * 52
        d.rectangle([wx, fy + 62, wx + 30, fy + 96], fill=(245, 190, 40))
    # flames at the door
    d.polygon([(fx + fw * 0.55, fy + fh), (fx + fw * 0.62, fy + fh - 56),
               (fx + fw * 0.70, fy + fh), (fx + fw * 0.78, fy + fh - 44),
               (fx + fw * 0.86, fy + fh)], fill=(230, 110, 20))
    d.line([fx, fy + fh, fx + fw, fy + fh], fill=(16, 28, 46), width=4)


def draw_gradcap(d, x, y, w, h):
    """Graduation cap above a microchip: AI in the exam hall."""
    cx, cy = x + w * 0.50, y + h * 0.40
    # cap board (diamond) and skull cap
    d.polygon([(cx - 118, cy), (cx, cy - 50), (cx + 118, cy), (cx, cy + 50)],
              fill=(16, 28, 46))
    d.polygon([(cx - 62, cy + 14), (cx + 62, cy + 14), (cx + 62, cy + 62),
               (cx, cy + 82), (cx - 62, cy + 62)], fill=(30, 44, 66))
    # tassel
    d.line([cx + 118, cy, cx + 118, cy + 78], fill=(245, 190, 40), width=5)
    d.polygon([(cx + 108, cy + 78), (cx + 128, cy + 78), (cx + 118, cy + 104)],
              fill=(245, 190, 40))
    # chip below
    chx, chy = cx - 46, y + h * 0.68
    d.rounded_rectangle([chx, chy, chx + 92, chy + 48], radius=8,
                        fill=(91, 45, 142))
    for i in range(4):
        px = chx + 14 + i * 21
        d.line([px, chy - 8, px, chy], fill=(16, 28, 46), width=4)
        d.line([px, chy + 48, px, chy + 56], fill=(16, 28, 46), width=4)
    d.text((cx, chy + 24), "AI", font=font(SANS_B, 30), fill=WHITE,
           anchor="mm")


STORIES = [
    dict(tag="UKRAINE  ·  BALTIC SEA", accent=(31, 78, 121),
         tint=(214, 228, 240), draw=draw_ship,
         headline="Cargo ship ablaze off Finland",
         body="A Russian cargo ship is still burning after a drone attack "
              "in the Baltic — the war spilling north."),
    dict(tag="UKRAINE  ·  KYIV REGION", accent=(139, 30, 30),
         tint=(242, 220, 218), draw=draw_drone_strike,
         headline="14 missing after drone hits homes",
         body="A Russian drone struck a home in the Kyiv region; at least "
              "14 people are missing, Zelenskiy says."),
    dict(tag="CLIMATE  ·  COP31", accent=(30, 107, 74),
         tint=(214, 236, 224), draw=draw_globe,
         headline="Climate talks end with no fossil-fuel deal",
         body="COP31 in Türkiye collapses: the final draft drops the words "
              "“fossil fuels”."),
    dict(tag="JUSTICE  ·  THE HAGUE", accent=(138, 109, 27),
         tint=(244, 236, 205), draw=draw_scales,
         headline="Myanmar guilty of Rohingya genocide",
         body="The UN’s top court rules Myanmar committed genocide against "
              "the Rohingya."),
    dict(tag="INDONESIA", accent=(179, 71, 0),
         tint=(248, 226, 205), draw=draw_factory,
         headline="Factory fire: dozens missing",
         body="Seven bodies recovered and 50 people missing after a blaze "
              "tears through a factory."),
    dict(tag="SOUTH KOREA", accent=(91, 45, 142),
         tint=(232, 220, 244), draw=draw_gradcap,
         headline="Minister quits over AI exam-cheating scandal",
         body="The education minister resigns after anti-AI cheating "
              "measures throw the exam into chaos."),
]

TICKER = ("ALSO TODAY  —  Mexico captures cartel boss “El Chapo Isidro”  ·  "
          "Lisbon marches over living costs  ·  Nepal PM meets Modi in Delhi  ·  "
          "India 720/9 in Wellington Test")


def draw_card(d, story, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=WHITE,
                        outline=CARD_LINE, width=2)
    # illustration panel
    panel_h = 170
    d.rounded_rectangle([x + 2, y + 2, x + w - 2, y + panel_h], radius=10,
                        fill=story["tint"])
    d.rectangle([x + 2, y + panel_h - 40, x + w - 2, y + panel_h],
                fill=story["tint"])
    story["draw"](d, x + 14, y + 8, w - 28, panel_h - 8)
    # accent bar under the panel
    d.rectangle([x + 2, y + panel_h, x + w - 2, y + panel_h + 6],
                fill=story["accent"])
    tx = x + 26
    ty = y + panel_h + 22
    d.text((tx, ty), story["tag"], font=font(SANS_B, 23),
           fill=story["accent"])
    ty += 36
    for line in wrap(d, story["headline"], font(SANS_B, 34), w - 52):
        d.text((tx, ty), line, font=font(SANS_B, 34), fill=INK)
        ty += 40
    ty += 4
    for line in wrap(d, story["body"], font(SANS, 23), w - 52):
        d.text((tx, ty), line, font=font(SANS, 23), fill=(52, 58, 66))
        ty += 30


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.text((W // 2, 30), "THE WORLD IN ONE IMAGE",
           font=font(SERIF_B, 82), fill=WHITE, anchor="ma")
    d.text((W // 2, 122), "MONDAY  ·  23 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=(245, 190, 40), anchor="ma")
    d.rectangle([0, 168, W, 176], fill=RED)
    # standfirst
    d.text((W // 2, 196),
           "War at sea and in the air — climate talks collapse — justice for "
           "the Rohingya — fire in Indonesia — AI cheats the exam",
           font=font(SERIF_I, 30), fill=INK, anchor="ma")
    # story grid
    gx, gy, cw, chh, gap = 48, 240, 592, 412, 20
    for i, story in enumerate(STORIES):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (chh + gap)
        draw_card(d, story, cx, cy, cw, chh)
    # ticker (shrink to fit the full width)
    size = 22
    while size > 15:
        tf = font(SANS_B, size)
        if d.textlength(TICKER, font=tf) <= W - 60:
            break
        size -= 1
    d.rectangle([0, 1096, W, 1150], fill=NAVY)
    d.text((W // 2, 1112), TICKER, font=tf, fill=WHITE, anchor="ma")
    # footer
    d.text((W // 2, 1162),
           "Six stories, one day — Monday 23 November 2026  ·  Sources: "
           "Reuters · BBC · AP  ·  Rendered by an AI agent for make.fun",
           font=font(SANS, 22), fill=GREY, anchor="ma")
    img.save(OUT)
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
