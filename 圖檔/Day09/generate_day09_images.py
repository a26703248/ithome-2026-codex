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
    draw.ellipse((1000, -170, 1400, 230), fill="#0C4A6E")
    draw.ellipse((-170, 520, 190, 880), fill="#312E81")
    text(draw, (70, 70), "DAY 09 · CODE REVIEW", 34, CYAN, True)
    text(draw, (70, 165), "先找疑點，", 66, WHITE, True)
    text(draw, (70, 250), "再決定能不能合併", 66, WHITE, True)
    text(draw, (70, 342), "ChatGPT 初篩 × JUnit 證據 × 人工決策", 31, "#CBD5E1")

    cards = [("疑", "指出觸發條件", BLUE), ("驗", "寫測試重現", ORANGE), ("決", "人工判斷", GREEN)]
    x = 70
    for tag, note, color in cards:
        rounded(draw, (x, 480, x + 340, 625), WHITE, 24)
        draw.ellipse((x + 24, 515, x + 88, 579), fill=color)
        text(draw, (x + 56, 547), tag, 28, WHITE, True, "mm")
        text(draw, (x + 118, 547), note, 26, NAVY, True, "lm")
        x += 405
    save(image, "day09-01-cover.png")


def three_layers():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "初篩、證據、決策分成三層", 47, NAVY, True)
    text(draw, (64, 108), "先寫失敗斷言；目前不能重現的項目先保留追查", 27, MUTED)
    cards = [
        ("1", "ChatGPT 初篩", "擴大搜尋面\n標出疑點", BLUE),
        ("2", "自動化工具", "編譯與測試\n留下結果", ORANGE),
        ("3", "人工審查", "補業務脈絡\n決定是否擋下", GREEN),
    ]
    for index, (number, title, note, color) in enumerate(cards):
        x = 65 + index * 410
        rounded(draw, (x, 220, x + 335, 525), WHITE, 24, color, 4)
        draw.ellipse((x + 132, 252, x + 202, 322), fill=color)
        text(draw, (x + 167, 287), number, 29, WHITE, True, "mm")
        text(draw, (x + 167, 380), title, 28, NAVY, True, "mm")
        text(draw, (x + 167, 455), note, 23, MUTED, False, "mm")
        if index < 2:
            arrow(draw, (x + 343, 372), (x + 402, 372))
    rounded(draw, (260, 585, 1020, 660), NAVY, 18)
    text(draw, (640, 622), "ChatGPT 輸出是審查輸入，不是合併依據", 28, CYAN, True, "mm")
    save(image, "day09-02-three-layers.png")


def diff_findings():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 45), "一小段 diff，藏了三種失敗條件", 45, WHITE, True)
    rounded(draw, (55, 125, 780, 655), "#111827", 18, "#475569", 2)
    code = [
        ("13", "if (workspaceId.isBlank()) {", RED, 23),
        ("16", "String key = workspaceId.strip().toLowerCase(Locale.ROOT);", WHITE, 18),
        ("17", "if (runningWorkspaces.contains(key)) {", ORANGE, 21),
        ("20", "runningWorkspaces.add(key);", ORANGE, 21),
        ("25", "runningWorkspaces.remove(workspaceId);", PURPLE, 20),
    ]
    y = 190
    for line, value, color, code_size in code:
        text(draw, (90, y), line, 23, MUTED, False)
        text(draw, (150, y), value, code_size, color, False)
        y += 82
    findings = [
        ("null", "例外型別失控", RED, 170),
        ("並行", "兩批都回傳成功", ORANGE, 330),
        ("鍵值", "完成後仍未釋放", PURPLE, 490),
    ]
    for tag, note, color, y in findings:
        rounded(draw, (835, y, 1205, y + 110), WHITE, 18, color, 4)
        rounded(draw, (855, y + 22, 950, y + 82), color, 14)
        text(draw, (902, y + 52), tag, 23, WHITE, True, "mm")
        text(draw, (980, y + 52), note, 23, NAVY, True, "lm")
    save(image, "day09-03-diff-findings.png")


def red_green():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "把建議寫成測試，才知道是不是缺陷", 45, NAVY, True)
    text(draw, (64, 108), "同一組四項 JUnit 5 測試，修正前後各跑一次", 27, MUTED)
    cards = [
        (70, "修正前", "4 tests", "3 failures", "BUILD FAILURE", RED),
        (690, "最小修正後", "4 tests", "0 failures", "BUILD SUCCESS", GREEN),
    ]
    for x, title, count, result, build, color in cards:
        rounded(draw, (x, 205, x + 520, 555), WHITE, 26, color, 5)
        text(draw, (x + 260, 265), title, 32, color, True, "mm")
        text(draw, (x + 260, 355), count, 36, NAVY, True, "mm")
        text(draw, (x + 260, 425), result, 29, SLATE, True, "mm")
        rounded(draw, (x + 110, 480, x + 410, 535), color, 14)
        text(draw, (x + 260, 507), build, 22, WHITE, True, "mm")
    arrow(draw, (600, 380), (675, 380), CYAN, 9)
    rounded(draw, (330, 610, 950, 680), NAVY, 18)
    text(draw, (640, 645), "紅字不是答案；可重現步驟才是證據", 26, CYAN, True, "mm")
    save(image, "day09-04-red-green.png")


def comparison():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 45), "模擬初篩也要接受三方交叉", 44, NAVY, True)
    columns = [(60, 430, "問題"), (430, 670, "模擬初篩"), (670, 915, "測試／文件"), (915, 1220, "結論")]
    for left, right, label in columns:
        rounded(draw, (left, 125, right, 190), NAVY, 10)
        text(draw, ((left + right) / 2, 157), label, 23, WHITE, True, "mm")
    rows = [
        ("null 例外", "找到", "紅燈", "修正", GREEN),
        ("contains + add", "找到", "並行紅燈", "單次 add", GREEN),
        ("newKeySet 並行保證", "待查", "Java API 文件", "排除", RED),
        ("finish 鍵不一致", "漏報", "人工補測試", "修正", PURPLE),
    ]
    y = 210
    for issue, ai, evidence, result, color in rows:
        values = [issue, ai, evidence, result]
        for index, (left, right, _) in enumerate(columns):
            fill = WHITE if index < 3 else color
            rounded(draw, (left, y, right, y + 85), fill, 8, "#CBD5E1", 1)
            text_color = NAVY if index < 3 else WHITE
            text(draw, ((left + right) / 2, y + 42), values[index], 22, text_color, index == 3, "mm")
        y += 100
    rounded(draw, (260, 630, 1020, 695), NAVY, 16)
    text(draw, (640, 662), "找到不等於定案，沒找到也不等於沒有", 25, CYAN, True, "mm")
    save(image, "day09-05-comparison.png")


if __name__ == "__main__":
    cover()
    three_layers()
    diff_findings()
    red_green()
    comparison()
