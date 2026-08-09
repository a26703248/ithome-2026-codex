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
    draw.ellipse((1220, -190, 1770, 360), fill="#1E3A8A")
    draw.ellipse((-250, 650, 210, 1110), fill="#134E4A")
    label(draw, (105, 95), "DAY 17 · 進階整合工作流", 38, "#5EEAD4", True)
    label(draw, (105, 220), "ChatGPT ＋ Codex", 75, WHITE, True)
    label(draw, (105, 325), "用任務契約接好規劃與執行", 48, "#CBD5E1", True)

    rounded(draw, (110, 565, 430, 720), "#1E293B", 24, BLUE, 4)
    label(draw, (270, 620), "ChatGPT", 34, BLUE, True, "mm")
    label(draw, (270, 675), "釐清與拆解", 26, WHITE, False, "mm")
    arrow(draw, (440, 642), (610, 642), CYAN, 8)
    rounded(draw, (620, 540, 980, 745), "#1E293B", 24, ORANGE, 4)
    label(draw, (800, 605), "任務契約", 38, ORANGE, True, "mm")
    label(draw, (800, 670), "範圍 · 驗收 · 未知", 26, WHITE, False, "mm")
    arrow(draw, (990, 642), (1160, 642), CYAN, 8)
    rounded(draw, (1170, 565, 1490, 720), "#1E293B", 24, GREEN, 4)
    label(draw, (1330, 620), "Codex", 34, GREEN, True, "mm")
    label(draw, (1330, 675), "修改與驗證", 26, WHITE, False, "mm")
    save(image, "day17-01-cover.png")


def handoff_flow():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 65), "雙工具接力：人是交接點，也是核准點", 56, NAVY, True)
    label(draw, (85, 135), "規劃與執行分工，責任不外包", 31, MUTED)

    cards = [
        (80, "ChatGPT", "找出缺口\n比較切法", BLUE),
        (550, "作者核准", "確認範圍\n保留未知", ORANGE),
        (1020, "Codex", "讀取專案\n修改測試", GREEN),
    ]
    for x, title, note, color in cards:
        rounded(draw, (x, 260, x + 400, 650), WHITE, 28, color, 5)
        label(draw, (x + 200, 350), title, 43, color, True, "mm")
        first, second = note.split("\n")
        label(draw, (x + 200, 465), first, 32, NAVY, True, "mm")
        label(draw, (x + 200, 525), second, 32, SLATE, False, "mm")
    arrow(draw, (490, 455), (535, 455), CYAN, 7)
    arrow(draw, (960, 455), (1005, 455), CYAN, 7)
    rounded(draw, (300, 735, 1300, 820), NAVY, 20)
    label(draw, (800, 777), "交接物：能獨立閱讀、能驗收的任務契約", 31, CYAN, True, "mm")
    save(image, "day17-02-handoff-flow.png")


def requirement_gaps():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 65), "先拆資訊，不急著把需求變成程式碼", 56, NAVY, True)
    label(draw, (85, 135), "同一句需求裡，事實、推測與未知不能混在一起", 31, MUTED)

    columns = [
        (75, "已知事實", ["目前每日 08:00", "現有輸出為 PDF", "三段難以獨立測試"], GREEN),
        (555, "技術推測", ["可能需重做排程", "格式介面可能要抽離", "回歸風險偏高"], ORANGE),
        (1035, "待確認", ["能否訂閱多頻率", "逾時如何處理", "各格式內容是否一致"], RED),
    ]
    for x, title, items, color in columns:
        rounded(draw, (x, 235, x + 410, 700), WHITE, 28, color, 5)
        label(draw, (x + 205, 305), title, 38, color, True, "mm")
        y = 415
        for item in items:
            draw.ellipse((x + 50, y - 8, x + 68, y + 10), fill=color)
            label(draw, (x + 95, y), item, 27, NAVY, False, "lm")
            y += 95
    rounded(draw, (345, 760, 1255, 835), NAVY, 18)
    label(draw, (800, 797), "未知事項留在契約裡，不交給 Codex 猜", 29, CYAN, True, "mm")
    save(image, "day17-03-requirement-gaps.png")


def task_contract():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 65), "任務契約：把能做、不能做、如何驗收寫在一起", 53, WHITE, True)
    label(draw, (85, 135), "本次只新增「發送前一小時」的時間計算", 31, "#CBD5E1")

    fields = [
        ("目標", "輸入指定發送時間，回傳提前一小時", BLUE),
        ("允許", "新增時間計算類別與 JUnit 5 測試", GREEN),
        ("禁止", "不碰既有排程、寄信、PDF 與資料庫", RED),
        ("驗收", "08:00 → 07:00，保留 Asia/Taipei", ORANGE),
        ("回報", "檔案、命令、結果、殘留風險", PURPLE),
    ]
    y = 220
    for title, note, color in fields:
        rounded(draw, (105, y, 1495, y + 100), "#111827", 20, color, 4)
        rounded(draw, (130, y + 18, 335, y + 82), color, 14)
        label(draw, (232, y + 50), title, 29, WHITE, True, "mm")
        label(draw, (390, y + 50), note, 29, WHITE, True, "lm")
        y += 112
    label(draw, (800, 825), "契約不替未知事項補答案", 29, CYAN, True, "mm")
    save(image, "day17-04-task-contract.png")


def verification_map():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 65), "完成不是一句話，而是四段可核對的證據", 55, NAVY, True)
    label(draw, (85, 135), "需求、修改、測試與風險要能互相對映", 31, MUTED)

    rows = [
        ("契約", "提前一小時並保留時區", BLUE, "已確認"),
        ("修改", "ReportProductionWindow", PURPLE, "範圍內"),
        ("測試", "mvn clean test · 2 項通過", GREEN, "有證據"),
        ("未完成", "頻率、格式、寄信整合", ORANGE, "保留風險"),
    ]
    y = 235
    for title, note, color, status in rows:
        rounded(draw, (100, y, 1500, y + 120), WHITE, 22, color, 4)
        rounded(draw, (125, y + 25, 345, y + 95), color, 14)
        label(draw, (235, y + 60), title, 29, WHITE, True, "mm")
        label(draw, (400, y + 60), note, 29, NAVY, True, "lm")
        rounded(draw, (1240, y + 28, 1450, y + 92), "#E2E8F0", 14)
        label(draw, (1345, y + 60), status, 25, SLATE, True, "mm")
        y += 140
    rounded(draw, (345, 805, 1255, 865), NAVY, 16)
    label(draw, (800, 835), "只證明契約內的範圍，不放大成果", 27, CYAN, True, "mm")
    save(image, "day17-05-verification-map.png")


if __name__ == "__main__":
    cover()
    handoff_flow()
    requirement_gaps()
    task_contract()
    verification_map()
