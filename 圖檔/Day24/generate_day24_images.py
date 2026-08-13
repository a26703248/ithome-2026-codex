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
    draw.ellipse((1260, -190, 1780, 330), fill="#312E81")
    draw.ellipse((-260, 660, 220, 1140), fill="#134E4A")
    label(draw, (105, 90), "DAY 24 · 前人砍樹後人曝曬", 38, "#5EEAD4", True)
    label(draw, (105, 205), "安全與程式碼品質把關", 69, WHITE, True)
    label(draw, (105, 310), "測試通過，只證明你測過的那一部分", 45, "#CBD5E1", True)

    stages = [
        (105, "清單", BLUE),
        (470, "證據", PURPLE),
        (835, "判讀", ORANGE),
        (1200, "決策", GREEN),
    ]
    for index, (x, title, color) in enumerate(stages):
        rounded(draw, (x, 565, x + 260, 730), "#111827", 28, color, 5)
        label(draw, (x + 130, 648), title, 37, color, True, "mm")
        if index < len(stages) - 1:
            arrow(draw, (x + 275, 648), (x + 345, 648), "#475569", 7)
    save(image, "day24-01-cover.png")


def six_layers():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "六層檢查：一個綠燈不能代表整套系統安全", 48, NAVY, True)
    label(draw, (85, 128), "每一層都要留下可重現證據，沒有資料就標成未知", 30, MUTED)

    cards = [
        ("需求與權限", "誰能替哪位客戶建立報表？", BLUE),
        ("程式碼行為", "輸入、例外與失敗路徑", PURPLE),
        ("相依套件", "版本、來源、通知與可達性", ORANGE),
        ("資料與祕密", "信箱、憑證與日誌最小化", RED),
        ("執行環境", "網路、檔案與資源上限", TEAL),
        ("維運與監控", "限流、告警、重試與追蹤", GREEN),
    ]
    for index, (title, detail, color) in enumerate(cards):
        col, row = index % 3, index // 3
        left = 85 + col * 500
        top = 220 + row * 275
        rounded(draw, (left, top, left + 430, top + 205), WHITE, 24, color, 4)
        rounded(draw, (left + 25, top + 28, left + 90, top + 93), color, 18)
        label(draw, (left + 57, top + 60), str(index + 1), 29, WHITE, True, "mm")
        label(draw, (left + 115, top + 55), title, 30, NAVY, True)
        label(draw, (left + 35, top + 135), detail, 24, SLATE)

    rounded(draw, (255, 785, 1345, 855), NAVY, 18)
    label(draw, (800, 820), "掃描器提供線索；清單負責防止視野只剩掃描器", 27, CYAN, True, "mm")
    save(image, "day24-02-six-layers.png")


def code_review():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "Java 修改審查：登入成功，不等於有權操作客戶資料", 47, NAVY, True)
    label(draw, (85, 125), "把授權、輸入限制與日誌內容拆成三個可驗證條件", 30, MUTED)

    rounded(draw, (90, 215, 755, 725), WHITE, 28, RED, 5)
    label(draw, (422, 270), "AI 修改草稿", 35, RED, True, "mm")
    label(draw, (145, 355), "request：帶有 Principal", 27, NAVY, True)
    label(draw, (145, 425), "customerId：直接採用路徑值", 26, SLATE)
    label(draw, (145, 495), "format：任意字串", 26, SLATE)
    label(draw, (145, 565), "log：完整收件信箱", 26, SLATE)
    rounded(draw, (140, 630, 705, 685), "#FEF2F2", 14)
    label(draw, (422, 657), "缺少客戶層級授權", 25, RED, True, "mm")

    rounded(draw, (845, 215, 1510, 725), WHITE, 28, GREEN, 5)
    label(draw, (1177, 270), "修正版", 35, GREEN, True, "mm")
    label(draw, (900, 355), "Principal：只提供請求身分", 27, NAVY, True)
    label(draw, (900, 425), "AccessPolicy：判斷客戶權限", 26, SLATE)
    label(draw, (900, 495), "format 列舉：PDF／WORD／EXCEL", 25, SLATE)
    label(draw, (900, 565), "log：代號、客戶與格式", 26, SLATE)
    rounded(draw, (890, 630, 1465, 685), "#ECFDF5", 14)
    label(draw, (1177, 657), "輸入與權限都有測試", 25, GREEN, True, "mm")

    arrow(draw, (765, 470), (830, 470), ORANGE, 8)
    save(image, "day24-03-code-review.png")


def evidence_matrix():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "安全通知不是結論：版本、觸發條件、呼叫路徑要一起看", 47, WHITE, True)
    label(draw, (85, 125), "Apache PDFBox 2.0.23 的縮小案例判讀", 30, "#CBD5E1")

    columns = [90, 500, 940, 1510]
    headers = ["檢查", "證據", "判斷"]
    rounded(draw, (90, 205, 1510, 295), "#111827", 18, "#475569", 2)
    for index, header in enumerate(headers):
        label(draw, ((columns[index] + columns[index + 1]) // 2, 250), header, 28, WHITE, True, "mm")

    rows = [
        ("版本", "dependency:tree → 2.0.23", "通知命中", ORANGE),
        ("觸發條件", "載入特製 PDF", "官方條件", BLUE),
        ("縮小路徑", "只建立並輸出新 PDF", "未找到載入呼叫", GREEN),
        ("正式系統", "程式與相依清單未提供", "維持待確認", RED),
    ]
    for row_index, (item, evidence, result, color) in enumerate(rows):
        top = 320 + row_index * 112
        rounded(draw, (90, top, 1510, top + 88), "#111827", 14, "#334155", 2)
        values = [item, evidence, result]
        for col_index, value in enumerate(values):
            label(
                draw,
                ((columns[col_index] + columns[col_index + 1]) // 2, top + 44),
                value,
                24,
                color if col_index == 2 else WHITE,
                col_index == 2,
                "mm",
            )

    rounded(draw, (235, 805, 1365, 865), "#172554", 16, BLUE, 3)
    label(draw, (800, 835), "目前路徑未找到觸發點 ≠ 正式系統安全 ≠ 不必升級", 26, CYAN, True, "mm")
    save(image, "day24-04-evidence-matrix.png")


def review_comparison():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (85, 55), "同一份修改，三種檢查看到不同問題", 50, NAVY, True)
    label(draw, (85, 128), "有效發現、脈絡誤報與證據缺口都要保留", 30, MUTED)

    items = [
        (120, "Codex 初篩", "跨客戶授權缺口", "已用 403 測試重現", BLUE),
        (585, "套件通知＋呼叫路徑", "PDFBox 版本命中", "縮小路徑未找到觸發點", ORANGE),
        (1050, "人工六層複核", "日誌洩漏與限流未知", "一項修正、一項待確認", GREEN),
    ]
    for left, title, finding, status, color in items:
        rounded(draw, (left, 235, left + 410, 715), WHITE, 28, color, 5)
        label(draw, (left + 205, 300), title, 29, color, True, "mm")
        rounded(draw, (left + 35, 370, left + 375, 480), "#F1F5F9", 18)
        label(draw, (left + 205, 425), finding, 25, NAVY, True, "mm")
        rounded(draw, (left + 35, 535, left + 375, 645), "#F8FAFC", 18, LINE, 2)
        label(draw, (left + 205, 590), status, 23, SLATE, True, "mm")

    rounded(draw, (250, 790, 1350, 855), NAVY, 18)
    label(draw, (800, 822), "工具找候選問題，人工負責脈絡、取捨與結案", 27, CYAN, True, "mm")
    save(image, "day24-05-review-comparison.png")


if __name__ == "__main__":
    cover()
    six_layers()
    code_review()
    evidence_matrix()
    review_comparison()
