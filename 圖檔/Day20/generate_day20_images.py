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
    draw.ellipse((1230, -180, 1770, 360), fill="#1E3A8A")
    draw.ellipse((-250, 650, 220, 1120), fill="#134E4A")
    label(draw, (105, 90), "DAY 20 · 前人砍樹後人曝曬", 38, "#5EEAD4", True)
    label(draw, (105, 210), "自動化測試維運", 72, WHITE, True)
    label(draw, (105, 315), "先證明根因，再處理紅燈", 47, "#CBD5E1", True)

    cards = [
        (100, "紅燈", "固定重現", RED),
        (485, "假設", "依序驗證", ORANGE),
        (870, "修正", "最小差異", BLUE),
        (1255, "綠燈", "留下證據", GREEN),
    ]
    for x, title, note, color in cards:
        rounded(draw, (x, 570, x + 300, 735), "#1E293B", 24, color, 4)
        label(draw, (x + 150, 620), title, 31, color, True, "mm")
        label(draw, (x + 150, 680), note, 25, WHITE, False, "mm")
    save(image, "day20-01-cover.png")


def failure_classification():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "CI 紅燈先分五類，再決定修哪裡", 53, NAVY, True)
    label(draw, (85, 132), "錯誤分類，比立刻修改斷言更重要", 31, MUTED)

    cards = [
        (65, "產品缺陷", "固定輸入仍失敗", RED),
        (370, "測試缺陷", "斷言不符規格", ORANGE),
        (675, "環境差異", "版本／時區不同", BLUE),
        (980, "相依問題", "JUnit 尚未啟動", PURPLE),
        (1285, "偶發失敗", "結果無法重現", TEAL),
    ]
    for x, title, note, color in cards:
        rounded(draw, (x, 265, x + 250, 610), WHITE, 24, color, 5)
        draw.ellipse((x + 85, 315, x + 165, 395), fill=color)
        label(draw, (x + 125, 355), "?", 38, WHITE, True, "mm")
        label(draw, (x + 125, 465), title, 29, NAVY, True, "mm")
        label(draw, (x + 125, 535), note, 22, SLATE, False, "mm")

    rounded(draw, (255, 730, 1345, 830), NAVY, 20)
    label(draw, (800, 780), "禁止捷徑：刪測試／放寬斷言／無條件重試", 29, CYAN, True, "mm")
    save(image, "day20-02-failure-classification.png")


def diagnosis_sequence():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "Codex 診斷順序：先取證，後修改", 54, NAVY, True)
    label(draw, (85, 132), "把修改權暫時拿掉，避免用綠燈掩蓋根因", 31, MUTED)

    steps = [
        (70, "1", "讀失敗摘要", "expected true", RED),
        (455, "2", "建立假設", "時區／測試／相依", ORANGE),
        (840, "3", "固定重現", "UTC 23:00", BLUE),
        (1225, "4", "證據定位", "reportZone 未用", GREEN),
    ]
    for index, (x, code, title, note, color) in enumerate(steps):
        rounded(draw, (x, 275, x + 305, 625), WHITE, 26, color, 5)
        rounded(draw, (x + 105, 315, x + 200, 390), color, 18)
        label(draw, (x + 152, 352), code, 31, WHITE, True, "mm")
        label(draw, (x + 152, 465), title, 29, NAVY, True, "mm")
        label(draw, (x + 152, 535), note, 23, SLATE, False, "mm")
        if index < len(steps) - 1:
            arrow(draw, (x + 315, 450), (x + 370, 450), LINE, 7)

    rounded(draw, (310, 735, 1290, 835), NAVY, 20)
    label(draw, (800, 785), "根因：忽略 reportZone，直接使用 Clock 時區", 29, CYAN, True, "mm")
    save(image, "day20-03-diagnosis-sequence.png")


def timezone_regression():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "同一瞬間，先轉成業務時區再判斷", 52, NAVY, True)
    label(draw, (85, 132), "2026-08-18T23:00:00Z ＝ 臺北次日 07:00", 31, MUTED)

    rounded(draw, (100, 235, 735, 650), WHITE, 28, RED, 5)
    label(draw, (417, 300), "修正前", 37, RED, True, "mm")
    label(draw, (417, 400), "UTC 23:00", 49, NAVY, True, "mm")
    label(draw, (417, 485), "直接與 07:00 比較", 28, SLATE, False, "mm")
    rounded(draw, (250, 550, 585, 610), "#FEE2E2", 16)
    label(draw, (417, 580), "expected true → false", 23, RED, True, "mm")

    arrow(draw, (760, 445), (835, 445), BLUE, 9)

    rounded(draw, (865, 235, 1500, 650), WHITE, 28, GREEN, 5)
    label(draw, (1182, 300), "修正後", 37, GREEN, True, "mm")
    label(draw, (1182, 400), "Asia/Taipei 07:00", 45, NAVY, True, "mm")
    label(draw, (1182, 485), "同一瞬間轉換時區", 28, SLATE, False, "mm")
    rounded(draw, (1015, 550, 1350, 610), "#DCFCE7", 16)
    label(draw, (1182, 580), "準點 true／前後一分 false", 23, GREEN, True, "mm")

    rounded(draw, (275, 745, 1325, 835), NAVY, 18)
    label(draw, (800, 790), "三條邊界：06:59 false／07:00 true／07:01 false", 27, CYAN, True, "mm")
    save(image, "day20-04-timezone-regression.png")


def ci_verification():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "三段證據，不把單次綠燈當完成", 52, WHITE, True)
    label(draw, (85, 132), "先保留失敗，再核對局部測試與乾淨建置", 31, "#CBD5E1")

    checks = [
        (100, "修正前", "1 failure", RED, "FAIL"),
        (575, "局部測試", "3 passed", BLUE, "OK"),
        (1050, "mvn clean test", "BUILD SUCCESS", GREEN, "OK"),
    ]
    for x, title, note, color, status in checks:
        rounded(draw, (x, 280, x + 400, 640), "#111827", 28, color, 5)
        draw.ellipse((x + 145, 330, x + 255, 440), fill=color)
        label(draw, (x + 200, 385), status, 38, WHITE, True, "mm")
        label(draw, (x + 200, 510), title, 30, WHITE, True, "mm")
        label(draw, (x + 200, 575), note, 24, color, True, "mm")

    rounded(draw, (270, 740, 1330, 835), "#1E293B", 18, CYAN, 3)
    label(draw, (800, 787), "尚未證明：正式排程／產製耗時／郵件送達", 28, CYAN, True, "mm")
    save(image, "day20-05-ci-verification.png")


if __name__ == "__main__":
    cover()
    failure_classification()
    diagnosis_sequence()
    timezone_regression()
    ci_verification()
