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
BLUE = "#2563EB"
ORANGE = "#F97316"
GREEN = "#16A34A"
RED = "#DC2626"
PURPLE = "#7C3AED"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded(draw, box, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(draw, xy, value, size, fill, bold=False, anchor=None):
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
    draw.ellipse((990, -180, 1410, 240), fill="#0C4A6E")
    draw.ellipse((-190, 500, 210, 900), fill="#312E81")
    label(draw, (70, 70), "DAY 11 · CODEX", 34, CYAN, True)
    label(draw, (70, 165), "從回答，", 66, WHITE, True)
    label(draw, (70, 250), "走到可驗證的修改", 66, WHITE, True)
    label(draw, (70, 345), "讀取 × 修改 × 測試 × 回報", 31, "#CBD5E1")

    cards = [("讀", "理解範圍", BLUE), ("做", "操作專案", ORANGE), ("驗", "留下證據", GREEN)]
    x = 70
    for tag, note, color in cards:
        rounded(draw, (x, 480, x + 340, 625), WHITE, 24)
        draw.ellipse((x + 24, 515, x + 88, 579), fill=color)
        label(draw, (x + 56, 547), tag, 28, WHITE, True, "mm")
        label(draw, (x + 118, 547), note, 26, NAVY, True, "lm")
        x += 405
    save(image, "day11-01-cover.png")


def agent_loop():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (64, 52), "用四個檢查點讀代理的工作紀錄", 44, NAVY, True)
    label(draw, (64, 105), "取得新結果後，下一個動作也會跟著調整", 27, MUTED)
    steps = [
        ("1", "定位", BLUE), ("2", "動作", PURPLE),
        ("3", "驗證", GREEN), ("4", "交付", ORANGE),
    ]
    positions = [(90, 285), (390, 285), (690, 285), (990, 285)]
    for (number, title, color), (x, y) in zip(steps, positions):
        rounded(draw, (x, y, x + 200, y + 150), WHITE, 22, color, 4)
        draw.ellipse((x + 65, y + 20, x + 135, y + 90), fill=color)
        label(draw, (x + 100, y + 55), number, 27, WHITE, True, "mm")
        label(draw, (x + 100, y + 120), title, 30, NAVY, True, "mm")
    arrow(draw, (295, 360), (375, 360))
    arrow(draw, (595, 360), (675, 360))
    arrow(draw, (895, 360), (975, 360))
    draw.line([(1090, 450), (1090, 535), (190, 535), (190, 450)], fill=CYAN, width=7)
    draw.polygon([(190, 450), (178, 468), (202, 468)], fill=CYAN)
    rounded(draw, (350, 575, 930, 660), NAVY, 18)
    label(draw, (640, 617), "發現新線索，就回到定位重新判斷", 27, CYAN, True, "mm")
    save(image, "day11-02-agent-loop.png")


def boundary():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (64, 48), "面對一個動作，我先問兩個問題", 45, WHITE, True)
    label(draw, (64, 102), "現在碰得到什麼？若要跨出去，誰來開門？", 27, "#CBD5E1")
    rounded(draw, (80, 180, 790, 625), "#111827", 28, CYAN, 5)
    label(draw, (115, 220), "目前可操作的範圍", 30, CYAN, True)
    cards = [
        ("讀檔", "限定專案內容", BLUE, 290),
        ("改檔", "只寫開放範圍", ORANGE, 410),
        ("跑工具", "沿用相同限制", GREEN, 530),
    ]
    for title, note, color, y in cards:
        rounded(draw, (125, y, 730, y + 85), WHITE, 16)
        rounded(draw, (150, y + 17, 270, y + 68), color, 12)
        label(draw, (210, y + 42), title, 22, WHITE, True, "mm")
        label(draw, (310, y + 42), note, 22, NAVY, True, "lm")
    rounded(draw, (875, 210, 1200, 390), WHITE, 22, ORANGE, 5)
    label(draw, (1037, 265), "想碰其他位置", 27, NAVY, True, "mm")
    label(draw, (1037, 325), "先停下來", 25, ORANGE, True, "mm")
    rounded(draw, (875, 445, 1200, 625), WHITE, 22, RED, 5)
    label(draw, (1037, 500), "想連外部網路", 27, NAVY, True, "mm")
    label(draw, (1037, 560), "交給門禁判斷", 25, RED, True, "mm")
    arrow(draw, (795, 330), (855, 300), ORANGE, 7)
    arrow(draw, (795, 500), (855, 530), RED, 7)
    save(image, "day11-03-boundary.png")


def work_log():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (64, 48), "一次真實工作紀錄：先分清環境失敗與測試失敗", 42, NAVY, True)
    label(draw, (64, 100), "同一個 mvn clean test，失敗原因可能完全不同", 27, MUTED)
    events = [
        ("1", "讀任務", "只改主程式", BLUE),
        ("2", "跑測試", "連線被擋", RED),
        ("3", "核准後重跑", "2 項測試失敗", ORANGE),
        ("4", "最小修改", "只在有餘數時 +1", PURPLE),
        ("5", "再次驗證", "5 項全部通過", GREEN),
    ]
    x = 55
    for index, (number, title, note, color) in enumerate(events):
        rounded(draw, (x, 220, x + 210, 520), WHITE, 22, color, 4)
        draw.ellipse((x + 70, 248, x + 140, 318), fill=color)
        label(draw, (x + 105, 283), number, 28, WHITE, True, "mm")
        label(draw, (x + 105, 375), title, 24, NAVY, True, "mm")
        label(draw, (x + 105, 445), note, 21, MUTED, False, "mm")
        if index < len(events) - 1:
            arrow(draw, (x + 215, 370), (x + 245, 370), CYAN, 6)
        x += 245
    rounded(draw, (250, 590, 1030, 665), NAVY, 18)
    label(draw, (640, 627), "JUnit 沒啟動，就不能拿紅字判斷程式修壞", 26, CYAN, True, "mm")
    save(image, "day11-04-work-log.png")


def evidence():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (64, 50), "完成訊息之外，我固定檢查三份證據", 45, NAVY, True)
    label(draw, (64, 105), "少任何一份，都不能把代理回報當成交付", 27, MUTED)
    cards = [
        ("DIFF", "只改 1 個方法", "沒有無關重構", BLUE),
        ("TEST", "5 項通過", "同一命令重跑", GREEN),
        ("HUMAN", "人工驗收", "補上剩餘風險", ORANGE),
    ]
    x = 70
    for tag, title, note, color in cards:
        rounded(draw, (x, 220, x + 340, 535), WHITE, 26, color, 5)
        rounded(draw, (x + 85, 255, x + 255, 315), color, 14)
        label(draw, (x + 170, 285), tag, 23, WHITE, True, "mm")
        label(draw, (x + 170, 390), title, 31, NAVY, True, "mm")
        label(draw, (x + 170, 460), note, 22, MUTED, False, "mm")
        x += 400
    rounded(draw, (270, 600, 1010, 675), NAVY, 18)
    label(draw, (640, 637), "Codex 執行，人負責最後判斷", 28, CYAN, True, "mm")
    save(image, "day11-05-evidence.png")


if __name__ == "__main__":
    cover()
    agent_loop()
    boundary()
    work_log()
    evidence()
