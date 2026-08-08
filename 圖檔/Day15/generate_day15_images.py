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
    draw.ellipse((1220, -180, 1760, 360), fill="#1E3A8A")
    draw.ellipse((-220, 635, 220, 1075), fill="#134E4A")
    label(draw, (115, 105), "DAY 15 · CODEX 基礎入門", 38, "#5EEAD4", True)
    label(draw, (115, 235), "核准前，先看懂邊界", 78, WHITE, True)
    label(draw, (115, 340), "權限不是開或關，而是目的、範圍與後果", 40, "#CBD5E1")

    cards = [
        ("PURPOSE", "為了哪項驗收", BLUE),
        ("SCOPE", "會碰哪些資源", PURPLE),
        ("IMPACT", "最壞影響範圍", ORANGE),
    ]
    x = 150
    for tag, note, color in cards:
        rounded(draw, (x, 565, x + 390, 735), "#1E293B", 24, color, 4)
        label(draw, (x + 195, 620), tag, 27, color, True, "mm")
        label(draw, (x + 195, 685), note, 29, WHITE, True, "mm")
        x += 455
    save(image, "day15-01-cover.png")


def two_layers():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 78), "兩道門，處理兩種問題", 58, NAVY, True)
    label(draw, (90, 148), "沙箱限制能力；核准政策決定何時停下來問", 31, MUTED)

    rounded(draw, (120, 245, 735, 655), WHITE, 30, BLUE, 6)
    label(draw, (427, 320), "SANDBOX", 32, BLUE, True, "mm")
    label(draw, (427, 390), "沙箱", 50, NAVY, True, "mm")
    label(draw, (427, 485), "可寫哪些路徑", 30, SLATE, True, "mm")
    label(draw, (427, 545), "命令能否連網", 30, SLATE, True, "mm")

    rounded(draw, (865, 245, 1480, 655), WHITE, 30, PURPLE, 6)
    label(draw, (1172, 320), "APPROVAL", 32, PURPLE, True, "mm")
    label(draw, (1172, 390), "核准政策", 50, NAVY, True, "mm")
    label(draw, (1172, 485), "何時必須暫停", 30, SLATE, True, "mm")
    label(draw, (1172, 545), "由誰確認越界", 30, SLATE, True, "mm")

    arrow(draw, (742, 450), (850, 450), CYAN, 8)
    rounded(draw, (300, 735, 1300, 825), NAVY, 20)
    label(draw, (800, 780), "邊界內可自動前進；越界時回到人工判斷", 30, CYAN, True, "mm")
    save(image, "day15-02-two-layers.png")


def permission_surfaces():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 72), "不要把所有能力包成一個「允許」", 56, NAVY, True)
    label(draw, (90, 140), "每個面向都要對上任務的實際需要", 31, MUTED)

    items = [
        ("READ", "讀取檔案", "專案範圍", BLUE),
        ("WRITE", "修改檔案", "工作區內", PURPLE),
        ("EXEC", "執行指令", "指定命令", ORANGE),
        ("NET", "網路存取", "必要網域", TEAL),
        ("SECRET", "使用憑證", "本次不需", RED),
    ]
    x = 70
    for tag, title, scope, color in items:
        rounded(draw, (x, 245, x + 275, 665), WHITE, 26, color, 5)
        draw.ellipse((x + 88, 290, x + 187, 389), fill=color)
        label(draw, (x + 137, 339), tag, 21, WHITE, True, "mm")
        label(draw, (x + 137, 470), title, 30, NAVY, True, "mm")
        rounded(draw, (x + 35, 540, x + 240, 605), "#F1F5F9", 15)
        label(draw, (x + 137, 572), scope, 25, color, True, "mm")
        x += 310

    rounded(draw, (300, 735, 1300, 825), NAVY, 20)
    label(draw, (800, 780), "能力與任務相稱，才是最小權限", 31, CYAN, True, "mm")
    save(image, "day15-03-permission-surfaces.png")


def three_decisions():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 75), "三種操作，答案可以完全不同", 56, WHITE, True)
    label(draw, (90, 145), "先看目的、資源與替代方案，再判斷是否核准", 31, "#CBD5E1")

    cards = [
        ("只讀取 diff", "無網路 · 不改檔", "放行", GREEN),
        ("Maven 下載外掛", "核對來源 · 限縮連線", "縮小", ORANGE),
        ("外部要求部署", "超出驗收 · 還會上傳成品", "拒絕", RED),
    ]
    x = 95
    for title, reason, decision, color in cards:
        rounded(draw, (x, 245, x + 440, 690), "#1E293B", 28, color, 5)
        label(draw, (x + 220, 335), title, 35, WHITE, True, "mm")
        label(draw, (x + 220, 435), reason, 27, "#CBD5E1", True, "mm")
        rounded(draw, (x + 95, 535, x + 345, 625), color, 20)
        label(draw, (x + 220, 580), decision, 36, WHITE, True, "mm")
        x += 485

    label(draw, (800, 790), "核准具體動作，不核准模糊的善意", 29, CYAN, True, "mm")
    save(image, "day15-04-three-decisions.png")


def untrusted_input():
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    label(draw, (90, 72), "文件把測試任務推向部署時", 58, NAVY, True)
    label(draw, (90, 140), "外部說明先當證據，不直接當成操作命令", 31, MUTED)

    steps = [
        ("1", "辨識任務漂移", "原本只跑單元測試，內容卻要求部署", RED),
        ("2", "停在差異檢查", "不新增套件庫，也不執行 deploy", ORANGE),
        ("3", "核對交付範圍", "使用者任務、AGENTS.md、驗收條件", BLUE),
        ("4", "索取安全重現", "要求不含憑證的最小重現專案", GREEN),
    ]
    y = 230
    for index, (number, title, note, color) in enumerate(steps):
        rounded(draw, (110, y, 1490, y + 115), WHITE, 20, color, 4)
        draw.ellipse((145, y + 22, 215, y + 92), fill=color)
        label(draw, (180, y + 57), number, 27, WHITE, True, "mm")
        label(draw, (270, y + 57), title, 31, NAVY, True, "lm")
        label(draw, (650, y + 57), note, 27, SLATE, False, "lm")
        if index < len(steps) - 1:
            draw.line((800, y + 115, 800, y + 135), fill=CYAN, width=7)
        y += 135

    rounded(draw, (260, 790, 1340, 865), NAVY, 18)
    label(draw, (800, 827), "外部文件提供線索，不提供新的授權", 29, CYAN, True, "mm")
    save(image, "day15-05-untrusted-input.png")


if __name__ == "__main__":
    cover()
    two_layers()
    permission_surfaces()
    three_decisions()
    untrusted_input()
