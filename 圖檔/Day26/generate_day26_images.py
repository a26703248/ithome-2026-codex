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
FONT_CANDIDATES = [
    (Path(r"C:\Windows\Fonts\msjh.ttc"), Path(r"C:\Windows\Fonts\msjhbd.ttc")),
    (Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
     Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")),
]


def _resolve_fonts():
    for regular, bold in FONT_CANDIDATES:
        if regular.exists() and bold.exists():
            return regular, bold
    raise FileNotFoundError("No CJK font found; install Microsoft JhengHei or Noto Sans CJK.")


FONT, FONT_BOLD = _resolve_fonts()


def font(size: int, bold: bool = False):
    path = FONT_BOLD if bold else FONT
    if path.suffix.lower() == ".ttc" and "NotoSansCJK" in path.name:
        return ImageFont.truetype(str(path), size, index=3)  # index 3 == Traditional Chinese face
    return ImageFont.truetype(str(path), size)


def canvas():
    image = Image.new("RGB", (W, H), CREAM)
    return image, ImageDraw.Draw(image)


def text_width(draw, value, text_font):
    bounds = draw.textbbox((0, 0), value, font=text_font)
    return bounds[2] - bounds[0]


def wrap(draw, value, text_font, max_width):
    lines = []
    current = ""
    for char in value:
        trial = current + char
        if current and text_width(draw, trial, text_font) > max_width:
            lines.append(current)
            current = char
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def draw_text(draw, xy, value, size, color=INK, bold=False, max_width=None,
              anchor="la", spacing=12, align="left"):
    text_font = font(size, bold)
    if max_width:
        value = "\n".join(wrap(draw, value, text_font, max_width))
    draw.multiline_text(
        xy,
        value,
        font=text_font,
        fill=color,
        anchor=anchor,
        spacing=spacing,
        align=align,
    )


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
    draw_text(draw, (1520, 846), f"DAY 26 · {number:02d}", 20, SLATE, True, anchor="ra")


def save(image, name):
    image.save(OUT / name, "PNG", optimize=True)


def arrow(draw, start, end, color=TEAL, width=6):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    draw.polygon([(x2, y2), (x2 - 18, y2 - 12), (x2 - 18, y2 + 12)], fill=color)


def cover():
    image, draw = canvas()
    draw.rectangle((0, 0, W, H), fill=NAVY)
    draw.ellipse((1090, -210, 1760, 460), fill="#173D57")
    draw.ellipse((-180, 610, 410, 1200), fill="#163C50")
    draw_text(draw, (100, 92), "DAY 26｜團隊、流程與治理", 27, "#77D2C4", True)
    draw_text(draw, (100, 205), "導入 AI 開發工具的治理課題", 62, WHITE, True)
    draw_text(draw, (104, 307), "個人試用順手，不等於組織可以直接開放", 32, "#DCEBE8")

    stages = [
        ("個人試用", "順手、無紀錄", CORAL),
        ("事件發生", "真實資料被誤用", GOLD),
        ("盤點用途", "風險分級", TEAL),
        ("組織治理", "權限＋稽核＋覆核", TEAL),
    ]
    x_positions = [105, 465, 825, 1185]
    y = 500
    for index, ((title, detail, color), x) in enumerate(zip(stages, x_positions)):
        box(draw, (x, y, x + 270, y + 170), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + 135, y + 58), title, 28, WHITE, True, anchor="mm")
        draw_text(draw, (x + 135, y + 116), detail, 21, "#C8D8DF", anchor="mm", max_width=230, align="center")
        if index < len(stages) - 1:
            arrow(draw, (x + 280, y + 85), (x + 345, y + 85), "#91A8B6", 5)
    draw_text(draw, (100, 805), "治理邊界擋不住的，就交給程式碼擋", 25, "#AFC5CE")
    save(image, "day26-01-cover.png")


def inventory_table():
    image, draw = canvas()
    header(draw, "先把用途攤開", "使用案例盤點：誰、碰什麼、拿到什麼權限")
    labels = [(80, 300, 300, "盤點項目"), (320, 300, 900, "本案例內容"),
              (920, 300, 1520, "主要風險")]
    for x1, y1, x2, title in labels:
        box(draw, (x1, y1 - 45, x2, y1), fill=NAVY, radius=12)
        draw_text(draw, ((x1 + x2) / 2, y1 - 22), title, 22, WHITE, True, anchor="mm")
    rows = [
        ("使用目的", "補 OCR／ETL 前處理測試、調整草稿生成邏輯", "誤把測試範圍當成生產資料"),
        ("輸入資料", "測試資料是否使用真實客戶掃描檔、含個資", "個資或機密文件外流"),
        ("工具權限", "Codex 可讀寫目錄、能否連外部網路", "誤讀客戶資料庫或機密設定"),
        ("輸出用途", "修改是否先開分支、經 Code Review 才合併", "未經審查的變更混入正式環境"),
        ("外部依賴", "Codex 執行環境、OCR／ETL 套件來源", "供應商合規責任"),
    ]
    y = 322
    row_height = 96
    coords = [(80, 300), (320, 900), (920, 1520)]
    for index, row in enumerate(rows):
        fill = WHITE if index % 2 == 0 else "#EDF3F3"
        for column, ((x1, x2), value) in enumerate(zip(coords, row)):
            box(draw, (x1, y, x2, y + row_height - 12), fill=fill, outline="#D4DEE2", width=2, radius=12)
            color = TEAL if column == 0 else (CORAL if column == 2 else INK)
            draw_text(draw, (x1 + 24, y + (row_height - 12) / 2), value, 21, color, column == 0,
                      max_width=x2 - x1 - 48, anchor="lm")
        y += row_height
    box(draw, (80, 800, 1520, 838), fill=MINT, radius=16)
    draw_text(draw, (800, 819), "風險越高，核准與覆核就該越嚴，不是所有用途一視同仁", 22, TEAL, True, anchor="mm")
    footer(draw, 2)
    save(image, "day26-02-inventory.png")


def governance_hexagon():
    image, draw = canvas()
    header(draw, "治理骨架", "六個面向，缺一不可")
    items = [
        ("權限與分級", "無角色對應分級清單", CORAL),
        ("稽核紀錄", "Codex 操作無對應紀錄", GOLD),
        ("人工覆核", "分級邏輯異動未加嚴", TEAL),
        ("事件通報", "無標準表單與時限", CORAL),
        ("供應商變更", "條款更新未重新評估", GOLD),
        ("效果改善", "沒人追蹤執行率", TEAL),
    ]
    cols = 3
    cell_w, cell_h = 460, 190
    gap_x, gap_y = 40, 40
    start_x, start_y = 100, 300
    for index, (title, gap, color) in enumerate(items):
        col = index % cols
        row = index // cols
        x = start_x + col * (cell_w + gap_x)
        y = start_y + row * (cell_h + gap_y)
        box(draw, (x, y, x + cell_w, y + cell_h), fill=WHITE, outline=color, width=4, radius=22)
        draw_text(draw, (x + 30, y + 34), title, 30, NAVY, True)
        draw.line((x + 30, y + 82, x + cell_w - 30, y + 82), fill="#D9E2E6", width=2)
        draw_text(draw, (x + 30, y + 104), "缺口：" + gap, 22, SLATE, max_width=cell_w - 60, spacing=10)
    footer(draw, 3)
    save(image, "day26-03-governance-hexagon.png")


def dev_flow():
    image, draw = canvas()
    header(draw, "把治理放進開發流程", "每個節點都有一個能被追問的答案")
    stages = [
        ("1", "任務申請", "使用目的＋\n資料分級", TEAL),
        ("2", "存取檢查", "AccessGovernance\nGuard 核准／拒絕", CORAL),
        ("3", "Codex 執行", "讀寫範圍受限\n於核准結果", GOLD),
        ("4", "Code Review", "分級異動\n雙人覆核", TEAL),
        ("5", "稽核紀錄", "核准與拒絕\n都留存", NAVY),
    ]
    x_positions = [70, 375, 680, 985, 1290]
    y = 345
    for index, ((number, role, output, color), x) in enumerate(zip(stages, x_positions)):
        if index:
            arrow(draw, (x - 78, y + 118), (x - 18, y + 118), "#91A7B2", 5)
        box(draw, (x, y, x + 240, y + 238), fill=WHITE, outline=color, width=4, radius=24)
        draw.ellipse((x + 18, y + 18, x + 68, y + 68), fill=color)
        draw_text(draw, (x + 43, y + 43), number, 23, WHITE, True, anchor="mm")
        draw_text(draw, (x + 120, y + 96), role, 25, NAVY, True, anchor="mm")
        draw.line((x + 35, y + 132, x + 205, y + 132), fill="#D5DFE3", width=2)
        draw_text(draw, (x + 120, y + 181), output, 21, SLATE, anchor="mm", align="center", spacing=13)
    box(draw, (180, 680, 1420, 770), fill=NAVY, radius=24)
    draw_text(draw, (800, 711), "被拒絕的請求不是消失，是變成一筆可查的稽核事件", 26, WHITE, True, anchor="mm")
    draw_text(draw, (800, 751), "角色不符、用途空白或分級異動 → 停止並留存原因", 21, "#C7D8DF", anchor="mm")
    footer(draw, 4)
    save(image, "day26-04-dev-flow.png")


def copyright_layers():
    image, draw = canvas()
    header(draw, "引用邊界", "素材屬於哪一層，決定能不能引用原文")
    layers = [
        ("第一層", "ISO／CNS 標準", "只能用自己的話說明\n逐字引用一律視為紅燈", CORAL, "#FBE8E4"),
        ("第二層", "法律條文", "可自由引用、全文轉錄\n建議註明條號與出處", GOLD, "#FBF1DC"),
        ("第三層", "開放／公開授權", "依授權引用、改作\n標註來源與版本", TEAL, "#E1F1EC"),
    ]
    x = 110
    width = 430
    y = 300
    for title, name, rule, color, bg in layers:
        box(draw, (x, y, x + width, y + 430), fill=bg, outline=color, width=4, radius=26)
        draw_text(draw, (x + width / 2, y + 60), title, 26, color, True, anchor="mm")
        draw_text(draw, (x + width / 2, y + 116), name, 32, NAVY, True, anchor="mm")
        draw.line((x + 40, y + 160, x + width - 40, y + 160), fill="#D9E2E6", width=2)
        draw_text(draw, (x + width / 2, y + 250), rule, 23, INK, anchor="mm", align="center", spacing=16)
        x += width + 45
    box(draw, (110, 760, 1490, 812), fill=NAVY, radius=20)
    draw_text(draw, (800, 786), "本篇引用 ISO/IEC 42001 一律改寫；法律與政府框架標明出處", 23, WHITE, True, anchor="mm")
    footer(draw, 5)
    save(image, "day26-05-copyright-layers.png")


if __name__ == "__main__":
    cover()
    inventory_table()
    governance_hexagon()
    dev_flow()
    copyright_layers()
    print("Generated 5 Day 26 images at 1600x900.")
