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


def arrow(draw, start, end, color=CYAN, width=7):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        direction = 1 if ex > sx else -1
        points = [(ex, ey), (ex - direction * 18, ey - 12), (ex - direction * 18, ey + 12)]
    else:
        direction = 1 if ey > sy else -1
        points = [(ex, ey), (ex - 12, ey - direction * 18), (ex + 12, ey - direction * 18)]
    draw.polygon(points, fill=color)


def multiline(draw, center_x, start_y, lines, size, fill, gap=38, bold=False):
    for index, line in enumerate(lines):
        text(draw, (center_x, start_y + index * gap), line, size, fill, bold, "mm")


def save(image, name):
    image.save(ROOT / name, format="PNG", optimize=True)


def cover():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    d.ellipse((1020, -140, 1380, 220), fill="#0C4A6E")
    d.ellipse((-170, 520, 190, 880), fill="#172554")
    text(d, (70, 70), "DAY 05 · 系統設計", 34, CYAN, True)
    text(d, (70, 165), "先比較代價，", 66, WHITE, True)
    text(d, (70, 250), "再決定架構", 66, WHITE, True)
    text(d, (70, 342), "ChatGPT 攤開選項，人承擔取捨", 31, "#CBD5E1")

    cards = [("1", "事實", TEAL), ("2", "方案", BLUE), ("3", "證據", ORANGE)]
    x = 82
    for number, label, color in cards:
        rounded(d, (x, 490, x + 300, 625), WHITE, 25)
        d.ellipse((x + 28, 526, x + 80, 578), fill=color)
        text(d, (x + 54, 553), number, 24, WHITE, True, "mm")
        text(d, (x + 105, 555), label, 38, NAVY, True, "lm")
        x += 405
    save(im, "day05-01-cover.png")


def constraints():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "設計前，先分開輸入與未知", 47, NAVY, True)
    text(d, (64, 108), "數字是輸入；限制位置與驗收門檻仍要查證", 27, MUTED)

    cards = [
        ("每日資料量", "約 1 TB", TEAL, "本輪輸入"),
        ("來源速率", "約 12 MB/s", BLUE, "本輪輸入"),
        ("純傳輸時間", "> 23 小時", ORANGE, "條件式推論"),
        ("瓶頸位置", "尚未確認", RED, "待測量"),
    ]
    for i, (title, value, color, tag) in enumerate(cards):
        x = 64 + i * 291
        rounded(d, (x, 175, x + 260, 455), WHITE, 24, color, 4)
        rounded(d, (x + 24, 202, x + 135, 242), color, 12)
        text(d, (x + 79, 223), tag, 18, WHITE, True, "mm")
        text(d, (x + 130, 302), title, 25, SLATE, True, "mm")
        text(d, (x + 130, 367), value, 35, color, True, "mm")
        text(d, (x + 130, 414), "→ 決定下一個實驗", 18, MUTED, False, "mm")

    rounded(d, (135, 525, 1145, 640), NAVY, 22)
    text(d, (640, 563), "未知：批次大小｜尖峰流量｜可接受完成時間｜團隊維運能力", 25, WHITE, True, "mm")
    text(d, (640, 607), "沒有這些證據，就不能把推論寫成架構事實", 23, CYAN, True, "mm")
    save(im, "day05-02-constraints.png")


def options():
    im = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "三個候選方案，用同一把尺比較", 47, WHITE, True)
    text(d, (64, 108), "責任邊界越多，部署與故障處理成本也會增加", 27, "#CBD5E1")
    cards = [
        ("A", "同步單體", ["HTTP 請求", "匯入處理", "工作區"], TEAL),
        ("B", "模組化單體＋非同步任務", ["匯入介面", "任務表／背景工作元件", "工作區"], ORANGE),
        ("C", "獨立匯入服務＋訊息代理", ["匯入服務", "訊息代理", "既有工作區"], BLUE),
    ]
    for i, (tag, title, items, color) in enumerate(cards):
        x = 64 + i * 405
        rounded(d, (x, 175, x + 360, 555), WHITE, 25, color, 4)
        d.ellipse((x + 142, 200, x + 218, 276), fill=color)
        text(d, (x + 180, 239), tag, 32, WHITE, True, "mm")
        title_size = 24 if i > 0 else 29
        text(d, (x + 180, 320), title, title_size, NAVY, True, "mm")
        for idx, item in enumerate(items):
            y = 372 + idx * 57
            rounded(d, (x + 42, y, x + 318, y + 42), "#E2E8F0", 12)
            text(d, (x + 180, y + 22), item, 20, SLATE, idx == 1, "mm")
    rounded(d, (185, 600, 1095, 660), "#164E63", 16)
    text(d, (640, 631), "候選方案不是排名；關鍵是什麼證據會改變選擇", 25, WHITE, True, "mm")
    save(im, "day05-03-options.png")


def selected_flow():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "第一版：模組化單體＋非同步任務", 47, NAVY, True)
    text(d, (64, 108), "先切開執行責任，不急著切開部署邊界", 27, MUTED)

    nodes = [
        (65, "手動／排程", TEAL),
        (300, "匯入 API", BLUE),
        (535, "任務表", ORANGE),
        (770, "背景工作元件", BLUE),
        (1005, "工作區", GREEN),
    ]
    for x, label, color in nodes:
        rounded(d, (x, 245, x + 190, 365), WHITE, 22, color, 4)
        text(d, (x + 95, 307), label, 25, NAVY, True, "mm")
    for x in [255, 490, 725, 960]:
        arrow(d, (x, 305), (x + 38, 305), CYAN, 7)

    rounded(d, (165, 445, 1115, 610), NAVY, 22)
    text(d, (640, 486), "共同規則", 28, CYAN, True, "mm")
    multiline(d, 640, 532, ["租戶隔離　｜　任務狀態　｜　冪等鍵　｜　重試與告警", "介面保留未來拆分空間，但第一版仍是單一部署"], 23, WHITE, 40)
    save(im, "day05-04-selected-flow.png")


def decision_record():
    im = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    d = ImageDraw.Draw(im)
    text(d, (64, 55), "決策完成後，留下驗證門檻", 47, NAVY, True)
    text(d, (64, 108), "架構決策紀錄要能回答：現在選什麼、延後什麼、何時重看", 27, MUTED)
    cards = [
        ("現在採用", ["單一部署", "非同步任務", "共同匯入規則"], GREEN, "#F0FDF4"),
        ("暫緩加入", ["訊息代理", "獨立匯入服務", "多套部署流程"], ORANGE, "#FFF7ED"),
        ("觸發重評", ["背景工作元件追不上來源", "前台延遲惡化", "故障無法隔離"], BLUE, "#EFF6FF"),
    ]
    for i, (title, items, color, bg) in enumerate(cards):
        x = 64 + i * 405
        rounded(d, (x, 175, x + 360, 540), bg, 24, color, 4)
        text(d, (x + 180, 230), title, 32, color, True, "mm")
        d.line((x + 40, 270, x + 320, 270), fill=color, width=3)
        for idx, item in enumerate(items):
            y = 324 + idx * 72
            d.ellipse((x + 45, y - 12, x + 69, y + 12), fill=color)
            d.ellipse((x + 53, y - 4, x + 61, y + 4), fill=WHITE)
            text(d, (x + 90, y), item, 23, SLATE, True, "lm")
    rounded(d, (180, 590, 1100, 660), NAVY, 18)
    text(d, (640, 626), "壓測、故障注入與租戶隔離測試，才是升級架構的證據", 24, WHITE, True, "mm")
    save(im, "day05-05-decision-record.png")


if __name__ == "__main__":
    cover()
    constraints()
    options()
    selected_flow()
    decision_record()
