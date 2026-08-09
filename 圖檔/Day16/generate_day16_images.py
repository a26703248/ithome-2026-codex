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
    draw.polygon([(ex, ey), (ex - 20, ey - 14), (ex - 20, ey + 14)], fill=color)


def save(image, name):
    image.save(ROOT / name, format="PNG", optimize=True)


def cover():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.ellipse((1210, -180, 1770, 380), fill="#1E3A8A")
    draw.ellipse((-240, 640, 220, 1100), fill="#134E4A")
    label(draw, (110, 100), "DAY 16 · Codex 基礎入門", 38, "#5EEAD4", True)
    label(draw, (110, 225), "把修改整理成可審查的交付", 70, WHITE, True)
    label(draw, (110, 325), "分支、差異、測試、commit 與 PR 草稿", 39, "#CBD5E1")

    steps = [("BRANCH", BLUE), ("DIFF", PURPLE), ("TEST", ORANGE), ("COMMIT", TEAL), ("DRAFT PR", GREEN)]
    x = 95
    for index, (text, color) in enumerate(steps):
        rounded(draw, (x, 570, x + 245, 705), "#1E293B", 22, color, 4)
        label(draw, (x + 122, 637), text, 27, color, True, "mm")
        if index < len(steps) - 1:
            arrow(draw, (x + 250, 637), (x + 290, 637), CYAN, 6)
        x += 300
    save(image, "day16-01-cover.png")


def evidence_chain():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 70), "Git 證據鏈：每一步都要能回答一個問題", 55, NAVY, True)
    label(draw, (90, 138), "工具可以前進，範圍與驗收仍由人確認", 31, MUTED)

    steps = [
        ("01", "確認起點", "原有修改是誰的？", BLUE),
        ("02", "任務分支", "從哪個基底開始？", PURPLE),
        ("03", "最小 diff", "實際改了什麼？", ORANGE),
        ("04", "測試紀錄", "驗證涵蓋什麼？", TEAL),
        ("05", "commit", "這次意圖是什麼？", GREEN),
        ("06", "PR 草稿", "風險與缺口在哪？", RED),
    ]
    x = 55
    for index, (number, title, note, color) in enumerate(steps):
        rounded(draw, (x, 270, x + 220, 630), WHITE, 24, color, 5)
        label(draw, (x + 110, 325), number, 27, color, True, "mm")
        label(draw, (x + 110, 420), title, 31, NAVY, True, "mm")
        label(draw, (x + 110, 510), note, 22, SLATE, False, "mm")
        if index < len(steps) - 1:
            arrow(draw, (x + 223, 450), (x + 260, 450), CYAN, 6)
        x += 255

    rounded(draw, (280, 725, 1320, 815), NAVY, 20)
    label(draw, (800, 770), "分支保存範圍；測試與審查保存判斷", 30, CYAN, True, "mm")
    save(image, "day16-02-evidence-chain.png")


def scoped_diff():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 72), "提交前，只讓本任務進入暫存區", 56, WHITE, True)
    label(draw, (90, 142), "先看 diff，再列出檔案；不用 git add .", 31, "#CBD5E1")

    rounded(draw, (95, 235, 1505, 690), "#111827", 24, "#475569", 3)
    label(draw, (145, 290), "git diff --cached --stat", 28, CYAN, True)
    label(draw, (145, 355), "ReportRangeService.java", 28, WHITE, True)
    label(draw, (915, 355), "1 +  1 -", 28, ORANGE, True)
    label(draw, (145, 420), "ReportRangeServiceTest.java", 28, WHITE, True)
    label(draw, (915, 420), "8 +  0 -", 28, GREEN, True)
    draw.line((145, 470, 1455, 470), fill="#334155", width=3)
    label(draw, (145, 530), "- !endDate.isAfter(startDate)", 28, RED)
    label(draw, (145, 585), "+ endDate.isBefore(startDate)", 28, GREEN)

    rounded(draw, (340, 745, 1260, 825), TEAL, 18)
    label(draw, (800, 785), "兩個檔案 · 一個意圖 · 可重現測試", 30, WHITE, True, "mm")
    save(image, "day16-03-scoped-diff.png")


def dirty_worktree():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 70), "工作目錄不乾淨時，先分清楚擁有者", 55, NAVY, True)
    label(draw, (90, 138), "保留既有修改，只挑選本任務的檔案", 31, MUTED)

    rounded(draw, (90, 230, 745, 690), WHITE, 28, ORANGE, 5)
    label(draw, (417, 290), "既有修改", 38, ORANGE, True, "mm")
    rounded(draw, (155, 375, 680, 495), "#FFF7ED", 18)
    label(draw, (205, 435), "README.md", 31, NAVY, True, "lm")
    label(draw, (620, 435), "保留", 27, ORANGE, True, "rm")
    label(draw, (417, 585), "不 reset · 不 restore · 不 stash", 25, SLATE, False, "mm")

    rounded(draw, (855, 230, 1510, 690), WHITE, 28, GREEN, 5)
    label(draw, (1182, 290), "本任務修改", 38, GREEN, True, "mm")
    rounded(draw, (920, 360, 1445, 455), "#F0FDF4", 18)
    label(draw, (970, 407), "ReportRangeService.java", 27, NAVY, True, "lm")
    rounded(draw, (920, 485, 1445, 580), "#F0FDF4", 18)
    label(draw, (970, 532), "ReportRangeServiceTest.java", 27, NAVY, True, "lm")
    label(draw, (1182, 635), "明確列名後暫存", 26, GREEN, True, "mm")

    rounded(draw, (330, 750, 1270, 830), NAVY, 18)
    label(draw, (800, 790), "同一檔案出現不明修改，就停下來確認", 29, CYAN, True, "mm")
    save(image, "day16-04-dirty-worktree.png")


def pr_draft():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 68), "PR 草稿不是完成摘要，是審查入口", 56, NAVY, True)
    label(draw, (90, 138), "審查者應能從同一頁重建判斷過程", 31, MUTED)

    fields = [
        ("問題", "同日起訖被判定為非法", RED),
        ("修改", "條件收斂＋新增回歸測試", BLUE),
        ("驗證", "mvn clean test · 5 項通過", GREEN),
        ("風險", "尚未執行網頁與資料庫測試", ORANGE),
        ("未完成", "待維護者審查與合併", PURPLE),
    ]
    y = 220
    for title, note, color in fields:
        rounded(draw, (120, y, 1480, y + 90), WHITE, 18, color, 4)
        rounded(draw, (145, y + 15, 335, y + 75), color, 14)
        label(draw, (240, y + 45), title, 27, WHITE, True, "mm")
        label(draw, (390, y + 45), note, 29, NAVY, True, "lm")
        y += 105

    rounded(draw, (330, 775, 1270, 850), NAVY, 18)
    label(draw, (800, 812), "先完成審查材料，再決定是否推送與建立 PR", 28, CYAN, True, "mm")
    save(image, "day16-05-pr-draft.png")


if __name__ == "__main__":
    cover()
    evidence_chain()
    scoped_diff()
    dirty_worktree()
    pr_draft()
