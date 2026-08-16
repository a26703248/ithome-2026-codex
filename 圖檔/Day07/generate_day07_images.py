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
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.ellipse((1010, -160, 1390, 220), fill="#0C4A6E")
    draw.ellipse((-170, 520, 190, 880), fill="#312E81")
    text(draw, (70, 70), "DAY 07 · API 契約", 34, CYAN, True)
    text(draw, (70, 165), "拿到 jobId，", 66, WHITE, True)
    text(draw, (70, 250), "還不算流程完成", 66, WHITE, True)
    text(draw, (70, 342), "把查詢路徑與任務狀態寫進契約", 31, "#CBD5E1")

    cards = [("識別", "jobId", BLUE), ("查詢", "GET /imports/{jobId}", GREEN), ("狀態", "四種結果", ORANGE)]
    x = 70
    for title, note, color in cards:
        rounded(draw, (x, 480, x + 340, 625), WHITE, 24)
        rounded(draw, (x + 24, 510, x + 120, 565), color, 14)
        text(draw, (x + 72, 538), title, 23, WHITE, True, "mm")
        note_size = 17 if "imports" in note else 24
        text(draw, (x + 150, 538), note, note_size, NAVY, True, "lm")
        x += 405
    save(image, "day07-01-cover.png")


def contract_flow():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "從 Day 06 的 jobId 接續查詢契約", 47, NAVY, True)
    text(draw, (64, 108), "決策白名單先固定，ChatGPT 再整理格式", 27, MUTED)
    steps = [
        ("1", "決策清單", "路徑、狀態", TEAL),
        ("2", "ChatGPT", "OpenAPI 草稿", BLUE),
        ("3", "解析器", "路徑與 enum", PURPLE),
        ("4", "JUnit", "GET 與回應", GREEN),
    ]
    for index, (number, title, note, color) in enumerate(steps):
        x = 50 + index * 310
        rounded(draw, (x, 210, x + 250, 445), WHITE, 22, color, 4)
        draw.ellipse((x + 88, 240, x + 162, 314), fill=color)
        text(draw, (x + 125, 278), number, 30, WHITE, True, "mm")
        text(draw, (x + 125, 355), title, 29, NAVY, True, "mm")
        text(draw, (x + 125, 403), note, 21, MUTED, False, "mm")
        if index < 3:
            arrow(draw, (x + 255, 328), (x + 303, 328), CYAN, 7)
    rounded(draw, (160, 525, 1120, 650), NAVY, 22)
    text(draw, (640, 567), "業務欄位都要回指決策來源", 30, CYAN, True, "mm")
    text(draw, (640, 612), "規格必填文字套用固定模板", 25, WHITE, True, "mm")
    save(image, "day07-02-contract-flow.png")


def openapi_focus():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 50), "查詢契約，我先對五個決策", 47, WHITE, True)
    text(draw, (64, 103), "方法、路徑、參數、回應與狀態集合", 27, "#CBD5E1")
    cards = [
        ("GET", "/imports/{jobId}", TEAL),
        ("PARAM", "jobId · uuid", BLUE),
        ("200", "jobId · status", GREEN),
        ("404", "IMPORT_NOT_AVAILABLE", ORANGE),
        ("ENUM", "4 個任務狀態", PURPLE),
    ]
    positions = [(60, 180), (470, 180), (880, 180), (265, 430), (675, 430)]
    for (tag, note, color), (x, y) in zip(cards, positions):
        rounded(draw, (x, y, x + 340, y + 165), WHITE, 22, color, 4)
        rounded(draw, (x + 24, y + 30, x + 145, y + 85), color, 14)
        text(draw, (x + 84, y + 58), tag, 22, WHITE, True, "mm")
        text(draw, (x + 24, y + 125), note, 21, SLATE, True, "lm")
    save(image, "day07-03-openapi-focus.png")


def cross_check():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "同一個查詢，要在三個地方對得上", 47, NAVY, True)
    text(draw, (64, 108), "路徑、回應與狀態集合逐項核對", 27, MUTED)
    columns = [
        ("OpenAPI", ["GET /imports/{jobId}", "200 job state", "404 unavailable"], BLUE),
        ("Controller", ["find(jobId)", "ResponseEntity.ok", "NOT_FOUND"], PURPLE),
        ("JUnit 5", ["規格對映", "控制器 2 案例", "Java 用戶端"], GREEN),
    ]
    for index, (title, lines, color) in enumerate(columns):
        x = 70 + index * 405
        rounded(draw, (x, 175, x + 350, 545), WHITE, 24, color, 4)
        text(draw, (x + 175, 230), title, 31, color, True, "mm")
        draw.line((x + 35, 275, x + 315, 275), fill=color, width=3)
        for row, line in enumerate(lines):
            y = 340 + row * 70
            draw.ellipse((x + 38, y - 9, x + 56, y + 9), fill=color)
            text(draw, (x + 80, y), line, 23, SLATE, True, "lm")
    rounded(draw, (340, 600, 940, 670), GREEN, 18)
    text(draw, (640, 635), "contract → controller → client", 27, WHITE, True, "mm")
    save(image, "day07-04-cross-check.png")


def response_examples():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    text(draw, (64, 55), "狀態不是文字標籤，而是下一個動作", 47, WHITE, True)
    text(draw, (64, 108), "前端依固定集合決定等待、顯示或結束", 27, "#CBD5E1")
    rows = [
        ("PENDING", "等待執行", "保留 jobId，稍後再查詢", BLUE),
        ("RUNNING", "處理中", "顯示進行中，不宣告完成", PURPLE),
        ("SUCCEEDED", "已完成", "停止輪詢；後續位置待確認", GREEN),
        ("FAILED", "執行失敗", "停止輪詢；失敗原因待確認", RED),
    ]
    for index, (status, title, action, color) in enumerate(rows):
        y = 175 + index * 118
        rounded(draw, (80, y, 1200, y + 90), WHITE, 18)
        rounded(draw, (105, y + 18, 265, y + 72), color, 14)
        text(draw, (185, y + 45), status, 22, WHITE, True, "mm")
        text(draw, (310, y + 45), title, 25, NAVY, True, "lm")
        text(draw, (600, y + 45), action, 22, SLATE, False, "lm")
    save(image, "day07-05-response-examples.png")


if __name__ == "__main__":
    cover()
    contract_flow()
    openapi_focus()
    cross_check()
    response_examples()
