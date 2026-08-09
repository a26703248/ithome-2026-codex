from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1600, 900
ROOT = Path(__file__).parent
FONT_REGULAR = Path(r"C:\Windows\Fonts\msjh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msjhbd.ttc")

NAVY = "#0F172A"
SLATE = "#334155"
MUTED = "#64748B"
PALE = "#F8FAFC"
WHITE = "#FFFFFF"
TEAL = "#14B8A6"
CYAN = "#22D3EE"
BLUE = "#3B82F6"
ORANGE = "#F97316"
GREEN = "#16A34A"
RED = "#DC2626"
PURPLE = "#8B5CF6"
LINE = "#CBD5E1"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded(draw, box, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(draw, xy, value, size, fill, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def arrow(draw, start, end, color=CYAN, width=8):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    draw.polygon([(ex, ey), (ex - 22, ey - 15), (ex - 22, ey + 15)], fill=color)


def save(image, name):
    image.save(ROOT / name, format="PNG", optimize=True)


def cover():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.ellipse((1230, -180, 1770, 360), fill="#312E81")
    draw.ellipse((-250, 650, 220, 1120), fill="#134E4A")
    label(draw, (105, 90), "DAY 20 · 進階整合工作流", 38, "#5EEAD4", True)
    label(draw, (105, 210), "遺留程式碼考古", 72, WHITE, True)
    label(draw, (105, 315), "每個理解，都要能回到證據", 47, "#CBD5E1", True)

    nodes = [
        (115, "入口", BLUE),
        (420, "資料", PURPLE),
        (725, "流程", TEAL),
        (1030, "PDF", ORANGE),
        (1335, "寄信", RED),
    ]
    for index, (x, title, color) in enumerate(nodes):
        draw.ellipse((x, 585, x + 150, 735), fill=color)
        label(draw, (x + 75, 660), title, 28, WHITE, True, "mm")
        if index < len(nodes) - 1:
            arrow(draw, (x + 165, 660), (x + 285, 660), "#475569", 7)
    save(image, "day20-01-cover.png")


def five_directions():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "不要逐檔摘要，先從五個方向找證據", 50, NAVY, True)
    label(draw, (85, 132), "閱讀順序沿著實際行為，不沿著資料夾排列", 30, MUTED)

    rounded(draw, (570, 300, 1030, 610), NAVY, 36)
    label(draw, (800, 390), "每日 08:00", 43, CYAN, True, "mm")
    label(draw, (800, 470), "產生 PDF 並寄信", 35, WHITE, True, "mm")
    label(draw, (800, 540), "可驗證的業務路徑", 25, "#CBD5E1", False, "mm")

    cards = [
        (90, 245, "外部入口", "runAt()", BLUE),
        (1100, 245, "資料存取", "訂閱者／數值", PURPLE),
        (90, 610, "外部整合", "PDF／郵件", ORANGE),
        (1100, 610, "副作用邊界", "產生器／郵件閘道", RED),
        (570, 690, "核心流程", "組合與協調", TEAL),
    ]
    for x, y, title, note, color in cards:
        rounded(draw, (x, y, x + 410, y + 150), WHITE, 22, color, 4)
        label(draw, (x + 205, y + 50), title, 30, color, True, "mm")
        label(draw, (x + 205, y + 105), note, 23, SLATE, False, "mm")
    save(image, "day20-02-five-directions.png")


def call_path():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "從批次入口追到兩個外部整合呼叫", 52, NAVY, True)
    label(draw, (85, 132), "每個節點都附檔案、方法與輸入、輸出", 30, MUTED)

    steps = [
        (55, "Job", "runAt", BLUE),
        (355, "訂閱資料", "findDaily…", PURPLE),
        (655, "Service", "generate…", TEAL),
        (955, "數值資料", "loadPrevious…", PURPLE),
        (1255, "PDF＋寄信", "render／send", RED),
    ]
    for index, (x, title, method, color) in enumerate(steps):
        rounded(draw, (x, 300, x + 240, 585), WHITE, 24, color, 5)
        draw.ellipse((x + 75, 335, x + 165, 425), fill=color)
        label(draw, (x + 120, 380), str(index + 1), 32, WHITE, True, "mm")
        label(draw, (x + 120, 485), title, 27, NAVY, True, "mm")
        label(draw, (x + 120, 535), method, 20, SLATE, False, "mm")
        if index < len(steps) - 1:
            arrow(draw, (x + 250, 445), (x + 285, 445), LINE, 7)

    rounded(draw, (280, 710, 1320, 820), NAVY, 20)
    label(draw, (800, 765), "靜態追蹤已確認 ≠ 正式環境行為已確認", 31, CYAN, True, "mm")
    save(image, "day20-03-call-path.png")


def certainty_boundary():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "理解地圖要同時保留確定與未知", 52, NAVY, True)
    label(draw, (85, 132), "不知道就列成問題，不用順暢敘事補空白", 30, MUTED)

    rounded(draw, (90, 230, 755, 760), WHITE, 30, GREEN, 5)
    label(draw, (422, 290), "已由程式與測試確認", 36, GREEN, True, "mm")
    confirmed = ["08:00 才進入流程", "讀取訂閱者與前日數值", "組合固定內文與檔名", "PDF、郵件邊界均被呼叫"]
    for i, item in enumerate(confirmed):
        y = 390 + i * 82
        draw.ellipse((150, y - 16, 182, y + 16), fill=GREEN)
        label(draw, (205, y), item, 27, NAVY, False, "lm")

    rounded(draw, (845, 230, 1510, 760), WHITE, 30, RED, 5)
    label(draw, (1177, 290), "仍待正式環境確認", 36, RED, True, "mm")
    unknown = ["排程器是否只呼叫一次", "設定值從哪裡注入", "PDF 是否寫暫存檔", "郵件重試與冪等策略"]
    for i, item in enumerate(unknown):
        y = 390 + i * 82
        draw.ellipse((905, y - 16, 937, y + 16), fill=RED)
        label(draw, (960, y), item, 27, NAVY, False, "lm")
    save(image, "day20-04-certainty-boundary.png")


def characterization_test():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "特徵測試：固定現況，也揭露風險", 52, WHITE, True)
    label(draw, (85, 132), "綠燈代表描述準確，不代表舊行為正確", 30, "#CBD5E1")

    rounded(draw, (110, 250, 720, 650), "#111827", 30, GREEN, 5)
    label(draw, (415, 320), "08:00 現有輸出", 36, GREEN, True, "mm")
    label(draw, (415, 420), "PDF 替身：1 次", 31, WHITE, True, "mm")
    label(draw, (415, 485), "郵件替身：1 次", 31, WHITE, True, "mm")
    label(draw, (415, 565), "附件名稱與內文已固定", 25, "#A7F3D0", False, "mm")

    rounded(draw, (880, 250, 1490, 650), "#111827", 30, RED, 5)
    label(draw, (1185, 320), "同一分鐘重跑", 36, RED, True, "mm")
    label(draw, (1185, 420), "PDF 替身：2 次", 31, WHITE, True, "mm")
    label(draw, (1185, 485), "郵件替身：2 次", 31, WHITE, True, "mm")
    label(draw, (1185, 565), "缺少冪等防線", 25, "#FECACA", False, "mm")

    rounded(draw, (315, 735, 1285, 835), "#1E293B", 18, CYAN, 3)
    label(draw, (800, 785), "Tests run: 2 · Failures: 0 · BUILD SUCCESS", 27, CYAN, True, "mm")
    save(image, "day20-05-characterization-test.png")


if __name__ == "__main__":
    cover()
    five_directions()
    call_path()
    certainty_boundary()
    characterization_test()
