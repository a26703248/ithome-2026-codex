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


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded(draw, box, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, fill, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def arrow(draw, start, end, color=CYAN, width=8):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        direction = 1 if ex > sx else -1
        points = [(ex, ey), (ex - direction * 20, ey - 14), (ex - direction * 20, ey + 14)]
    else:
        direction = 1 if ey > sy else -1
        points = [(ex, ey), (ex - 14, ey - direction * 20), (ex + 14, ey - direction * 20)]
    draw.polygon(points, fill=color)


def save(image, name):
    image.save(ROOT / name, format="PNG", optimize=True)


def cover():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    d.ellipse((1010, -130, 1370, 230), fill="#0C4A6E")
    d.ellipse((-170, 520, 190, 880), fill="#172554")
    text(d, (70, 70), "DAY 05 · 需求釐清", 34, CYAN, True)
    text(d, (70, 170), "先把未知攤開，", 66, WHITE, True)
    text(d, (70, 254), "再開始設計", 66, WHITE, True)
    text(d, (70, 340), "ChatGPT 找缺口，人決定規則與責任", 31, "#CBD5E1")

    labels = [("事實", TEAL), ("假設", ORANGE), ("決策", BLUE)]
    x = 92
    for label, color in labels:
        rounded(d, (x, 485, x + 285, 625), WHITE, 25)
        d.ellipse((x + 28, 520, x + 76, 568), fill=color)
        if label == "事實":
            d.line((x + 37, 545, x + 48, 556), fill=WHITE, width=6)
            d.line((x + 48, 556, x + 67, 532), fill=WHITE, width=6)
        else:
            text(d, (x + 52, 545), "?", 29, WHITE, True, "mm")
        text(d, (x + 98, 548), label, 38, NAVY, True, "lm")
        x += 405
    save(im, "day05-01-cover.png")


def hidden_gaps():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "一句需求，至少藏著四類未決問題", 47, NAVY, True)
    text(d, (64, 108), "句子有動作，不代表已經可以估工與驗收", 27, MUTED)
    rounded(d, (64, 160, 1216, 285), WHITE, 22, "#CBD5E1", 2)
    text(d, (640, 202), "「把自行爬文或企業內部資料匯入工作區，繼續編輯加值」", 31, NAVY, True, "mm")
    text(d, (640, 250), "業務目標清楚　｜　執行規則未定", 23, TEAL, True, "mm")

    cards = [
        ("資料", "欄位是否對齊？", BLUE),
        ("權限", "誰可以匯入？", ORANGE),
        ("流程", "日報何時執行？", TEAL),
        ("驗收", "怎樣才算完成？", RED),
    ]
    for i, (title, body, color) in enumerate(cards):
        x = 64 + i * 291
        rounded(d, (x, 345, x + 260, 575), WHITE, 22, color, 4)
        d.ellipse((x + 90, 375, x + 170, 455), fill=color)
        text(d, (x + 130, 417), str(i + 1), 36, WHITE, True, "mm")
        text(d, (x + 130, 500), title, 32, color, True, "mm")
        text(d, (x + 130, 542), body, 22, SLATE, False, "mm")
    rounded(d, (210, 620, 1070, 676), NAVY, 16)
    text(d, (640, 649), "缺少規則時，工程團隊只是在各自猜答案", 25, WHITE, True, "mm")
    save(im, "day05-02-hidden-gaps.png")


def four_buckets():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "讓每句需求都有狀態", 47, NAVY, True)
    text(d, (64, 108), "分類不是排版，而是把下一個責任人找出來", 27, MUTED)
    cards = [
        ("01", "已知事實", "保留文件位置", TEAL, "#ECFEFF"),
        ("02", "暫時假設", "要求證據驗證", ORANGE, "#FFF7ED"),
        ("03", "待決策", "交回負責人拍板", BLUE, "#EFF6FF"),
        ("04", "版本範圍", "明確納入或排除", GREEN, "#F0FDF4"),
    ]
    for i, (num, title, body, color, bg) in enumerate(cards):
        col, row = i % 2, i // 2
        x, y = 64 + col * 590, 170 + row * 225
        rounded(d, (x, y, x + 550, y + 185), bg, 24, color, 3)
        rounded(d, (x + 25, y + 31, x + 105, y + 111), color, 18)
        text(d, (x + 65, y + 73), num, 29, WHITE, True, "mm")
        text(d, (x + 135, y + 62), title, 34, NAVY, True)
        text(d, (x + 135, y + 113), body, 25, SLATE)
        text(d, (x + 135, y + 150), "→ 下一個動作可追蹤", 20, color, True)
    save(im, "day05-03-four-buckets.png")


def three_rounds():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "三輪對話，不是一次生成完整規格", 47, WHITE, True)
    text(d, (64, 108), "每輪只消除一種不確定性，也保留人工檢查點", 27, "#CBD5E1")
    rounds = [
        ("1", "找缺口", "只依 v0 文件\n列出歧義與缺漏", TEAL),
        ("2", "補證據", "加入範圍、欄位\n資料量與速率", ORANGE),
        ("3", "寫驗收", "把候選規則\n改成驗收草案", BLUE),
    ]
    xs = [70, 470, 870]
    for idx, ((num, title, body, color), x) in enumerate(zip(rounds, xs)):
        rounded(d, (x, 200, x + 330, 510), WHITE, 28)
        d.ellipse((x + 125, 230, x + 205, 310), fill=color)
        text(d, (x + 165, 271), num, 36, WHITE, True, "mm")
        text(d, (x + 165, 360), title, 38, NAVY, True, "mm")
        line1, line2 = body.split("\n")
        text(d, (x + 165, 417), line1, 23, SLATE, False, "mm")
        text(d, (x + 165, 452), line2, 23, SLATE, False, "mm")
        if idx < 2:
            arrow(d, (x + 342, 355), (x + 388, 355), CYAN, 7)
    rounded(d, (165, 570, 1115, 646), "#164E63", 18)
    text(d, (640, 609), "每一輪都要回看原文件，模型回覆不是需求證據", 27, WHITE, True, "mm")
    save(im, "day05-04-three-rounds.png")


def acceptance():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "把候選規則改成可驗收草案", 47, NAVY, True)
    text(d, (64, 108), "Given／When／Then 讓前提、操作與預期結果可以逐項核對", 27, MUTED)
    blocks = [
        ("GIVEN", "前提", "候選規則允許租戶 A\n使用者匯入工作區 W", TEAL),
        ("WHEN", "操作", "匯入一筆含有\n本輪暫定欄位的資料", ORANGE),
        ("THEN", "預期結果", "租戶 A 看得到資料\n租戶 B 無法存取", GREEN),
    ]
    for i, (tag, title, body, color) in enumerate(blocks):
        x = 64 + i * 405
        rounded(d, (x, 180, x + 360, 480), WHITE, 26, color, 4)
        rounded(d, (x + 28, 210, x + 150, 256), color, 14)
        text(d, (x + 89, 234), tag, 20, WHITE, True, "mm")
        text(d, (x + 28, 315), title, 38, NAVY, True)
        line1, line2 = body.split("\n")
        text(d, (x + 28, 380), line1, 23, SLATE)
        text(d, (x + 28, 420), line2, 23, SLATE)
        if i < 2:
            arrow(d, (x + 365, 330), (x + 395, 330), "#94A3B8", 6)
    rounded(d, (140, 545, 1140, 655), NAVY, 22)
    text(d, (640, 580), "仍待決策：無權限回應｜部分錯誤策略｜重送是否去重", 25, WHITE, True, "mm")
    text(d, (640, 622), "保留未知，比用猜測補滿規格更安全", 24, CYAN, True, "mm")
    save(im, "day05-05-acceptance.png")


if __name__ == "__main__":
    cover()
    hidden_gaps()
    four_buckets()
    three_rounds()
    acceptance()
