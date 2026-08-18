# NOTE: unlike most generate_dayNN_images.py scripts in this series, this file does
# NOT (yet) cover every image in the folder. day17-01/02/03/05 have no known source
# and were left as-is (raster only). This script currently only defines the function
# that produces day17-04-new-requirements.png, rebuilt from scratch by sampling the
# original PNG's colors/layout after the source design file could not be found, to
# fix a mismatch between the image (4 boxes) and its own title/alt text (six items).
# Add functions for the other four images here if their sources ever turn up, and
# call them from main() the same way the other Day folders do.

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
ROOT = Path(__file__).parent
FONT_REGULAR = Path(r"C:\Windows\Fonts\msjh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msjhbd.ttc")

NAVY_BG = (11, 18, 32)
BOX_FILL = (17, 28, 51)
WHITE = (248, 250, 252)
DESC = (203, 213, 225)
UNDERLINE = (30, 41, 59)
CIRCLE_TR = (12, 74, 110)
CIRCLE_BL = (49, 46, 129)

BLUE = (37, 99, 235)
VIOLET = (124, 58, 237)
ORANGE = (249, 115, 22)
GREEN = (22, 163, 74)
RED = (220, 38, 38)
TEAL = (13, 148, 136)


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded(draw, box, fill=None, outline=None, width=1, radius=20):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, fill, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def wrap(draw, value, size, bold, max_width):
    f = font(size, bold)
    lines = []
    cur = ""
    for ch in value:
        trial = cur + ch
        if draw.textlength(trial, font=f) > max_width and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def new_requirements():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY_BG)
    d = ImageDraw.Draw(im)

    d.ellipse((930, -220, 1490, 340), fill=CIRCLE_TR)
    d.ellipse((-240, 500, 320, 1060), fill=CIRCLE_BL)

    d.text((73, 46), "四種頻率、三種格式，六項未定案的技術決策", font=font(40, True), fill=WHITE)
    d.line((73, 122, 1207, 122), fill=UNDERLINE, width=2)

    items = [
        ("1", BLUE, "四種頻率", "日、週、雙週、月，客戶自選"),
        ("2", VIOLET, "三種格式", "PDF、Word、Excel"),
        ("3", ORANGE, "提前一小時", "發送前一小時開始製作"),
        ("4", GREEN, "數值計算範圍", "週期報表的成長率怎麼算未定"),
        ("5", RED, "排程觸發邏輯", "依頻率與提前量重新計算觸發時機"),
        ("6", TEAL, "格式輸出解耦", "PDF 產製邏輯要跟輸出格式拆開"),
    ]

    bw, bh = 350, 230
    gap_x, gap_y = 42, 35
    left = 73
    row_ys = [183, 183 + bh + gap_y]
    col_xs = [left, left + bw + gap_x, left + 2 * (bw + gap_x)]

    badge_pad = 28
    badge_h = 58

    for idx, (num, color, heading, desc) in enumerate(items):
        row = idx // 3
        col = idx % 3
        bx = col_xs[col]
        by = row_ys[row]

        rounded(d, (bx, by, bx + bw, by + bh), fill=BOX_FILL, outline=color, width=3, radius=22)

        badge_x0 = bx + badge_pad
        badge_x1 = bx + bw - badge_pad
        badge_y0 = by + 27
        badge_y1 = badge_y0 + badge_h
        rounded(d, (badge_x0, badge_y0, badge_x1, badge_y1), fill=color, radius=18)
        text(d, ((badge_x0 + badge_x1) / 2, (badge_y0 + badge_y1) / 2), num, 26, WHITE, True, anchor="mm")

        heading_y = badge_y1 + 22
        text(d, (bx + badge_pad, heading_y), heading, 27, WHITE, True)

        desc_y = heading_y + 46
        max_w = bw - 2 * badge_pad
        for line in wrap(d, desc, 20, False, max_w):
            text(d, (bx + badge_pad, desc_y), line, 20, DESC, False)
            desc_y += 28

    im.save(ROOT / "day17-04-new-requirements.png", format="PNG", optimize=True)


if __name__ == "__main__":
    new_requirements()
