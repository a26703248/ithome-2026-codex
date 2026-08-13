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
    draw.ellipse((1250, -180, 1770, 340), fill="#312E81")
    draw.ellipse((-250, 650, 220, 1120), fill="#134E4A")
    label(draw, (105, 90), "DAY 22 · 前人砍樹後人曝曬", 38, "#5EEAD4", True)
    label(draw, (105, 210), "AI 輔助除錯實戰", 72, WHITE, True)
    label(draw, (105, 315), "合理解釋不是根因，實驗才是證據", 46, "#CBD5E1", True)

    stages = [
        (130, "症狀", BLUE),
        (470, "假設", PURPLE),
        (810, "實驗", ORANGE),
        (1150, "結論", GREEN),
    ]
    for index, (x, title, color) in enumerate(stages):
        rounded(draw, (x, 565, x + 250, 725), "#111827", 28, color, 5)
        label(draw, (x + 125, 645), title, 37, color, True, "mm")
        if index < len(stages) - 1:
            arrow(draw, (x + 265, 645), (x + 325, 645), "#475569", 7)
    save(image, "day22-01-cover.png")


def symptom_vs_root_cause():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "第一個合理解釋，通常只是起點", 52, NAVY, True)
    label(draw, (85, 132), "同一個延遲症狀，可能來自不同環節", 30, MUTED)

    rounded(draw, (90, 230, 700, 735), WHITE, 30, BLUE, 5)
    label(draw, (395, 295), "看見的症狀", 38, BLUE, True, "mm")
    label(draw, (150, 390), "08:00 批次已啟動", 29, NAVY, True)
    label(draw, (150, 460), "後面的報表較晚才開始", 29, NAVY, True)
    label(draw, (150, 530), "部分信件超過預期時間", 29, NAVY, True)
    rounded(draw, (140, 615, 650, 680), "#EFF6FF", 15)
    label(draw, (395, 648), "症狀描述不等於原因", 25, BLUE, True, "mm")

    rounded(draw, (830, 230, 1510, 735), WHITE, 30, PURPLE, 5)
    label(draw, (1170, 295), "待驗證的假設", 38, PURPLE, True, "mm")
    hypotheses = [
        ("資料計算變慢", ORANGE),
        ("PDF 產生器退化", RED),
        ("郵件回應阻塞流程", GREEN),
    ]
    for index, (text, color) in enumerate(hypotheses):
        y = 405 + index * 105
        draw.ellipse((900, y - 18, 936, y + 18), fill=color)
        label(draw, (965, y), text, 29, NAVY, False, "lm")
    save(image, "day22-02-symptom-vs-root-cause.png")


def hypothesis_table():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "把合理解釋改寫成能被實驗推翻的假設", 48, NAVY, True)
    label(draw, (85, 127), "每次只替換一個外部環節，保留其他條件", 30, MUTED)

    columns = [85, 485, 855, 1190, 1515]
    headers = ["假設", "目前證據", "最小實驗", "結果"]
    rounded(draw, (85, 210, 1515, 305), NAVY, 18)
    for index, header in enumerate(headers):
        left = columns[index]
        right = columns[index + 1]
        label(draw, ((left + right) // 2, 258), header, 27, WHITE, True, "mm")

    rows = [
        ("資料計算變慢", "讀取固定 10 ms", "固定測試資料量", "不支持"),
        ("PDF 元件退化", "產生固定 40 ms", "替換 PDF 測試替身", "不支持"),
        ("郵件阻塞流程", "寄信等待 900 ms", "郵件延遲改為 0", "支持"),
    ]
    for row_index, row in enumerate(rows):
        top = 330 + row_index * 155
        fill = WHITE if row_index % 2 == 0 else "#F1F5F9"
        rounded(draw, (85, top, 1515, top + 125), fill, 14, LINE, 2)
        for col_index, value in enumerate(row):
            left = columns[col_index]
            right = columns[col_index + 1]
            color = GREEN if row_index == 2 and col_index == 3 else NAVY
            label(draw, ((left + right) // 2, top + 62), value, 25, color, row_index == 2, "mm")

    rounded(draw, (260, 805, 1340, 870), "#ECFDF5", 16, GREEN, 3)
    label(draw, (800, 837), "結論只涵蓋縮小案例，不外推成正式環境量測", 26, GREEN, True, "mm")
    save(image, "day22-03-hypothesis-table.png")


def minimal_experiment():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "最小實驗：只改郵件等待時間", 52, WHITE, True)
    label(draw, (85, 132), "第二份報表何時開始，是最直接的觀察值", 30, "#CBD5E1")

    rounded(draw, (110, 235, 720, 680), "#111827", 30, RED, 5)
    label(draw, (415, 300), "舊流程 · 郵件 900 ms", 33, RED, True, "mm")
    label(draw, (175, 400), "讀資料", 26, WHITE)
    label(draw, (175, 468), "PDF", 26, WHITE)
    label(draw, (175, 536), "郵件", 26, WHITE)
    label(draw, (175, 604), "第二份開始", 26, WHITE)
    label(draw, (640, 400), "10 ms", 28, CYAN, True, "rm")
    label(draw, (640, 468), "40 ms", 28, CYAN, True, "rm")
    label(draw, (640, 536), "900 ms", 28, RED, True, "rm")
    label(draw, (640, 604), "950 ms", 34, RED, True, "rm")

    rounded(draw, (880, 235, 1490, 680), "#111827", 30, GREEN, 5)
    label(draw, (1185, 300), "舊流程 · 郵件 0 ms", 33, GREEN, True, "mm")
    label(draw, (945, 400), "讀資料", 26, WHITE)
    label(draw, (945, 468), "PDF", 26, WHITE)
    label(draw, (945, 536), "郵件", 26, WHITE)
    label(draw, (945, 604), "第二份開始", 26, WHITE)
    label(draw, (1410, 400), "10 ms", 28, CYAN, True, "rm")
    label(draw, (1410, 468), "40 ms", 28, CYAN, True, "rm")
    label(draw, (1410, 536), "0 ms", 28, GREEN, True, "rm")
    label(draw, (1410, 604), "50 ms", 34, GREEN, True, "rm")

    rounded(draw, (275, 750, 1325, 835), "#1E293B", 18, ORANGE, 3)
    label(draw, (800, 792), "移除 900 ms 郵件等待，觀察值也少了 900 ms", 29, ORANGE, True, "mm")
    save(image, "day22-04-minimal-experiment.png")


def two_phase_experiment():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "兩階段實驗：先準備報表，再進入寄信階段", 48, NAVY, True)
    label(draw, (85, 125), "固定準備順序，但沒有縮短郵件總耗時", 30, MUTED)

    steps = [
        (95, "準備 1", BLUE),
        (400, "準備 2", BLUE),
        (900, "寄信 1", ORANGE),
        (1205, "寄信 2", ORANGE),
    ]
    for index, (x, text, color) in enumerate(steps):
        rounded(draw, (x, 280, x + 250, 445), WHITE, 24, color, 5)
        label(draw, (x + 125, 362), text, 34, color, True, "mm")
        if index < len(steps) - 1:
            gap_color = TEAL if index == 1 else LINE
            arrow(draw, (x + 265, 362), (x + 290, 362), gap_color, 7)

    rounded(draw, (110, 560, 1490, 790), NAVY, 28)
    label(draw, (800, 610), "mvn clean test", 34, CYAN, True, "mm")
    label(draw, (800, 675), "Tests run: 3 · Failures: 0 · Errors: 0", 28, WHITE, True, "mm")
    label(draw, (800, 755), "BUILD SUCCESS", 31, GREEN, True, "mm")
    save(image, "day22-05-fix-and-regression.png")


if __name__ == "__main__":
    cover()
    symptom_vs_root_cause()
    hypothesis_table()
    minimal_experiment()
    two_phase_experiment()
