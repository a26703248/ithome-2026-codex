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
    label(draw, (115, 105), "DAY 14 · CODEX 基礎入門", 38, "#5EEAD4", True)
    label(draw, (115, 235), "測試通過，還缺什麼？", 78, WHITE, True)
    label(draw, (115, 335), "從完成摘要回到可驗證證據", 42, "#CBD5E1")

    cards = [
        ("COMMAND", "命令與目錄", BLUE),
        ("TEST", "數量與狀態", RED),
        ("DIFF", "修改與邊界", PURPLE),
        ("DECISION", "完成或受阻", GREEN),
    ]
    x = 90
    for tag, note, color in cards:
        rounded(draw, (x, 555, x + 330, 725), "#1E293B", 24, color, 4)
        label(draw, (x + 165, 615), tag, 27, color, True, "mm")
        label(draw, (x + 165, 675), note, 28, WHITE, True, "mm")
        x += 370
    save(image, "day14-01-cover.png")


def four_layers():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 78), "四層驗證，各自回答不同風險", 58, NAVY, True)
    label(draw, (90, 148), "只有完整串起來，完成摘要才有可追溯性", 31, MUTED)

    layers = [
        ("1", "重現測試", "舊程式確實出錯", RED),
        ("2", "局部測試", "直接行為已修正", ORANGE),
        ("3", "完整測試", "既有單元測試未發現回歸", BLUE),
        ("4", "人工檢查", "diff 與需求邊界一致", GREEN),
    ]
    y = 250
    for index, (number, title, note, color) in enumerate(layers):
        x = 115 + index * 370
        rounded(draw, (x, y, x + 315, y + 390), WHITE, 28, color, 5)
        draw.ellipse((x + 112, y + 42, x + 202, y + 132), fill=color)
        label(draw, (x + 157, y + 87), number, 34, WHITE, True, "mm")
        label(draw, (x + 157, y + 205), title, 34, NAVY, True, "mm")
        label(draw, (x + 157, y + 285), note, 25, color, True, "mm")
        if index < len(layers) - 1:
            arrow(draw, (x + 320, y + 195), (x + 355, y + 195), CYAN, 6)
    rounded(draw, (320, 720, 1280, 805), NAVY, 20)
    label(draw, (800, 762), "紅燈證明抓對問題；綠燈證明修改後仍符合檢查", 29, CYAN, True, "mm")
    save(image, "day14-02-four-layers.png")


def read_output():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 78), "工作紀錄要逐段讀，不只找綠色結尾", 56, WHITE, True)
    label(draw, (90, 145), "先確認 JUnit 真的啟動，再判斷程式結果", 30, "#CBD5E1")

    rows = [
        ("01", "工作目錄", "程式碼/DAY13/reproduction/", BLUE),
        ("02", "完整命令", "mvn -Dtest=ReportRangeServiceTest test", PURPLE),
        ("03", "測試執行鏈", "Surefire Plugin → JUnit Platform", ORANGE),
        ("04", "結果摘要", "5 項測試 · 0 項失敗 · 1 項錯誤 · 0 項略過", RED),
        ("05", "結束碼", "1 · BUILD FAILURE", RED),
    ]
    y = 230
    for number, title, value, color in rows:
        rounded(draw, (105, y, 1495, y + 105), "#1E293B", 20, color, 4)
        rounded(draw, (135, y + 23, 230, y + 82), color, 14)
        label(draw, (182, y + 52), number, 25, WHITE, True, "mm")
        label(draw, (280, y + 52), title, 27, WHITE, True, "lm")
        label(draw, (565, y + 52), value, 27, "#CBD5E1", True, "lm")
        y += 120
    label(draw, (800, 860), "下載中止 → JUnit 未啟動 → 環境阻擋", 22, ORANGE, True, "mm")
    save(image, "day14-03-read-output.png")


def diff_review():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 78), "測試通過後，仍要人工檢查 diff", 58, NAVY, True)
    label(draw, (90, 148), "確認改了什麼，也確認哪些邊界沒有被動到", 31, MUTED)

    rounded(draw, (90, 235, 760, 665), WHITE, 28, BLUE, 5)
    label(draw, (135, 285), "程式碼修改", 34, BLUE, True)
    rounded(draw, (135, 365, 715, 535), "#EFF6FF", 20)
    label(draw, (175, 415), "- !endDate.isAfter(startDate)", 25, RED, True)
    label(draw, (175, 485), "+ endDate.isBefore(startDate)", 25, GREEN, True)
    label(draw, (425, 605), "一個條件判斷", 28, NAVY, True, "mm")

    rounded(draw, (840, 235, 1510, 665), WHITE, 28, PURPLE, 5)
    label(draw, (885, 285), "測試與邊界", 34, PURPLE, True)
    checks = [
        ("＋ 同日起訖回傳 1", GREEN),
        ("＝ 公開方法簽章", BLUE),
        ("＝ pom.xml 與相依套件", BLUE),
        ("＝ 四項既有測試", BLUE),
    ]
    y = 385
    for value, color in checks:
        label(draw, (900, y), value, 27, color, True)
        y += 67
    rounded(draw, (280, 730, 1320, 815), NAVY, 20)
    label(draw, (800, 772), "測試回答行為；diff 回答修改範圍", 31, CYAN, True, "mm")
    save(image, "day14-04-diff-review.png")


def acceptance():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 75), "不要只報完成，要逐項對上證據", 58, NAVY, True)
    label(draw, (90, 145), "技術子任務完成，不等於原始使用者流程已驗收", 31, MUTED)

    headers = [(95, "驗收條件"), (600, "證據"), (1190, "狀態")]
    rounded(draw, (75, 225, 1525, 315), NAVY, 18)
    for x, value in headers:
        label(draw, (x, 270), value, 28, WHITE, True, "lm")

    rows = [
        ("同日起訖回傳 1", "先錯 1 項，修正後 5 項通過", "完成", GREEN),
        ("公開方法簽章與建置設定不變", "原始碼 diff；方法簽章及 pom.xml 未變", "完成", GREEN),
        ("網頁可產出單日報表", "未跑網頁、資料庫、端對端測試", "未驗證", ORANGE),
    ]
    y = 335
    for condition, evidence, status, color in rows:
        rounded(draw, (75, y, 1525, y + 135), WHITE, 15, "#CBD5E1", 2)
        label(draw, (95, y + 67), condition, 27, NAVY, True, "lm")
        label(draw, (600, y + 67), evidence, 25, SLATE, False, "lm")
        rounded(draw, (1180, y + 35, 1465, y + 100), color, 16)
        label(draw, (1322, y + 67), status, 28, WHITE, True, "mm")
        y += 155
    rounded(draw, (350, 815, 1250, 875), NAVY, 16)
    label(draw, (800, 845), "完成、部分完成與未驗證，要由證據決定", 27, CYAN, True, "mm")
    save(image, "day14-05-acceptance.png")


if __name__ == "__main__":
    cover()
    four_layers()
    read_output()
    diff_review()
    acceptance()
