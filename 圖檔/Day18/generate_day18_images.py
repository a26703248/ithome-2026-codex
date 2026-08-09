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
    label(draw, (105, 90), "DAY 18 · 進階整合工作流", 38, "#5EEAD4", True)
    label(draw, (105, 210), "大型重構任務拆解", 72, WHITE, True)
    label(draw, (105, 315), "讓每次改動都能停、能測、能退", 45, "#CBD5E1", True)

    cards = [
        (100, "範圍歸零", "main 零差異", BLUE),
        (485, "行為留證", "08:00／07:59", ORANGE),
        (870, "逐段放行", "局部／完整測試", GREEN),
        (1255, "節點可退", "單獨提交", PURPLE),
    ]
    for x, title, note, color in cards:
        rounded(draw, (x, 570, x + 300, 735), "#1E293B", 24, color, 4)
        label(draw, (x + 150, 620), title, 30, color, True, "mm")
        label(draw, (x + 150, 680), note, 25, WHITE, False, "mm")
    save(image, "day18-01-cover.png")


def coupling_scope():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "runIfScheduled() 集中協調四段流程", 52, NAVY, True)
    label(draw, (85, 132), "T2 與 T3 都會修改這個方法，先後關係不能省", 31, MUTED)

    rounded(draw, (105, 230, 1495, 690), WHITE, 30, RED, 5)
    label(draw, (800, 290), "DailyReportService.runIfScheduled()", 39, RED, True, "mm")
    items = [
        (170, "08:00 觸發", "時間判斷", BLUE),
        (505, "組合數值", "報表內文", TEAL),
        (840, "呼叫 PDF", "取得附件", ORANGE),
        (1175, "交付附件", "郵件元件", PURPLE),
    ]
    for x, title, note, color in items:
        rounded(draw, (x, 390, x + 255, 585), "#F1F5F9", 22, color, 4)
        label(draw, (x + 127, 450), title, 29, color, True, "mm")
        label(draw, (x + 127, 515), note, 25, SLATE, False, "mm")
    rounded(draw, (310, 755, 1290, 835), NAVY, 18)
    label(draw, (800, 795), "先列出可觀察證據，再決定哪一段先移出", 29, CYAN, True, "mm")
    save(image, "day18-02-coupling-scope.png")


def task_map():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "重構任務地圖：每一步都有驗收與停手點", 53, NAVY, True)
    label(draw, (85, 132), "本例共用同一個熱點類別，採循序修改", 31, MUTED)

    tasks = [
        (70, "T1", "留下證據", "2 項測試", BLUE),
        (455, "T2", "抽出排程", "介面不變", ORANGE),
        (840, "T3", "拆內容／傳送", "兩段可測", TEAL),
        (1225, "T4", "格式路由", "先接 PDF", PURPLE),
    ]
    for index, (x, code, title, check, color) in enumerate(tasks):
        rounded(draw, (x, 280, x + 305, 620), WHITE, 26, color, 5)
        rounded(draw, (x + 95, 320, x + 210, 390), color, 18)
        label(draw, (x + 152, 355), code, 30, WHITE, True, "mm")
        label(draw, (x + 152, 455), title, 30, NAVY, True, "mm")
        label(draw, (x + 152, 530), check, 25, SLATE, False, "mm")
        if index < len(tasks) - 1:
            arrow(draw, (x + 315, 450), (x + 370, 450), LINE, 7)
    rounded(draw, (235, 730, 1365, 825), NAVY, 20)
    label(draw, (800, 775), "不是每張任務圖都需要平行；先避開同檔衝突", 28, CYAN, True, "mm")
    save(image, "day18-03-task-map.png")


def first_step_diff():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "T1 邊界：main 雜湊不變，只新增測試證據", 50, WHITE, True)
    label(draw, (85, 132), "任務邊界直接寫進 Codex 提示詞", 31, "#CBD5E1")

    rounded(draw, (100, 230, 750, 680), "#111827", 28, GREEN, 5)
    label(draw, (425, 300), "允許", 38, GREEN, True, "mm")
    allowed = ["新增特徵測試", "記錄測試結果", "回報殘留風險"]
    y = 405
    for item in allowed:
        draw.ellipse((175, y - 10, 197, y + 12), fill=GREEN)
        label(draw, (235, y), item, 30, WHITE, False, "lm")
        y += 90

    rounded(draw, (850, 230, 1500, 680), "#111827", 28, RED, 5)
    label(draw, (1175, 300), "禁止", 38, RED, True, "mm")
    denied = ["修改 src/main", "新增 Word／Excel", "順手搬檔或改名"]
    y = 405
    for item in denied:
        draw.ellipse((925, y - 10, 947, y + 12), fill=RED)
        label(draw, (985, y), item, 30, WHITE, False, "lm")
        y += 90

    rounded(draw, (390, 755, 1210, 835), "#1E293B", 18, CYAN, 3)
    label(draw, (800, 795), "程式差異：測試＋1 檔；正式程式 0 檔", 28, CYAN, True, "mm")
    save(image, "day18-04-first-step-diff.png")


def verification_nodes():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 60), "測試通過只是其中一關，範圍也要核對", 54, NAVY, True)
    label(draw, (85, 132), "每個完成節點，都要能說明、審查與回復", 31, MUTED)

    points = [
        (170, "呼叫證據", "08:00／07:59", BLUE),
        (525, "局部測試", "2 項通過", GREEN),
        (880, "完整測試", "BUILD SUCCESS", TEAL),
        (1235, "範圍核對", "SHA-256 相同", PURPLE),
    ]
    draw.line((200, 465, 1385, 465), fill=LINE, width=10)
    for x, title, note, color in points:
        draw.ellipse((x, 390, x + 150, 540), fill=color)
        label(draw, (x + 75, 465), "通過", 27, WHITE, True, "mm")
        label(draw, (x + 75, 605), title, 28, NAVY, True, "mm")
        label(draw, (x + 75, 660), note, 24, SLATE, False, "mm")
    rounded(draw, (280, 760, 1320, 840), NAVY, 18)
    label(draw, (800, 800), "建立 T1 完成節點後，T2 才取得前置條件", 28, CYAN, True, "mm")
    save(image, "day18-05-verification-nodes.png")


if __name__ == "__main__":
    cover()
    coupling_scope()
    task_map()
    first_step_diff()
    verification_nodes()
