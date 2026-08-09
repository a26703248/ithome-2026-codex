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
    label(draw, (105, 90), "DAY 22 · 進階整合工作流", 38, "#5EEAD4", True)
    label(draw, (105, 205), "文件與註解自動化", 72, WHITE, True)
    label(draw, (105, 310), "生成文字很快，建立可信文件靠證據", 45, "#CBD5E1", True)

    stages = [
        (105, "來源", BLUE),
        (470, "草稿", PURPLE),
        (835, "驗證", ORANGE),
        (1200, "責任", GREEN),
    ]
    for index, (x, title, color) in enumerate(stages):
        rounded(draw, (x, 565, x + 260, 730), "#111827", 28, color, 5)
        label(draw, (x + 130, 648), title, 37, color, True, "mm")
        if index < len(stages) - 1:
            arrow(draw, (x + 275, 648), (x + 345, 648), "#475569", 7)
    save(image, "day22-01-cover.png")


def source_map():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "文件裡的每一句話，都要能回到來源與驗證", 48, NAVY, True)
    label(draw, (85, 128), "沒有證據的欄位保留未知，不用合理文字填滿", 30, MUTED)

    columns = [85, 490, 875, 1210, 1515]
    headers = ["文件內容", "可信來源", "驗證方式", "狀態"]
    rounded(draw, (85, 205, 1515, 300), NAVY, 18)
    for index, header in enumerate(headers):
        label(draw, ((columns[index] + columns[index + 1]) // 2, 253), header, 27, WHITE, True, "mm")

    rows = [
        ("Java 17", "pom.xml", "mvn clean test", "已驗證", GREEN),
        ("兩階段順序", "程式＋測試", "事件序列", "已驗證", GREEN),
        ("正式啟動參數", "沒有來源", "正式部署設定", "待確認", ORANGE),
        ("週期數值區間", "需求書未定義", "產品決策", "待確認", ORANGE),
    ]
    for row_index, (item, source, check, status, color) in enumerate(rows):
        top = 325 + row_index * 125
        rounded(draw, (85, top, 1515, top + 98), WHITE if row_index % 2 == 0 else "#F1F5F9", 14, LINE, 2)
        values = [item, source, check, status]
        for col_index, value in enumerate(values):
            fill = color if col_index == 3 else NAVY
            label(draw, ((columns[col_index] + columns[col_index + 1]) // 2, top + 49), value, 25, fill, col_index == 3, "mm")

    rounded(draw, (260, 820, 1340, 880), "#FFF7ED", 16, ORANGE, 3)
    label(draw, (800, 850), "待確認不是缺陷；把推測寫成事實才是", 26, ORANGE, True, "mm")
    save(image, "day22-02-source-map.png")


def readme_before_after():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "README 修改前後：從『看似完整』變成『可重現』", 47, NAVY, True)
    label(draw, (85, 125), "新版沒有發明正式啟動方式，而是清楚標出證據邊界", 30, MUTED)

    rounded(draw, (90, 210, 755, 770), WHITE, 28, RED, 5)
    label(draw, (422, 270), "修改前", 36, RED, True, "mm")
    label(draw, (145, 365), "java -jar target/daily-report.jar", 25, NAVY, True)
    label(draw, (145, 418), "--config config/prod.yml", 25, NAVY, True)
    rounded(draw, (135, 500, 710, 575), "#FEF2F2", 14)
    label(draw, (422, 537), "JAR 與設定檔都不存在", 26, RED, True, "mm")
    label(draw, (145, 650), "正式環境設定：沿用舊值", 26, MUTED)
    label(draw, (145, 700), "來源：未標示", 26, MUTED)

    rounded(draw, (845, 210, 1510, 770), WHITE, 28, GREEN, 5)
    label(draw, (1177, 270), "修改後", 36, GREEN, True, "mm")
    label(draw, (900, 365), "mvn clean test", 29, NAVY, True)
    rounded(draw, (890, 420, 1465, 495), "#ECFDF5", 14)
    label(draw, (1177, 457), "2 項測試通過", 27, GREEN, True, "mm")
    label(draw, (900, 575), "正式啟動與部署", 26, NAVY, True)
    rounded(draw, (890, 620, 1465, 695), "#FFF7ED", 14)
    label(draw, (1177, 657), "待正式設定確認", 27, ORANGE, True, "mm")
    save(image, "day22-03-readme-before-after.png")


def command_verification():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "文件裡的命令，也要真的執行", 52, WHITE, True)
    label(draw, (85, 128), "同一份驗證紀錄同時保留失敗證據與成功結果", 30, "#CBD5E1")

    rounded(draw, (90, 225, 1510, 460), "#111827", 26, RED, 4)
    label(draw, (140, 280), "過時 README", 28, RED, True)
    label(draw, (140, 345), "> java -jar target/daily-report.jar", 27, WHITE)
    label(draw, (140, 405), "Error: Unable to access jarfile target/daily-report.jar", 25, RED, True)

    rounded(draw, (90, 520, 1510, 790), "#111827", 26, GREEN, 4)
    label(draw, (140, 575), "更新後 README", 28, GREEN, True)
    label(draw, (140, 640), "> mvn clean test", 27, WHITE)
    label(draw, (140, 700), "Tests run: 2 · Failures: 0 · Errors: 0", 26, CYAN, True)
    label(draw, (140, 738), "BUILD SUCCESS", 31, GREEN, True)
    save(image, "day22-04-command-verification.png")


def comment_comparison():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "我刪掉重述程式碼的註解，只保留理由與限制", 47, NAVY, True)
    label(draw, (85, 125), "程式碼能說明做了什麼；註解補上為什麼這樣安排", 30, MUTED)

    rounded(draw, (90, 220, 755, 690), WHITE, 28, RED, 5)
    label(draw, (422, 280), "冗餘註解", 35, RED, True, "mm")
    label(draw, (145, 390), "// 把報表加入清單", 28, NAVY, True)
    label(draw, (145, 455), "preparedReports.add(", 25, SLATE)
    label(draw, (180, 505), "prepare(customer));", 25, SLATE)
    rounded(draw, (140, 585, 705, 650), "#FEF2F2", 14)
    label(draw, (422, 617), "實作一改，註解也容易過時", 24, RED, True, "mm")

    rounded(draw, (845, 220, 1510, 690), WHITE, 28, GREEN, 5)
    label(draw, (1177, 280), "有效註解", 35, GREEN, True, "mm")
    label(draw, (900, 378), "避免慢速寄信延後", 27, NAVY, True)
    label(draw, (900, 430), "下一份報表的準備", 27, NAVY, True)
    label(draw, (900, 515), "限制：沒有縮短", 27, ORANGE, True)
    label(draw, (900, 567), "郵件總耗時", 27, ORANGE, True)
    rounded(draw, (890, 610, 1465, 660), "#ECFDF5", 14)
    label(draw, (1177, 635), "理由與邊界都有測試證據", 23, GREEN, True, "mm")

    rounded(draw, (245, 770, 1355, 850), NAVY, 18)
    label(draw, (800, 810), "好註解解釋設計理由；測試負責證明它沒有失真", 27, CYAN, True, "mm")
    save(image, "day22-05-comment-comparison.png")


if __name__ == "__main__":
    cover()
    source_map()
    readme_before_after()
    command_verification()
    comment_comparison()
