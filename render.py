#!/usr/bin/env python3
"""Render Thursday 19 November 2026 world news as a 1024x1024 PNG front page.

Drawn entirely with Pillow shapes and DejaVu fonts; no network, no photos.
Run: python3 render.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font("DejaVuSans-Bold.ttf", 62)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_TAG = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 16)

NAVY = (15, 42, 74)
NAVY_LIGHT = (24, 62, 102)
INK = (20, 24, 30)
GREY = (70, 78, 88)
BG = (255, 255, 255)
BLOCK_BG = (244, 246, 248)
BLOCK_LINE = (205, 212, 220)
GOLD = (212, 175, 55)

# (tag, tag colour, headline, summary)
STORIES = [
    ("DIPLOMACY", (27, 94, 143),
     "Trump, Xi and Putin meet in Shenzhen",
     "First trilateral summit, on the APEC sidelines, puts nuclear arms control in focus."),
    ("JUSTICE", (122, 63, 140),
     "ICJ rules on Rohingya genocide case",
     "Judges decide whether Myanmar committed genocide in its 2017 crackdown; Gambia brought the case in 2019."),
    ("CONFLICT", (178, 58, 48),
     "Iran strikes US bases in the Gulf",
     "Drones targeted US sites in Kuwait and Bahrain after US jets hit a missile site on Qeshm Island; defences said they intercepted them."),
    ("WAR", (120, 72, 20),
     "Israeli tanks cross Gaza's Yellow Line",
     "First ground operation beyond the line since the October 2025 ceasefire; raid near Nuseirat aimed to destroy a tunnel."),
    ("CLIMATE", (34, 120, 72),
     "COP31 talks deadlocked in Antalya",
     "Final days of the summit with 21 issues unresolved; new draft texts due Thursday before it closes Friday."),
    ("MARKETS", (13, 110, 110),
     "Anthropic IPO is the biggest ever",
     "Priced at $83 a share, raising $81.3 billion; shares start trading on Nasdaq as ANT on Thursday."),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with textlength; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, idx, cx, cy, colour):
    """Simple abstract pictogram centred at (cx, cy), ~84px across."""
    r = 42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 240, 245),
                 outline=colour, width=3)
    if idx == 0:  # three leaders: three circles + table line
        for dx in (-24, 0, 24):
            draw.ellipse([cx + dx - 11, cy - 22, cx + dx + 11, cy], fill=colour)
        draw.rectangle([cx - 34, cy + 8, cx + 34, cy + 14], fill=colour)
    elif idx == 1:  # scales of justice
        draw.line([cx, cy - 26, cx, cy + 26], fill=colour, width=4)
        draw.line([cx - 28, cy - 18, cx + 28, cy - 18], fill=colour, width=4)
        draw.polygon([(cx - 34, cy - 2), (cx - 14, cy - 2), (cx - 24, cy - 18)], fill=colour)
        draw.polygon([(cx + 14, cy - 2), (cx + 34, cy - 2), (cx + 24, cy - 18)], fill=colour)
        draw.rectangle([cx - 16, cy + 22, cx + 16, cy + 27], fill=colour)
    elif idx == 2:  # drone: body + four rotors
        draw.rectangle([cx - 18, cy - 8, cx + 18, cy + 8], fill=colour)
        for dx, dy in ((-28, -20), (28, -20), (-28, 20), (28, 20)):
            draw.ellipse([cx + dx - 8, cy + dy - 8, cx + dx + 8, cy + dy + 8],
                         outline=colour, width=3)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    elif idx == 3:  # tank + dashed line
        draw.rectangle([cx - 30, cy + 2, cx + 30, cy + 18], fill=colour)
        draw.ellipse([cx - 8, cy - 14, cx + 12, cy + 6], fill=colour)
        draw.line([cx + 10, cy - 6, cx + 34, cy - 6], fill=colour, width=4)
        for i in range(5):
            x0 = cx - 34 + i * 15
            draw.line([x0, cy + 26, x0 + 8, cy + 26], fill=(178, 58, 48), width=3)
    elif idx == 4:  # globe with leaf
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=colour, width=4)
        draw.line([cx - 24, cy, cx + 24, cy], fill=colour, width=3)
        draw.line([cx, cy - 24, cx, cy + 24], fill=colour, width=2)
        draw.polygon([(cx + 10, cy + 30), (cx + 34, cy + 12), (cx + 34, cy + 30)], fill=colour)
    else:  # rising bars + arrow
        for i, hgt in enumerate((14, 24, 34)):
            x0 = cx - 30 + i * 20
            draw.rectangle([x0, cy + 22 - hgt, x0 + 13, cy + 22], fill=colour)
        draw.line([cx - 32, cy - 22, cx - 6, cy - 2, cx + 8, cy - 12, cx + 32, cy - 28],
                  fill=(178, 58, 48), width=4)
        draw.polygon([(cx + 32, cy - 28), (cx + 20, cy - 28), (cx + 32, cy - 16)], fill=(178, 58, 48))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 8), title, font=F_TITLE, fill=(255, 255, 255))
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 78), date, font=F_DATE, fill=(212, 175, 55))

    # --- Story grid: 2 columns x 3 rows ---
    margin, gap = 16, 14
    col_w = (W - 2 * margin - gap) // 2
    row_h = 268
    top = 140
    foot_y = top + 3 * row_h + 2 * gap + 12

    for i, (tag, colour, head, summ) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (col_w + gap)
        y0 = top + row * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=10,
                            fill=BLOCK_BG, outline=BLOCK_LINE, width=2)

        # pictogram, top-left
        ix, iy = x0 + 62, y0 + 62
        draw_icon(d, i, ix, iy, colour)

        # tag pill, top-right of icon row
        tx = x0 + 122
        ty = y0 + 22
        tag_w = d.textlength(tag, font=F_TAG) + 20
        d.rounded_rectangle([tx, ty, tx + tag_w, ty + 30], radius=15, fill=colour)
        d.text((tx + 10, ty + 5), tag, font=F_TAG, fill=(255, 255, 255))

        # headline, right of icon, wraps to at most 2 lines
        hx = x0 + 122
        hw = x1 - hx - 14
        lines = wrap(d, head, F_HEAD, hw)
        assert len(lines) <= 2, f"headline too long: {head!r} -> {lines}"
        hy = ty + 40
        for ln in lines:
            d.text((hx, hy), ln, font=F_HEAD, fill=INK)
            hy += 32

        # divider, then summary, full width below icon row
        d.line([x0 + 16, y0 + 128, x1 - 16, y0 + 128], fill=BLOCK_LINE, width=2)
        sx = x0 + 16
        sw = x1 - sx - 16
        slines = wrap(d, summ, F_BODY, sw)
        assert len(slines) <= 4, f"summary too long: {summ!r}"
        sy = y0 + 144
        for ln in slines:
            d.text((sx, sy), ln, font=F_BODY, fill=GREY)
            sy += 29
        assert sy <= y1 - 6, f"block {i} overflows"

    # --- Footer ---
    foot = "Sources: wire reports, 19 November 2026"
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, foot_y), foot, font=F_FOOT, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"saved {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
