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
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    d.ellipse((1010, -160, 1390, 220), fill="#0C4A6E")
    d.ellipse((-170, 520, 190, 880), fill="#312E81")
    text(d, (70, 70), "DAY 06 · 提示工程", 34, CYAN, True)
    text(d, (70, 165), "把提示詞，", 66, WHITE, True)
    text(d, (70, 250), "寫成工作說明", 66, WHITE, True)
    text(d, (70, 342), "交代目標，也交代怎麼證明完成", 31, "#CBD5E1")

    labels = [("1", "任務", TEAL), ("2", "條件", BLUE), ("3", "驗收", ORANGE)]
    x = 82
    for number, label, color in labels:
        rounded(d, (x, 490, x + 300, 625), WHITE, 25)
        d.ellipse((x + 28, 526, x + 80, 578), fill=color)
        text(d, (x + 54, 553), number, 24, WHITE, True, "mm")
        text(d, (x + 105, 555), label, 38, NAVY, True, "lm")
        x += 405
    save(im, "day06-01-cover.png")


def six_parts():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "我的提示詞六欄檢查表", 47, NAVY, True)
    text(d, (64, 108), "不是固定咒語，而是避免漏掉工作條件", 27, MUTED)
    items = [
        ("1", "任務", "要完成什麼", TEAL),
        ("2", "背景", "為什麼要做", BLUE),
        ("3", "輸入", "可以依據什麼", PURPLE),
        ("4", "限制", "哪些不能碰", RED),
        ("5", "輸出", "交付長什麼樣", ORANGE),
        ("6", "驗收", "如何證明完成", GREEN),
    ]
    for i, (number, title, note, color) in enumerate(items):
        row, col = divmod(i, 3)
        x = 64 + col * 405
        y = 178 + row * 205
        rounded(d, (x, y, x + 360, y + 160), WHITE, 22, color, 4)
        d.ellipse((x + 26, y + 34, x + 84, y + 92), fill=color)
        text(d, (x + 55, y + 64), number, 25, WHITE, True, "mm")
        text(d, (x + 110, y + 57), title, 31, NAVY, True, "lm")
        text(d, (x + 110, y + 108), note, 22, MUTED, False, "lm")
    rounded(d, (180, 608, 1100, 670), NAVY, 18)
    text(d, (640, 640), "任務風險越高，六欄越需要寫完整", 25, WHITE, True, "mm")
    save(im, "day06-02-six-parts.png")


def prompt_evolution():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "同一任務，逐輪補齊可驗收資訊", 47, WHITE, True)
    text(d, (64, 108), "提示詞變長不是目的；未知資訊變少才是", 27, "#CBD5E1")
    cards = [
        ("V1", "只有任務", ["資料格式未知", "目標模型未知", "只能猜"], RED),
        ("V2", "加入背景", ["欄位已知", "限制已知", "預設值待決"], ORANGE),
        ("V3", "加入驗收", ["規則可追蹤", "測試可執行", "假設要回報"], GREEN),
    ]
    for i, (tag, title, lines, color) in enumerate(cards):
        x = 64 + i * 405
        rounded(d, (x, 180, x + 360, 565), WHITE, 24, color, 4)
        rounded(d, (x + 120, 205, x + 240, 260), color, 14)
        text(d, (x + 180, 234), tag, 26, WHITE, True, "mm")
        text(d, (x + 180, 315), title, 31, NAVY, True, "mm")
        for j, line in enumerate(lines):
            y = 385 + j * 57
            d.ellipse((x + 52, y - 8, x + 68, y + 8), fill=color)
            text(d, (x + 90, y), line, 22, SLATE, True, "lm")
        if i < 2:
            arrow(d, (x + 365, 370), (x + 400, 370), CYAN, 7)
    rounded(d, (225, 615, 1055, 670), "#164E63", 16)
    text(d, (640, 643), "每一輪只補會改變結果的資訊", 24, WHITE, True, "mm")
    save(im, "day06-03-prompt-evolution.png")


def quality_check():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "回應品質，不能只看文字像不像答案", 47, NAVY, True)
    text(d, (64, 108), "把生成內容送進驗收迴圈，才能看見隱藏假設", 27, MUTED)
    stages = [
        ("提示詞", "條件完整", TEAL),
        ("程式差異", "範圍最小", BLUE),
        ("JUnit 5", "6 項測試", PURPLE),
        ("人工核對", "業務語意", ORANGE),
    ]
    for i, (title, note, color) in enumerate(stages):
        x = 55 + i * 305
        rounded(d, (x, 225, x + 245, 410), WHITE, 22, color, 4)
        d.ellipse((x + 88, 250, x + 157, 319), fill=color)
        text(d, (x + 122, 285), str(i + 1), 28, WHITE, True, "mm")
        text(d, (x + 122, 350), title, 27, NAVY, True, "mm")
        text(d, (x + 122, 386), note, 20, MUTED, False, "mm")
        if i < 3:
            arrow(d, (x + 250, 318), (x + 298, 318), CYAN, 7)
    rounded(d, (155, 500, 1125, 640), NAVY, 22)
    text(d, (640, 546), "測試通過 ≠ 業務決策正確", 31, CYAN, True, "mm")
    text(d, (640, 597), "它只證明程式符合目前寫下的規則", 25, WHITE, True, "mm")
    save(im, "day06-04-quality-check.png")


def reusable_card():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "可複用提示詞卡片", 47, WHITE, True)
    text(d, (64, 108), "需要時展開六欄，不必每次貼滿整份模板", 27, "#CBD5E1")
    rounded(d, (90, 165, 1190, 620), WHITE, 28)
    columns = [
        ("交代工作", ["任務：＿＿＿＿", "背景：＿＿＿＿", "輸入：＿＿＿＿"], TEAL),
        ("劃出邊界", ["限制：＿＿＿＿", "不可修改：＿＿", "敏感資料：排除"], RED),
        ("要求證據", ["輸出：＿＿＿＿", "驗收：＿＿＿＿", "未確認：列出"], GREEN),
    ]
    for i, (title, lines, color) in enumerate(columns):
        x = 125 + i * 355
        rounded(d, (x, 205, x + 320, 560), "#F8FAFC", 22, color, 4)
        text(d, (x + 160, 260), title, 31, color, True, "mm")
        d.line((x + 35, 300, x + 285, 300), fill=color, width=3)
        for j, line in enumerate(lines):
            text(d, (x + 42, 355 + j * 72), line, 23, SLATE, j == 2, "lm")
    rounded(d, (250, 642, 1030, 690), "#164E63", 14)
    text(d, (640, 666), "先交代工作，再要求可核對的完成證據", 23, WHITE, True, "mm")
    save(im, "day06-05-reusable-card.png")


if __name__ == "__main__":
    cover()
    six_parts()
    prompt_evolution()
    quality_check()
    reusable_card()
