from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1280, 720
ROOT = Path(__file__).parent
FONT_REGULAR = Path(r"C:\Windows\Fonts\msjh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msjhbd.ttc")

NAVY = "#071426"
SLATE = "#334155"
MUTED = "#64748B"
PALE = "#F1F5F9"
WHITE = "#F8FAFC"
CYAN = "#22D3EE"
TEAL = "#0E7490"
BLUE = "#2563EB"
ORANGE = "#F97316"
GREEN = "#16A34A"
RED = "#DC2626"
PURPLE = "#7C3AED"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded(draw, box, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, fill, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def arrow(draw, start, end, color=CYAN, width=7):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    draw.polygon([(ex, ey), (ex - 18, ey - 12), (ex - 18, ey + 12)], fill=color)


def save(image, name):
    image.save(ROOT / name, format="PNG", optimize=True)


def cover():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.ellipse((1010, -160, 1390, 220), fill="#0C4A6E")
    draw.ellipse((-170, 520, 190, 880), fill="#312E81")
    text(draw, (70, 70), "DAY 08 · SPRING CRON", 34, CYAN, True)
    text(draw, (70, 165), "每天九點，", 66, WHITE, True)
    text(draw, (70, 250), "是哪個九點？", 66, WHITE, True)
    text(draw, (70, 342), "ChatGPT 出反例 × Java 計算 × JUnit 驗證", 31, "#CBD5E1")

    cards = [("式", "六欄 cron", BLUE), ("區", "時區換算", ORANGE), ("驗", "下一時刻", GREEN)]
    x = 70
    for tag, note, color in cards:
        rounded(draw, (x, 480, x + 340, 625), WHITE, 24)
        draw.ellipse((x + 24, 515, x + 88, 579), fill=color)
        text(draw, (x + 56, 547), tag, 28, WHITE, True, "mm")
        text(draw, (x + 118, 547), note, 27, NAVY, True, "lm")
        x += 405
    save(image, "day08-01-cover.png")


def learning_loop():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "導師不先公布答案", 47, NAVY, True)
    text(draw, (64, 108), "我先預測，ChatGPT 專門挑戰前提", 27, MUTED)
    steps = [
        ("1", "我先填表", "cron · 時區 · 時刻", BLUE),
        ("2", "ChatGPT 提反例", "換格式 · 換時區", ORANGE),
        ("3", "程式做裁判", "Java · JUnit · 文件", GREEN),
    ]
    for index, (number, title, note, color) in enumerate(steps):
        x = 70 + index * 405
        rounded(draw, (x, 220, x + 330, 500), WHITE, 24, color, 4)
        draw.ellipse((x + 128, 252, x + 202, 326), fill=color)
        text(draw, (x + 165, 290), number, 30, WHITE, True, "mm")
        text(draw, (x + 165, 385), title, 29, NAVY, True, "mm")
        text(draw, (x + 165, 442), note, 21, MUTED, False, "mm")
        if index < 2:
            arrow(draw, (x + 338, 360), (x + 397, 360), CYAN, 7)
    rounded(draw, (250, 565, 1030, 655), NAVY, 22)
    text(draw, (640, 610), "理解的證據：預測與實際結果對得上", 29, WHITE, True, "mm")
    save(image, "day08-02-prediction-challenge.png")


def one_hour_plan():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "Spring cron 是六欄，秒數放最前面", 47, WHITE, True)
    text(draw, (64, 108), "0 0 9 * * * ＝ 每天上午九點", 27, "#CBD5E1")
    fields = [
        ("0", "秒", TEAL),
        ("0", "分", BLUE),
        ("9", "時", PURPLE),
        ("*", "日", ORANGE),
        ("*", "月", GREEN),
        ("*", "星期", RED),
    ]
    for index, (value, label, color) in enumerate(fields):
        x = 55 + index * 202
        rounded(draw, (x, 225, x + 175, 465), color, 22)
        text(draw, (x + 87, 305), value, 54, WHITE, True, "mm")
        text(draw, (x + 87, 405), label, 28, WHITE, True, "mm")
    rounded(draw, (170, 545, 1110, 645), WHITE, 22)
    text(draw, (640, 595), "五欄 0 9 * * * → IllegalArgumentException", 28, NAVY, True, "mm")
    save(image, "day08-03-cron-fields.png")


def overlap_guard():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "同一個九點，不是同一個時刻", 47, NAVY, True)
    text(draw, (64, 108), "基準時間：2026-08-18 23:30 UTC", 27, MUTED)

    cards = [
        ("Asia/Taipei", "07:30", "下一次 09:00", "01:00 UTC", BLUE),
        ("Asia/Tokyo", "08:30", "下一次 09:00", "00:00 UTC", ORANGE),
    ]
    for index, (zone, local_now, local_next, instant, color) in enumerate(cards):
        x = 75 + index * 600
        rounded(draw, (x, 205, x + 530, 570), WHITE, 26, color, 5)
        rounded(draw, (x + 30, 238, x + 260, 298), color, 14)
        text(draw, (x + 145, 268), zone, 24, WHITE, True, "mm")
        text(draw, (x + 45, 360), f"當地現在  {local_now}", 27, NAVY, True)
        text(draw, (x + 45, 425), local_next, 29, SLATE, True)
        text(draw, (x + 45, 510), f"= {instant}", 31, color, True)
    rounded(draw, (390, 615, 890, 690), NAVY, 18)
    text(draw, (640, 652), "cron 相同 · 時區不同 · Instant 不同", 24, CYAN, True, "mm")
    save(image, "day08-04-timezones.png")


def evidence():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "從預測表走到可重現結果", 47, NAVY, True)
    text(draw, (64, 108), "ChatGPT 負責找反例，程式與文件負責定案", 27, MUTED)
    layers = [
        ("我的預測", 150, 1050, SLATE),
        ("ChatGPT 反例", 245, 955, ORANGE),
        ("Java 與 JUnit 5", 340, 860, PURPLE),
        ("Spring 官方文件", 435, 765, GREEN),
    ]
    y = 535
    for label, left, right, color in layers:
        rounded(draw, (left, y, right, y + 78), color, 16)
        text(draw, ((left + right) / 2, y + 39), label, 28, WHITE, True, "mm")
        y -= 105
    rounded(draw, (430, 635, 850, 695), NAVY, 18)
    text(draw, (640, 665), "結論還要標出驗證邊界", 24, CYAN, True, "mm")
    save(image, "day08-05-evidence.png")


if __name__ == "__main__":
    cover()
    learning_loop()
    one_hour_plan()
    overlap_guard()
    evidence()
