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
    draw.ellipse((1240, -190, 1770, 340), fill="#134E4A")
    draw.ellipse((-240, 640, 200, 1080), fill="#1E3A8A")
    label(draw, (115, 105), "DAY 13 · CODEX 基礎入門", 38, "#5EEAD4", True)
    label(draw, (115, 235), "第一個 Codex 任務實戰", 78, WHITE, True)
    label(draw, (115, 330), "從模糊 issue，走到可驗證修正", 42, "#CBD5E1")

    cards = [
        ("ISSUE", "補齊條件", RED),
        ("TEST", "重現邊界", ORANGE),
        ("PATCH", "最小修正", BLUE),
        ("REPORT", "留下風險", GREEN),
    ]
    x = 115
    for tag, note, color in cards:
        rounded(draw, (x, 540, x + 310, 710), "#1E293B", 24, color, 4)
        label(draw, (x + 155, 600), tag, 29, color, True, "mm")
        label(draw, (x + 155, 662), note, 29, WHITE, True, "mm")
        x += 350
    save(image, "day13-01-cover.png")


def issue_gaps():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (95, 90), "一張 issue，還不是可執行任務", 58, NAVY, True)
    label(draw, (95, 155), "客服描述只有現象，還無法寫成會失敗的測試", 31, MUTED)

    rounded(draw, (90, 245, 650, 730), WHITE, 30, RED, 5)
    label(draw, (130, 300), "原始問題單", 34, RED, True)
    rounded(draw, (130, 370, 610, 610), "#FEF2F2", 22)
    label(draw, (170, 425), "「起點和終點同一天，", 34, NAVY, True)
    label(draw, (170, 485), "報表會失敗，", 34, NAVY, True)
    label(draw, (170, 545), "請協助修正。」", 34, NAVY, True)
    label(draw, (370, 675), "還缺能重跑的條件", 27, RED, True, "mm")

    arrow(draw, (685, 485), (780, 485), RED, 9)
    label(draw, (1130, 245), "交付前要補齊", 35, NAVY, True, "mm")
    gaps = [
        ("確切輸入", BLUE), ("錯誤訊息", RED), ("正常結果", GREEN),
        ("可改檔案", PURPLE), ("通過命令", ORANGE),
    ]
    y = 315
    for text, color in gaps:
        rounded(draw, (800, y, 1460, y + 82), WHITE, 18, color, 4)
        draw.ellipse((835, y + 19, 879, y + 63), fill=color)
        label(draw, (857, y + 42), "?", 22, WHITE, True, "mm")
        label(draw, (920, y + 41), text, 29, NAVY, True, "lm")
        y += 100
    save(image, "day13-02-issue-gaps.png")


def task_contract():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (95, 82), "把問題單補成能重跑的修正說明", 58, WHITE, True)
    label(draw, (95, 150), "每一欄都對應本次日期邊界與實際命令", 31, "#CBD5E1")

    rows = [
        ("呼叫", "2026-08-19 至 2026-08-19", "拋出 IllegalArgumentException", RED),
        ("結果", "同日起訖是一日範圍", "回傳 1", GREEN),
        ("可改", "ReportRangeService ＋ 1 項測試", "不改公開介面與 pom.xml", BLUE),
        ("驗收", "先失敗，再完整測試", "mvn clean test", ORANGE),
    ]
    y = 245
    for title, left, right, color in rows:
        rounded(draw, (95, y, 1505, y + 125), "#1E293B", 22, color, 4)
        rounded(draw, (125, y + 28, 295, y + 97), color, 16)
        label(draw, (210, y + 62), title, 29, WHITE, True, "mm")
        label(draw, (345, y + 62), left, 29, WHITE, True, "lm")
        arrow(draw, (900, y + 63), (995, y + 63), "#64748B", 6)
        label(draw, (1040, y + 62), right, 27, "#CBD5E1", True, "lm")
        y += 145
    save(image, "day13-03-task-contract.png")


def work_log():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 82), "先重現，再修正：一條可核對的證據鏈", 56, NAVY, True)
    label(draw, (85, 148), "相同缺陷要能由測試從紅燈推進到綠燈", 31, MUTED)

    events = [
        ("1", "基線", "4 項通過", BLUE),
        ("2", "回歸測試", "5 項／1 錯誤", RED),
        ("3", "定位", "!isAfter", PURPLE),
        ("4", "最小修正", "改用 isBefore", ORANGE),
        ("5", "完整驗證", "5 項全通過", GREEN),
    ]
    x = 60
    for index, (number, title, note, color) in enumerate(events):
        rounded(draw, (x, 285, x + 270, 615), WHITE, 25, color, 5)
        draw.ellipse((x + 95, 325, x + 175, 405), fill=color)
        label(draw, (x + 135, 365), number, 31, WHITE, True, "mm")
        label(draw, (x + 135, 475), title, 30, NAVY, True, "mm")
        label(draw, (x + 135, 545), note, 24, color, True, "mm")
        if index < len(events) - 1:
            arrow(draw, (x + 275, 450), (x + 310, 450), CYAN, 6)
        x += 315
    rounded(draw, (280, 705, 1320, 795), NAVY, 20)
    label(draw, (800, 750), "指定測試確認邊界；完整測試檢查既有行為", 30, CYAN, True, "mm")
    save(image, "day13-04-work-log.png")


def completion_report():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 82), "我用五個問題讀完成回報", 54, NAVY, True)
    label(draw, (90, 148), "問題都能指回程式碼、命令或尚未執行的檢查", 30, MUTED)

    rows = [
        ("哪裡判錯？", "日期相等被誤判成迄日較早", RED),
        ("改了哪裡？", "一個條件判斷與一項新測試", BLUE),
        ("跑了什麼？", "指定測試先錯 1 項；完整測試 5 項通過", GREEN),
        ("哪些沒跑？", "網頁、資料庫與端對端報表", ORANGE),
        ("還要確認？", "單日報表的實際輸出內容", PURPLE),
    ]
    y = 235
    for title, value, color in rows:
        rounded(draw, (105, y, 1495, y + 105), WHITE, 20, color, 4)
        rounded(draw, (135, y + 23, 365, y + 82), color, 14)
        label(draw, (250, y + 52), title, 27, WHITE, True, "mm")
        label(draw, (420, y + 52), value, 28, NAVY, True, "lm")
        y += 120
    save(image, "day13-05-completion-report.png")


if __name__ == "__main__":
    cover()
    issue_gaps()
    task_contract()
    work_log()
    completion_report()
