from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
W, H = 1600, 900
NAVY = "#11263D"
INK = "#183047"
TEAL = "#1C8C82"
MINT = "#DDF3EC"
CREAM = "#F7F3E8"
WHITE = "#FFFFFF"
CORAL = "#EE7B65"
GOLD = "#E4AD43"
SLATE = "#547084"
PALE = "#E8EEF2"
FONT = Path(r"C:\Windows\Fonts\msjh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msjhbd.ttc")


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def canvas():
    image = Image.new("RGB", (W, H), CREAM)
    return image, ImageDraw.Draw(image)


def text_width(draw, value, f):
    box = draw.textbbox((0, 0), value, font=f)
    return box[2] - box[0]


def wrap(draw, value, f, max_width):
    lines = []
    current = ""
    for char in value:
        trial = current + char
        if current and text_width(draw, trial, f) > max_width:
            lines.append(current)
            current = char
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def draw_text(draw, xy, value, size, color=INK, bold=False, max_width=None,
              anchor="la", spacing=12, align="left"):
    f = font(size, bold)
    if max_width:
        value = "\n".join(wrap(draw, value, f, max_width))
    draw.multiline_text(xy, value, font=f, fill=color, anchor=anchor,
                        spacing=spacing, align=align)


def box(draw, xy, fill=WHITE, outline=None, width=2, radius=26):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def header(draw, kicker, title, subtitle=None):
    draw_text(draw, (80, 62), kicker, 26, TEAL, True)
    draw_text(draw, (80, 116), title, 54, NAVY, True)
    if subtitle:
        draw_text(draw, (82, 190), subtitle, 26, SLATE)
    draw.line((80, 238, 1520, 238), fill="#C9D5DB", width=2)


def footer(draw, number):
    draw_text(draw, (80, 846), "2026 iThome 鐵人賽｜ChatGPT & Codex", 20, SLATE)
    draw_text(draw, (1520, 846), f"DAY 25 · {number:02d}", 20, SLATE, True, anchor="ra")


def save(image, name):
    image.save(OUT / name, "PNG", optimize=True)


def cover():
    image, draw = canvas()
    draw.rectangle((0, 0, W, H), fill=NAVY)
    draw.ellipse((1060, -190, 1760, 510), fill="#173D57")
    draw.ellipse((-180, 590, 430, 1200), fill="#163C50")
    draw_text(draw, (100, 92), "DAY 25｜從 0 到 1 的 AI 可驗證工作流試煉", 27, "#77D2C4", True)
    draw_text(draw, (100, 205), "不只是工程師", 76, WHITE, True)
    draw_text(draw, (104, 310), "AI 加速的是交接，不是取代角色", 34, "#DCEBE8")

    roles = [
        ("PM", "定義範圍", 120, TEAL),
        ("法遵", "核定規則", 390, GOLD),
        ("設計／QA", "補齊驗收", 660, CORAL),
        ("工程", "實作測試", 930, TEAL),
        ("維運", "部署復原", 1200, GOLD),
    ]
    y = 505
    for idx, (role, task, x, color) in enumerate(roles):
        box(draw, (x, y, x + 220, y + 150), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + 110, y + 46), role, 31, WHITE, True, anchor="mm")
        draw_text(draw, (x + 110, y + 102), task, 23, "#C8D8DF", anchor="mm")
        if idx < len(roles) - 1:
            draw.line((x + 224, y + 75, x + 258, y + 75), fill="#91A8B6", width=5)
            draw.polygon([(x + 258, y + 75), (x + 244, y + 65), (x + 244, y + 85)], fill="#91A8B6")
    draw_text(draw, (100, 805), "ChatGPT 整理脈絡｜Codex 執行驗證｜人員承擔決策", 25, "#AFC5CE")
    save(image, "day25-01-cover.png")


def role_matrix():
    image, draw = canvas()
    header(draw, "角色 × 工具 × 責任", "工具可以接力，決策不能外包")
    columns = [(80, 300, 285, "角色"), (305, 300, 655, "ChatGPT"),
               (675, 300, 1025, "Codex"), (1045, 300, 1520, "人工責任")]
    for x1, y1, x2, title in columns:
        box(draw, (x1, y1 - 46, x2, y1), fill=NAVY, radius=12)
        draw_text(draw, ((x1 + x2) / 2, y1 - 24), title, 22, WHITE, True, anchor="mm")
    rows = [
        ("PM", "整理決議與空白", "查既有實作限制", "範圍與優先順序"),
        ("法遵／資安", "轉成檢查問題", "找權限與日誌證據", "分級與例外"),
        ("設計／QA", "補狀態與測試案例", "原型與自動化測試", "可用性與風險覆蓋"),
        ("工程／維運", "整理方案與手冊", "修改、測試、查設定", "差異、部署與復原"),
    ]
    y = 322
    row_h = 112
    for i, row in enumerate(rows):
        fill = WHITE if i % 2 == 0 else "#EDF3F3"
        coords = [(80, 285), (305, 655), (675, 1025), (1045, 1520)]
        for j, (x1, x2) in enumerate(coords):
            box(draw, (x1, y, x2, y + row_h - 12), fill=fill, outline="#D4DEE2", width=2, radius=12)
            color = TEAL if j == 0 else INK
            draw_text(draw, ((x1 + x2) / 2, y + 49), row[j], 21, color, j == 0,
                      max_width=x2 - x1 - 24, anchor="mm", align="center")
        y += row_h
    box(draw, (80, 786, 1520, 824), fill=MINT, radius=16)
    draw_text(draw, (800, 805), "規則不清楚時先標示待確認；證據不足時不要自動補答案", 22, TEAL, True, anchor="mm")
    footer(draw, 2)
    save(image, "day25-02-role-matrix.png")


def before_after():
    image, draw = canvas()
    header(draw, "交接單前後對照", "從一句模糊交辦，到下一位能驗收的輸入")
    box(draw, (80, 292, 590, 745), fill="#FBE8E4", outline="#F2B7AA", width=3)
    draw_text(draw, (120, 332), "整理前", 28, CORAL, True)
    draw_text(draw, (120, 410), "「請幫我做複核介面」", 35, NAVY, True, max_width=430)
    draw_text(draw, (120, 555), "缺少：\n誰決定規則？\n怎樣才算完成？\n失敗時留下什麼？", 25, SLATE, max_width=410, spacing=18)
    draw.line((630, 515, 755, 515), fill=TEAL, width=8)
    draw.polygon([(755, 515), (725, 493), (725, 537)], fill=TEAL)
    draw_text(draw, (692, 465), "ChatGPT\n只整理，不代答", 22, TEAL, True, anchor="mm", align="center")
    box(draw, (795, 292, 1520, 745), fill=WHITE, outline="#B6DAD3", width=3)
    draw_text(draw, (835, 332), "整理後", 28, TEAL, True)
    items = [
        ("已確認", "不含自動發布；複核原因必填"),
        ("待確認", "版本衝突與資料留存策略"),
        ("驗收條件", "畫面、測試、日誌或設定可證明"),
        ("負責人", "PM、法遵、設計、QA、維運逐項簽認"),
    ]
    y = 405
    colors = [TEAL, GOLD, CORAL, NAVY]
    for (label, detail), color in zip(items, colors):
        draw.ellipse((840, y + 5, 864, y + 29), fill=color)
        draw_text(draw, (885, y), label, 23, color, True)
        draw_text(draw, (1040, y), detail, 22, INK, max_width=420)
        y += 82
    footer(draw, 3)
    save(image, "day25-03-handoff-before-after.png")


def handoff_flow():
    image, draw = canvas()
    header(draw, "複核功能交接流程", "每一棒都有輸入、輸出與驗收證據")
    stages = [
        ("1", "PM", "範圍／驗收", TEAL),
        ("2", "法遵＋設計", "規則／狀態", GOLD),
        ("3", "QA", "例外／邊界", CORAL),
        ("4", "工程＋Codex", "程式／測試", TEAL),
        ("5", "維運", "監控／復原", NAVY),
    ]
    xs = [70, 375, 680, 985, 1290]
    y = 360
    for i, ((num, role, output, color), x) in enumerate(zip(stages, xs)):
        if i:
            draw.line((x - 80, y + 112, x - 18, y + 112), fill="#91A7B2", width=6)
            draw.polygon([(x - 18, y + 112), (x - 36, y + 99), (x - 36, y + 125)], fill="#91A7B2")
        box(draw, (x, y, x + 240, y + 225), fill=WHITE, outline=color, width=4, radius=24)
        draw.ellipse((x + 18, y + 18, x + 68, y + 68), fill=color)
        draw_text(draw, (x + 43, y + 43), num, 23, WHITE, True, anchor="mm")
        draw_text(draw, (x + 120, y + 100), role, 27, NAVY, True, anchor="mm")
        draw.line((x + 35, y + 132, x + 205, y + 132), fill="#D5DFE3", width=2)
        draw_text(draw, (x + 120, y + 172), output, 22, SLATE, anchor="mm")
    box(draw, (220, 685, 1380, 765), fill=MINT, radius=24)
    draw_text(draw, (800, 725), "決議 → 介面狀態 → 測試案例 → 程式差異 → 部署檢查", 28, TEAL, True, anchor="mm")
    footer(draw, 4)
    save(image, "day25-04-handoff-flow.png")


def evidence_chain():
    image, draw = canvas()
    header(draw, "可追溯交付鏈", "「做完了」要能回到需求、測試與上線條件")
    nodes = [
        ("需求決議", "不含自動發布"),
        ("介面狀態", "載入／失敗／唯讀"),
        ("程式差異", "複核原因必填"),
        ("測試結果", "4 項通過"),
        ("部署檢查", "權限／監控／復原"),
    ]
    colors = [TEAL, GOLD, CORAL, TEAL, NAVY]
    x = 76
    y = 352
    for i, ((title, detail), color) in enumerate(zip(nodes, colors)):
        if i:
            draw.line((x - 54, y + 102, x - 12, y + 102), fill="#8AA0AC", width=5)
            draw.polygon([(x - 12, y + 102), (x - 28, y + 91), (x - 28, y + 113)], fill="#8AA0AC")
        box(draw, (x, y, x + 250, y + 205), fill=WHITE, outline=color, width=4, radius=24)
        draw_text(draw, (x + 125, y + 70), title, 27, color, True, anchor="mm")
        draw.line((x + 35, y + 105, x + 215, y + 105), fill="#D6E0E4", width=2)
        draw_text(draw, (x + 125, y + 146), detail, 21, INK, max_width=205, anchor="mm", align="center")
        x += 300
    box(draw, (80, 655, 1520, 770), fill=NAVY, radius=24)
    draw_text(draw, (800, 698), "通過測試 ≠ 可以直接上線", 30, WHITE, True, anchor="mm")
    draw_text(draw, (800, 741), "正式授權、資料留存、併發衝突與復原仍需真實環境驗證", 23, "#C7D8DF", anchor="mm")
    footer(draw, 5)
    save(image, "day25-05-evidence-chain.png")


if __name__ == "__main__":
    cover()
    role_matrix()
    before_after()
    handoff_flow()
    evidence_chain()
    print("Generated 5 Day 25 images at 1600x900.")
