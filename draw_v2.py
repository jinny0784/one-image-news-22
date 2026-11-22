#!/usr/bin/env python3
"""Illustrated V2 front page for news-image-20261122.

Draws a 1024x1024 illustrated newspaper front page summing up the world
news of Sunday 22 November 2026: a big drawn Hormuz lead scene, then nine
region panels, each with two small drawn story scenes plus short labels.
Pure PIL, no network, deterministic output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (30, 32, 40)

FD = "/usr/share/fonts/truetype/liberation/"
SANS = "LiberationSans-Regular.ttf"
SANSB = "LiberationSans-Bold.ttf"
SERIFB_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def F(size, bold=False):
    return ImageFont.truetype(FD + (SANSB if bold else SANS), size)


def SERIF(size):
    return ImageFont.truetype(SERIFB_PATH, size)


_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def tw(text, font):
    return _probe.textlength(text, font=font)


def fit(text, maxw, size, bold=True, minsize=7):
    """Largest font (<= size) that makes text fit maxw."""
    s = size
    while s > minsize and tw(text, F(s, bold)) > maxw:
        s -= 1
    return F(s, bold)


def vgrad(w, h, top, bottom):
    """Vertical gradient image."""
    im = Image.new("RGB", (w, h))
    dr = ImageDraw.Draw(im)
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        dr.line([(0, i), (w, i)], fill=c)
    return im


def mk(w, h, color):
    im = Image.new("RGB", (w, h), color)
    return im, ImageDraw.Draw(im, "RGBA")


def flame(dr, cx, base, wdt, hgt):
    """Layered flame: red outer, orange mid, yellow core."""
    dr.polygon([(cx - wdt, base), (cx, base - hgt), (cx + wdt, base)],
               fill=(214, 48, 24))
    dr.polygon([(cx - wdt * 0.62, base), (cx, base - hgt * 0.72),
                (cx + wdt * 0.62, base)], fill=(242, 116, 26))
    dr.polygon([(cx - wdt * 0.3, base), (cx, base - hgt * 0.45),
                (cx + wdt * 0.3, base)], fill=(250, 196, 60))


def smoke(dr, cx, top, n=5, r0=10, grow=5, drift=10):
    for i in range(n):
        r = r0 + i * grow
        x = cx + (i % 2) * drift - drift // 2 + i * 3
        y = top - i * (r + 4)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(70, 66, 74, 190))


def waves(dr, x0, x1, ys, color=(120, 170, 215)):
    import random
    rnd = random.Random(42)
    for y in ys:
        x = x0
        while x < x1 - 18:
            ln = rnd.randint(10, 22)
            dr.line([(x, y), (x + ln, y)], fill=color, width=2)
            x += ln + rnd.randint(8, 20)


# ---------------------------------------------------------------- scenes
def scene_hormuz_lead(w=592, h=256):
    im = vgrad(w, h, (43, 32, 66), (233, 122, 54))
    dr = ImageDraw.Draw(im, "RGBA")
    # sun and halo
    dr.ellipse([392, 44, 488, 140], fill=(255, 170, 70, 90))
    dr.ellipse([408, 58, 472, 122], fill=(255, 199, 92))
    # mountain silhouettes closing the strait
    dr.polygon([(0, 168), (0, 62), (70, 108), (128, 140), (168, 168)],
               fill=(26, 24, 48))
    dr.polygon([(w, 168), (w, 78), (512, 116), (470, 146), (438, 168)],
               fill=(26, 24, 48))
    # sea
    dr.rectangle([0, 168, w, h], fill=(15, 43, 76))
    waves(dr, 6, w - 6, [196, 216, 236], (96, 148, 198))
    # big tanker, centre-left
    tx, ty = 96, 158
    dr.polygon([(tx, ty + 26), (tx + 16, ty + 44), (tx + 218, ty + 44),
                (tx + 236, ty + 26), (tx + 226, ty + 14), (tx + 8, ty + 14)],
               fill=(18, 18, 24))
    dr.rectangle([tx + 26, ty, tx + 150, ty + 14], fill=(120, 38, 34))
    for i, c in enumerate([(38, 84, 124), (168, 92, 30), (52, 110, 74),
                           (120, 38, 34)]):
        dr.rectangle([tx + 30 + i * 30, ty - 12, tx + 56 + i * 30, ty],
                     fill=c)
    dr.rectangle([tx + 168, ty - 16, tx + 196, ty + 14], fill=(226, 222, 210))
    dr.rectangle([tx + 174, ty - 24, tx + 190, ty - 16], fill=(226, 222, 210))
    # fire on the tanker + smoke
    flame(dr, tx + 84, ty - 10, 26, 62)
    flame(dr, tx + 122, ty - 8, 16, 40)
    smoke(dr, tx + 92, ty - 78, n=5, r0=11, grow=6, drift=12)
    # second tanker, right, small flame
    sx, sy = 428, 182
    dr.polygon([(sx, sy + 14), (sx + 10, sy + 26), (sx + 108, sy + 26),
                (sx + 118, sy + 14), (sx + 110, sy + 6), (sx + 6, sy + 6)],
               fill=(18, 18, 24))
    dr.rectangle([sx + 16, sy - 4, sx + 74, sy + 6], fill=(90, 60, 40))
    flame(dr, sx + 46, sy - 4, 11, 30)
    smoke(dr, sx + 50, sy - 36, n=3, r0=6, grow=4, drift=7)
    # drone silhouette, top right
    dx, dy = 528, 34
    dr.rectangle([dx - 9, dy - 4, dx + 9, dy + 4], fill=(16, 16, 22))
    for ox, oy in [(-16, -10), (16, -10), (-16, 10), (16, 10)]:
        dr.line([(dx, dy), (dx + ox, dy + oy)], fill=(16, 16, 22), width=2)
        dr.ellipse([dx + ox - 5, dy + oy - 2, dx + ox + 5, dy + oy + 2],
                   fill=(16, 16, 22))
    return im


def scene_tanker(w, h):
    im = vgrad(w, h, (70, 52, 92), (226, 130, 66))
    dr = ImageDraw.Draw(im, "RGBA")
    dr.ellipse([w - 52, 6, w - 20, 38], fill=(255, 199, 92))
    dr.rectangle([0, h - 22, w, h], fill=(15, 43, 76))
    tx, ty = 18, h - 40
    dr.polygon([(tx, ty + 10), (tx + 8, ty + 20), (tx + 96, ty + 20),
                (tx + 104, ty + 10), (tx + 98, ty + 2), (tx + 4, ty + 2)],
               fill=(18, 18, 24))
    dr.rectangle([tx + 12, ty - 8, tx + 62, ty + 2], fill=(140, 44, 36))
    flame(dr, tx + 38, ty - 6, 12, 30)
    smoke(dr, tx + 40, ty - 38, n=3, r0=5, grow=3, drift=6)
    return im


def scene_radar(w, h):
    im, dr = mk(w, h, (22, 30, 52))
    dr.rectangle([0, h - 12, w, h], fill=(34, 48, 38))
    cx, cy = w // 2, h - 14
    dr.polygon([(cx - 4, cy), (cx + 4, cy), (cx + 16, cy - 30),
                (cx - 16, cy - 30)], fill=(150, 158, 168))
    dr.pieslice([cx - 30, cy - 58, cx + 30, cy - 2], 180, 330,
                fill=(196, 204, 214))
    dr.line([(cx, cy - 30), (cx + 44, cy - 52)], fill=(240, 200, 90), width=3)
    for r in (14, 24, 34):
        dr.arc([cx + 30 - r, cy - 52 - r, cx + 30 + r, cy - 52 + r],
               -60, 60, fill=(90, 210, 230), width=2)
    # incoming missile streak
    dr.line([(6, 10), (52, 30)], fill=(250, 170, 60), width=3)
    dr.polygon([(52, 30), (42, 24), (46, 34)], fill=(240, 240, 240))
    return im


def scene_drone(w, h):
    im = vgrad(w, h, (96, 120, 168), (196, 214, 232))
    dr = ImageDraw.Draw(im, "RGBA")
    # city blocks along the bottom
    for i, bh in enumerate([16, 24, 13, 28, 18, 22, 14]):
        x = 4 + i * (w // 7)
        dr.rectangle([x, h - bh, x + w // 7 - 5, h], fill=(52, 58, 74))
    dx, dy = w // 2, 24
    dr.rectangle([dx - 13, dy - 5, dx + 13, dy + 5], fill=(20, 20, 28))
    for ox, oy in [(-24, -13), (24, -13), (-24, 13), (24, 13)]:
        dr.line([(dx, dy), (dx + ox, dy + oy)], fill=(20, 20, 28), width=2)
        dr.ellipse([dx + ox - 8, dy + oy - 3, dx + ox + 8, dy + oy + 3],
                   fill=(20, 20, 28))
    dr.ellipse([dx - 3, dy + 5, dx + 3, dy + 10], fill=(178, 44, 34))
    return im


def scene_bridge(w, h):
    im = vgrad(w, h, (150, 196, 226), (224, 238, 246))
    dr = ImageDraw.Draw(im, "RGBA")
    dr.ellipse([w - 44, 6, w - 16, 34], fill=(250, 205, 92))
    dr.rectangle([0, h - 20, w, h], fill=(52, 110, 158))
    waves(dr, 4, w - 4, [h - 12], (170, 205, 235))
    deck = h - 34
    dr.rectangle([4, deck, w - 4, deck + 5], fill=(70, 74, 82))
    dr.arc([10, deck - 16, w - 10, deck + 22], 180, 360, fill=(70, 74, 82),
           width=3)
    for px in (w // 4, w // 2, 3 * w // 4):
        dr.rectangle([px - 3, deck + 5, px + 3, h - 18], fill=(96, 100, 110))
    # a small truck crossing
    tx = w // 3
    dr.rectangle([tx, deck - 12, tx + 26, deck - 3], fill=(196, 60, 40))
    dr.rectangle([tx + 18, deck - 9, tx + 32, deck - 3], fill=(90, 130, 180))
    for wx in (tx + 6, tx + 24):
        dr.ellipse([wx - 4, deck - 5, wx + 4, deck + 3], fill=(24, 24, 28))
    return im


def scene_syringe(w, h):
    im, dr = mk(w, h, (233, 240, 244))
    # syringe drawn horizontally on a layer, then rotated in
    lay = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    bx, by, bl, bh = 60, h - 14, w - 30, 26
    ld.rectangle([bx, by, bx + bl, by + bh], outline=(40, 90, 130),
                 width=5, fill=(190, 220, 240, 255))
    ld.rectangle([bx + 8, by + 5, bx + bl * 0.55, by + bh - 5],
                 fill=(70, 150, 205, 255))
    for i in range(5):
        x = bx + 16 + i * 16
        ld.line([(x, by + 3), (x, by + 9)], fill=(40, 90, 130), width=2)
    ld.rectangle([bx - 16, by + 4, bx, by + bh - 4], fill=(120, 128, 138))
    ld.rectangle([bx - 26, by - 3, bx - 20, by + bh + 3], fill=(90, 96, 104))
    ld.line([(bx + bl, by + bh // 2), (bx + bl + 34, by + bh // 2)],
            fill=(90, 96, 104), width=4)
    ld.polygon([(bx + bl + 34, by + bh // 2 - 3), (bx + bl + 48, by + bh // 2),
                (bx + bl + 34, by + bh // 2 + 3)], fill=(90, 96, 104))
    lay = lay.rotate(24, resample=Image.BILINEAR, center=(w, h))
    im.paste(lay, (-w // 2, -h // 2), lay)
    # vial beside it
    vx, vy = w - 34, h - 46
    dr.rectangle([vx, vy, vx + 16, vy + 24], fill=(120, 190, 130),
                 outline=(50, 110, 60), width=2)
    dr.rectangle([vx + 2, vy - 6, vx + 14, vy], fill=(150, 154, 160))
    return im


def scene_card(w, h):
    im, dr = mk(w, h, (18, 52, 66))
    x, y, cw, ch = 14, 9, w - 28, h - 25
    dr.rounded_rectangle([x, y, x + cw, y + ch], 8, fill=(206, 164, 62))
    dr.rectangle([x, y + 9, x + cw, y + 18], fill=(52, 46, 30))
    dr.rounded_rectangle([x + 10, y + 23, x + 26, y + 35], 3,
                         fill=(240, 224, 160), outline=(120, 96, 30))
    f = fit("10%", 60, 24)
    dr.text((x + cw - 52, y + ch - 27), "10%", font=f, fill=(52, 40, 10))
    return im


def scene_quake(w, h):
    im = vgrad(w, h, (196, 178, 150), (232, 214, 178))
    dr = ImageDraw.Draw(im, "RGBA")
    gy = h - 18
    dr.rectangle([0, gy, w, h], fill=(120, 92, 64))
    crack = [(w * 0.42, gy), (w * 0.48, gy + 6), (w * 0.44, gy + 10),
             (w * 0.52, gy + 15), (w * 0.5, h)]
    dr.line(crack, fill=(30, 22, 16), width=3)
    # intact house
    hx, hy = 14, gy - 26
    dr.rectangle([hx, hy, hx + 30, gy], fill=(214, 198, 168))
    dr.polygon([(hx - 3, hy), (hx + 15, hy - 13), (hx + 33, hy)],
               fill=(150, 62, 44))
    # tilted house
    tx, ty = w - 52, gy - 22
    dr.polygon([(tx, ty + 8), (tx + 32, ty), (tx + 34, gy), (tx + 2, gy)],
               fill=(198, 178, 150))
    dr.polygon([(tx - 2, ty + 8), (tx + 14, ty - 6), (tx + 34, ty)],
               fill=(150, 62, 44))
    dr.line([(tx + 8, ty + 10), (tx + 22, gy - 4)], fill=(60, 44, 30),
            width=2)
    return im


def scene_cop(w, h):
    im, dr = mk(w, h, (16, 44, 66))
    cx, cy, r = w // 2 - 16, h // 2, min(w, h) // 2 - 8
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 180))
    dr.pieslice([cx - r, cy - r, cx + r, cy + r], 200, 300,
                fill=(84, 160, 92))
    dr.pieslice([cx - r, cy - r, cx + r, cy + r], 20, 90,
                fill=(84, 160, 92))
    dr.pieslice([cx - r, cy - r, cx + r, cy + r], 300, 350,
                fill=(84, 160, 92))
    crack = [(cx - 8, cy - r + 4), (cx + 4, cy - 14), (cx - 6, cy + 2),
             (cx + 8, cy + 18), (cx + 2, cy + r - 4)]
    dr.line(crack, fill=(20, 24, 30), width=3)
    # thermometer of bad news
    tx = cx + r + 12
    dr.rounded_rectangle([tx, 12, tx + 9, h - 18], 4, outline=(230, 230, 230),
                         width=2)
    dr.rectangle([tx + 2, h - 34, tx + 7, h - 20], fill=(214, 48, 24))
    dr.ellipse([tx - 3, h - 20, tx + 12, h - 5], fill=(214, 48, 24))
    return im


def scene_protest(w, h):
    im = vgrad(w, h, (214, 198, 170), (236, 224, 198))
    dr = ImageDraw.Draw(im, "RGBA")
    # placards
    for px, py, pw, col in [(16, 8, 34, (196, 60, 40)),
                            (66, 4, 30, (52, 110, 180)),
                            (112, 10, 36, (230, 224, 210))]:
        dr.rectangle([px + pw // 2 - 1, py + 16, px + pw // 2 + 1, h - 20],
                     fill=(110, 88, 60))
        dr.rectangle([px, py, px + pw, py + 17], fill=col)
    dr.text((120, 13), "!", font=F(13, True), fill=(178, 44, 34))
    # crowd heads
    for row, yy in enumerate([h - 26, h - 15]):
        for i in range(9):
            x = 8 + i * (w // 9) + (6 if row else 0)
            dr.ellipse([x, yy, x + 11, yy + 11], fill=(70, 58, 48))
            dr.rectangle([x - 1, yy + 10, x + 12, yy + 15], fill=(88, 74, 62))
    return im


def scene_factory(w, h):
    im = vgrad(w, h, (120, 108, 118), (188, 168, 160))
    dr = ImageDraw.Draw(im, "RGBA")
    dr.rectangle([0, h - 10, w, h], fill=(70, 62, 58))
    bx, by = 18, h - 42
    dr.rectangle([bx, by, bx + 74, h - 10], fill=(96, 92, 98))
    dr.polygon([(bx, by), (bx + 20, by - 12), (bx + 46, by), (bx + 66, by - 12),
                (bx + 74, by)], fill=(70, 66, 72))
    for i in range(4):
        dr.rectangle([bx + 8 + i * 17, by + 10, bx + 18 + i * 17, by + 20],
                     fill=(240, 200, 90))
    dr.rectangle([bx + 82, by - 26, bx + 92, h - 10], fill=(80, 76, 82))
    flame(dr, bx + 34, by - 8, 16, 34)
    flame(dr, bx + 56, by - 6, 11, 24)
    smoke(dr, bx + 88, by - 34, n=3, r0=6, grow=4, drift=6)
    return im


def scene_cricket(w, h):
    im, dr = mk(w, h, (44, 118, 62))
    dr.ellipse([8, h - 16, w - 8, h + 10], fill=(58, 138, 76))
    # stumps
    for i in range(3):
        x = w - 34 + i * 8
        dr.rectangle([x, h - 42, x + 4, h - 14], fill=(240, 214, 130))
    dr.rectangle([w - 35, h - 45, w - 12, h - 42], fill=(240, 214, 130))
    # bat, swung diagonal
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([30, 8, 44, 52], 5, fill=(226, 200, 150))
    ld.rectangle([35, 50, 40, 66], fill=(90, 60, 40))
    lay = lay.rotate(-32, resample=Image.BILINEAR, center=(40, 36))
    im.paste(lay, (0, 0), lay)
    # ball mid-flight with motion trail
    dr.line([(58, 52), (86, 44)], fill=(255, 255, 255, 160), width=2)
    dr.ellipse([88, 38, 100, 50], fill=(196, 40, 40))
    return im


def scene_boat(w, h):
    im = vgrad(w, h, (140, 178, 205), (205, 226, 238))
    dr = ImageDraw.Draw(im, "RGBA")
    sea = h - 24
    dr.rectangle([0, sea, w, h], fill=(38, 96, 148))
    waves(dr, 4, w - 4, [sea + 8, sea + 16], (170, 210, 240))
    # capsizing hull, rolled to one side
    cx, cy = w // 2, sea - 2
    dr.polygon([(cx - 52, cy - 16), (cx + 46, cy - 26), (cx + 30, cy + 2),
                (cx - 34, cy + 4)], fill=(120, 62, 34))
    dr.rectangle([cx - 30, cy - 26, cx + 8, cy - 17], fill=(226, 222, 210))
    for i in range(4):
        dr.ellipse([cx - 24 + i * 13, cy - 15, cx - 18 + i * 13, cy - 9],
                   fill=(52, 44, 38))
    dr.line([(cx + 20, cy - 24), (cx + 34, cy - 40)], fill=(80, 60, 40),
            width=3)
    return im


def scene_chart(w, h):
    im, dr = mk(w, h, (20, 22, 34))
    for gx in range(14, w, 18):
        dr.line([(gx, 6), (gx, h - 14)], fill=(44, 48, 62), width=1)
    for gy in range(8, h - 12, 14):
        dr.line([(10, gy), (w - 8, gy)], fill=(44, 48, 62), width=1)
    pts = [(12, 14), (38, 20), (58, 16), (78, 34), (98, 30), (118, 50),
           (138, 46), (w - 12, 62)]
    dr.line(pts, fill=(232, 64, 48), width=3)
    ax, ay = pts[-1]
    dr.polygon([(ax, ay), (ax - 12, ay - 3), (ax - 4, ay - 12)],
               fill=(232, 64, 48))
    f = fit("-10.4%", 66, 17)
    dr.text((w - 74, 6), "-10.4%", font=f, fill=(232, 96, 80))
    return im


def scene_mercury(w, h):
    im, dr = mk(w, h, (10, 12, 26))
    import random
    rnd = random.Random(7)
    for _ in range(26):
        x, y = rnd.randint(2, w - 3), rnd.randint(2, h - 3)
        dr.ellipse([x, y, x + 2, y + 2], fill=(220, 224, 235))
    px, py, pr = w - 52, h // 2 + 6, 30
    dr.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(178, 158, 138))
    for cx, cy, cr in [(px - 12, py - 8, 6), (px + 10, py + 10, 8),
                       (px + 4, py - 16, 4), (px - 16, py + 14, 5)]:
        dr.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(150, 130, 110))
    dr.arc([px - pr - 12, py - 14, px + pr + 12, py + 16], 20, 200,
           fill=(140, 160, 200), width=2)
    # the orbiter: bus + two blue wings
    sx, sy = 26, 22
    dr.rectangle([sx, sy, sx + 14, sy + 12], fill=(216, 200, 160))
    dr.rectangle([sx - 20, sy + 2, sx, sy + 10], fill=(52, 92, 178))
    dr.rectangle([sx + 14, sy + 2, sx + 34, sy + 10], fill=(52, 92, 178))
    dr.line([(sx + 7, sy + 12), (sx + 7, sy + 20)], fill=(216, 200, 160),
            width=2)
    dr.ellipse([sx + 3, sy + 20, sx + 11, sy + 25], fill=(216, 200, 160))
    return im


def scene_f1(w, h):
    im = vgrad(w, h, (30, 34, 58), (104, 84, 110))
    dr = ImageDraw.Draw(im, "RGBA")
    # city lights strip (Vegas at night)
    import random
    rnd = random.Random(3)
    for _ in range(30):
        x, y = rnd.randint(2, w - 3), rnd.randint(4, 22)
        dr.ellipse([x, y, x + 2, y + 2], fill=(250, 210, 110))
    dr.rectangle([0, h - 18, w, h], fill=(40, 40, 46))
    dr.line([(0, h - 18), (w, h - 18)], fill=(240, 240, 240), width=2)
    # car: low body, big rear wing, halo
    by = h - 26
    dr.polygon([(18, by), (30, by - 10), (66, by - 12), (96, by - 8),
                (128, by - 4), (140, by), (140, by + 6), (18, by + 6)],
               fill=(30, 90, 200))
    dr.polygon([(96, by - 8), (112, by - 16), (126, by - 15), (128, by - 4)],
               fill=(24, 70, 160))
    dr.rectangle([16, by - 20, 22, by - 2], fill=(20, 20, 26))
    dr.rectangle([10, by - 22, 30, by - 18], fill=(20, 20, 26))
    dr.rectangle([118, by - 6, 146, by - 2], fill=(20, 20, 26))
    dr.arc([58, by - 20, 84, by - 4], 180, 360, fill=(230, 230, 230), width=3)
    for wx in (34, 118):
        dr.ellipse([wx - 10, by - 2, wx + 10, by + 16], fill=(12, 12, 14))
        dr.ellipse([wx - 4, by + 3, wx + 4, by + 11], fill=(120, 124, 130))
    return im


def scene_tennis(w, h):
    im, dr = mk(w, h, (36, 84, 140))
    dr.rectangle([0, h - 20, w, h], fill=(44, 128, 74))
    dr.line([(0, h - 20), (w, h - 20)], fill=(240, 240, 240), width=2)
    # racket
    cx, cy = 52, 30
    dr.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=(236, 238, 240),
               width=3)
    for gx in range(cx - 14, cx + 15, 7):
        dr.line([(gx, cy - 16), (gx, cy + 16)], fill=(200, 205, 210),
                width=1)
    for gy in range(cy - 14, cy + 15, 7):
        dr.line([(cx - 17, gy), (cx + 17, gy)], fill=(200, 205, 210),
                width=1)
    dr.line([(cx + 8, cy + 16), (cx + 26, cy + 40)], fill=(120, 80, 40),
            width=5)
    # ball
    dr.ellipse([w - 44, 16, w - 28, 32], fill=(198, 224, 60))
    dr.arc([w - 46, 14, w - 26, 34], 90, 270, fill=(240, 246, 220), width=2)
    return im


def scene_phone(w, h):
    im, dr = mk(w, h, (226, 232, 238))
    x, y, pw, ph = w // 2 - 17, 6, 34, h - 12
    dr.rounded_rectangle([x, y, x + pw, y + ph], 6, fill=(28, 30, 38))
    dr.rounded_rectangle([x + 3, y + 6, x + pw - 3, y + ph - 6], 4,
                         fill=(240, 244, 248))
    dr.rounded_rectangle([x + 6, y + 12, x + 22, y + 21], 3,
                         fill=(150, 190, 235))
    dr.rounded_rectangle([x + 12, y + 25, x + 28, y + 34], 3,
                         fill=(180, 226, 180))
    f = fit("AI", 22, 13)
    dr.text((x + 9, y + 38), "AI", font=f, fill=(178, 44, 34))
    # red X badge
    bx, by = x + pw - 6, y + 2
    dr.ellipse([bx - 8, by - 2, bx + 8, by + 14], fill=(196, 44, 34))
    dr.line([(bx - 4, by + 2), (bx + 4, by + 10)], fill=(255, 255, 255),
            width=2)
    dr.line([(bx - 4, by + 10), (bx + 4, by + 2)], fill=(255, 255, 255),
            width=2)
    return im


def scene_tower(w, h):
    im = vgrad(w, h, (168, 196, 220), (224, 236, 244))
    dr = ImageDraw.Draw(im, "RGBA")
    cx = w // 2
    top, bot = 10, h - 6
    dr.line([(cx, top), (cx - 22, bot)], fill=(70, 76, 86), width=3)
    dr.line([(cx, top), (cx + 22, bot)], fill=(70, 76, 86), width=3)
    for t in (0.35, 0.6, 0.85):
        y = top + (bot - top) * t
        half = 22 * t
        dr.line([(cx - half, y), (cx + half, y)], fill=(70, 76, 86), width=2)
    dr.line([(cx - 14, top + 16), (cx + 14, top + 16)], fill=(70, 76, 86),
            width=2)
    for r in (10, 18, 26):
        dr.arc([cx - r, top - r + 8, cx + r, top + r + 8], -50, 50,
               fill=(44, 110, 180), width=2)
        dr.arc([cx - r, top - r + 8, cx + r, top + r + 8], 130, 230,
               fill=(44, 110, 180), width=2)
    # prohibition slash
    dr.ellipse([cx - 30, top - 4, cx + 30, top + 56], outline=(196, 44, 34),
               width=4)
    dr.line([(cx - 21, top + 47), (cx + 21, top + 5)], fill=(196, 44, 34),
            width=4)
    return im


# ---------------------------------------------------------------- layout
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

REGIONS = [
    dict(title="SOUTH ASIA / INDIA", color=(179, 84, 30), count=11,
         scenes=[(scene_bridge, "Modi opens six-lane Ganga bridge"),
                 (scene_syringe, "1 crore HPV vaccine doses")],
         lines=[
             "India 720/9: record Test total in New Zealand",
             "Pilgrim crash in Kota kills 9",
             "Teen 'hacks' Agniveer site with AI chatbot",
             "Akvan recovery: 2,316 babies born in shelters",
             "US court summons Doval, ex-RAW chief Goel",
             "India team in Dhaka as Ganga treaty expires",
             "Rohingya hail ICJ verdict; Myanmar rejects it",
             "Nepal PM Balendra Shah arrives in Delhi",
             "India-EU trade pact likely signed 16 Dec",
         ]),
    dict(title="MIDDLE EAST / WEST ASIA", color=(164, 22, 35), count=10,
         scenes=[(scene_radar, "IRGC claims Patriot radar hits"),
                 (scene_drone, "4th US drone downed in 24h")],
         lines=[
             "Iran vows to break blockade; power cuts start",
             "US & Israel weigh fresh strikes on Iran",
             "Saudi coalition downs 3 Houthi missiles",
             "Israeli fire kills 4 in Gaza, incl. aid staff",
             "Iran war cost to US tops $48bn - Pentagon",
             "Qatar, Centcom chiefs hold talks in Doha",
             "21 Indians evacuated from Hormuz ship",
         ]),
    dict(title="US / AMERICAS", color=(29, 79, 161), count=10,
         scenes=[(scene_card, "Trump vows 10% card-rate cap"),
                 (scene_quake, "Peru quake: 1 dead, 853 displaced")],
         lines=[
             "Democrats' Senate vote tests new majority",
             "Sinaloa: 11 dead after cartel boss captured",
             "Immigration arrests at Seattle airport",
             "Judge blocks Trump revamp of $4bn homeless aid",
             "Lawmakers push ban on Chinese AI models",
             "Brazil storm kills 3, wrecks 8,000 homes",
             "Trump names Vance, Rubio as 2028 successors",
             "Air travel back to normal by Monday",
         ]),
    dict(title="EUROPE", color=(14, 124, 134), count=10,
         scenes=[(scene_cop, "COP31 collapses: no deal"),
                 (scene_protest, "France: 6th protest weekend")],
         lines=[
             "Guterres 'deeply disappointed' by failure",
             "NATO vows to defend 'every inch' of Poland",
             "Le Pen hails 'historic victory' in Senate",
             "Six EU states demand farm cuts for defence",
             "EU proposes Big Tech tax for next budget",
             "Belgium faces air-traffic shutdown Monday",
             "Estonia proposes closing border with Russia",
             "Russian strike near Kyiv kills 2, wounds 4",
         ]),
    dict(title="EAST ASIA", color=(194, 24, 91), count=6,
         scenes=[(scene_phone, "S. Korea edu chief quits in AI row"),
                 (scene_tower, "China warns US over FCC ban")],
         lines=[
             "India-Japan expand defence partnership",
             "India-China commanders conclude border talks",
             "$75,000 reward for exam-cheating tips in S. Korea",
             "UK swimmer crosses Hormuz for environment",
         ]),
    dict(title="SOUTHEAST ASIA & PACIFIC", color=(46, 125, 50), count=5,
         scenes=[(scene_factory, "Indonesia fire: 3 dead, 36 missing"),
                 (scene_cricket, "Australia edge England in T20")],
         lines=[
             "Malaysia to resettle 10,000 Rohingya",
             "Cummins keeps Cricket Australia's support",
             "Record 188 chase won with one ball to spare",
         ]),
    dict(title="AFRICA", color=(141, 90, 43), count=4,
         scenes=[(scene_boat, "Nigeria boat capsizes: 24 dead"),
                 (scene_drone, "Sudan downs drones over Khartoum")],
         lines=[
             "Congo politician killed over Ebola measures",
             "Ethiopia faces return to war as fighting spreads",
         ]),
    dict(title="BUSINESS / TECH / SCIENCE", color=(94, 53, 177), count=9,
         scenes=[(scene_chart, "Nasdaq worst week since 2020"),
                 (scene_mercury, "BepiColombo reaches Mercury")],
         lines=[
             "Nvidia -14% on reports of SEC probe",
             "Anthropic -8.5% a day after IPO debut",
             "Bitcoin hits 2-year low, rebounds to $60,000",
             "Bayer $7.25bn Roundup settlement approved",
             "US bars AI-chip centres serving China, Iran",
             "India's NSE enters world's top five markets",
             "Musk warns AI cash crunch may hit in 2027",
         ]),
    dict(title="SPORT / CULTURE", color=(20, 102, 60), count=9,
         scenes=[(scene_f1, "Verstappen wins Las Vegas GP"),
                 (scene_tennis, "Alcaraz v Zverev tonight")],
         lines=[
             "India declare 720/9 - record total in NZ",
             "England beat NZ 37-12 in rugby, record margin",
             "France beat Argentina 45-17, reach final",
             "Leeds beat Chelsea 4-1 at Stamford Bridge",
             "Man Utd appoint Pochettino as head coach",
             "Kansas City Current win first NWSL title",
             "GTA VI festival weekend lights up Miami",
         ]),
]


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def caption(sx, sy, sw, sh, text):
    d.rectangle([sx, sy + sh - 15, sx + sw, sy + sh], fill=(8, 8, 12, 178))
    cf = fit(text, sw - 8, 10)
    d.text((sx + 4, sy + sh - 12), text, font=cf, fill=(255, 255, 255))


def panel(x, y, w, h, reg):
    d.rectangle([x, y, x + w, y + h], fill=(252, 250, 244),
                outline=(188, 180, 160))
    d.rectangle([x, y, x + w, y + 24], fill=reg["color"])
    tf = fit(reg["title"], w - 54, 14)
    d.text((x + 8, y + 5), reg["title"], font=tf, fill=(255, 255, 255))
    cnt = str(reg["count"])
    cf = F(12, True)
    d.text((x + w - 10 - tw(cnt, cf), y + 6), cnt, font=cf,
           fill=(255, 255, 255))
    n = len(reg["lines"])
    sh = 66 if n >= 7 else min(118, 66 + (7 - n) * 13)
    sw = (w - 10) // 2
    for i, (fn, cap) in enumerate(reg["scenes"]):
        sx = x + 3 + i * (sw + 4)
        img.paste(fn(sw, sh), (sx, y + 27))
        caption(sx, y + 27, sw, sh, cap)
    ty = y + 31 + sh + 4
    size, lh = (12, 14) if n <= 8 else (11, 13)
    for i, line in enumerate(reg["lines"]):
        ly = ty + i * lh
        d.ellipse([x + 7, ly + 5, x + 11, ly + 9], fill=(178, 44, 34))
        lf = fit(line, w - 26, size, bold=False, minsize=9)
        d.text((x + 16, ly), line, font=lf, fill=INK)


def masthead():
    d.rectangle([0, 0, W, 58], fill=(13, 34, 64))
    d.rectangle([0, 58, W, 61], fill=(240, 196, 84))
    d.text((14, 13), "THE WORLD IN ONE DAY", font=SERIF(29),
           fill=(255, 255, 255))
    date = "SUNDAY 22 NOVEMBER 2026"
    df = F(20, True)
    d.text((W - 14 - tw(date, df), 7), date, font=df, fill=(240, 196, 84))
    tag = "74 STORIES · 9 REGIONS · ONE DAY"
    gf = F(11, True)
    d.text((W - 14 - tw(tag, gf), 35), tag, font=gf, fill=(198, 210, 226))


def lead():
    img.paste(scene_hormuz_lead(592, 256), (8, 66))
    d.rectangle([8, 66, 600, 322], outline=(120, 110, 96))
    x = 612
    maxw = W - x - 10
    d.text((x, 68), "LEAD · STRAIT OF HORMUZ", font=F(15, True),
           fill=(178, 35, 27))
    hf = SERIF(56)
    while tw("GULF ON FIRE", hf) > maxw and hf.size > 20:
        hf = SERIF(hf.size - 2)
    d.text((x, 90), "GULF ON FIRE", font=hf, fill=(178, 35, 27))
    cy = 96 + hf.size + 8
    for sub in ("Three tankers hit, Bahrain facility struck",
                "Iran vows to break the US blockade"):
        for ln in wrap(sub, F(17, True), maxw):
            d.text((x, cy), ln, font=F(17, True), fill=INK)
            cy += 21
        cy += 3
    cy += 4
    for b in ("4th US drone downed in 24 hours",
              "~25 tankers hit in the past week",
              "Bahrain strike injures 2; Saudis condemn",
              "Shipping through the strait down ~65%"):
        d.ellipse([x + 1, cy + 6, x + 5, cy + 10], fill=(178, 35, 27))
        bf = fit(b, maxw - 14, 13, bold=False, minsize=10)
        d.text((x + 12, cy), b, font=bf, fill=(52, 54, 62))
        cy += 19


def main():
    masthead()
    lead()
    d.line([(8, 330), (W - 8, 330)], fill=(150, 140, 120), width=2)
    cols = [8, 348, 688]
    rows = [334, 562, 790]
    for i, reg in enumerate(REGIONS):
        panel(cols[i % 3], rows[i // 3], 328, 222, reg)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    if size > 1_000_000:
        img.quantize(colors=256).save(out, optimize=True)
        size = os.path.getsize(out)
    total = sum(r["count"] for r in REGIONS)
    print(f"wrote {out}: {size} bytes, {total} stories, "
          f"{len(REGIONS)} regions")


if __name__ == "__main__":
    main()
