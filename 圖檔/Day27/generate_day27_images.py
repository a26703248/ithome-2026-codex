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
    draw_text(draw, (80, 116), title, 50, NAVY, True)
    if subtitle:
        draw_text(draw, (82, 190), subtitle, 26, SLATE)
    draw.line((80, 238, 1520, 238), fill="#C9D5DB", width=2)


def footer(draw, number):
    draw_text(draw, (80, 846), "2026 iThome 鐵人賽｜ChatGPT & Codex", 20, SLATE)
    draw_text(draw, (1520, 846), f"DAY 27 · {number:02d}", 20, SLATE, True, anchor="ra")


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
    draw_text(draw, (100, 92), "DAY 27｜團隊、流程與治理", 27, "#77D2C4", True)
    draw_text(draw, (100, 205), "成本與效能管理", 62, WHITE, True)
    draw_text(draw, (104, 307), "回應更快，不等於總成本更低", 32, "#DCEBE8")

    stages = [
        ("14 分鐘", "AI 生成看起來很快", CORAL),
        ("＋ 9 分鐘", "OCR／ETL 前處理", GOLD),
        ("＋ 33 分鐘", "覆核＋返工", TEAL),
        ("＝ 56 分鐘", "一份被接受的成果", TEAL),
    ]
    x_positions = [105, 465, 825, 1185]
    y = 500
    for index, ((title, detail, color), x) in enumerate(zip(stages, x_positions)):
        box(draw, (x, y, x + 270, y + 170), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + 135, y + 58), title, 30, WHITE, True, anchor="mm")
        draw_text(draw, (x + 135, y + 116), detail, 21, "#C8D8DF", anchor="mm", max_width=230, align="center")
        if index < len(stages) - 1:
            arrow(draw, (x + 280, y + 85), (x + 345, y + 85), "#91A8B6", 5)
    draw_text(draw, (100, 805), "比較單位是「被接受的成果」，不是一次模型回應", 25, "#AFC5CE")
    save(image, "day27-01-cover.png")


def cost_breakdown():
    image, draw = canvas()
    header(draw, "看每個被接受成果的總成本", "補 OcrPreprocessor 測試：一份定稿要花多少時間")
    labels = [(80, 300, 460, "成本項目"), (480, 300, 1520, "本案例數值")]
    for x1, y1, x2, title in labels:
        box(draw, (x1, y1 - 45, x2, y1), fill=NAVY, radius=12)
        draw_text(draw, ((x1 + x2) / 2, y1 - 22), title, 22, WHITE, True, anchor="mm")
    rows = [
        ("模型／方案使用", "共 6 輪對話，未量測精確 token 數"),
        ("OCR／ETL 前處理時間", "約 9 分鐘（含 2 份低解析度情境重新確認）"),
        ("AI 草稿生成執行與等待", "約 14 分鐘"),
        ("複核人員審查時間", "約 22 分鐘"),
        ("重新生成與返工", "2 次，共 11 分鐘"),
        ("最終被接受草稿", "第 3 版（v3），8 項測試通過覆核"),
    ]
    y = 322
    row_height = 78
    coords = [(80, 460), (480, 1520)]
    for index, row in enumerate(rows):
        fill = WHITE if index % 2 == 0 else "#EDF3F3"
        for column, ((x1, x2), value) in enumerate(zip(coords, row)):
            box(draw, (x1, y, x2, y + row_height - 10), fill=fill, outline="#D4DEE2", width=2, radius=12)
            color = TEAL if column == 0 else INK
            draw_text(draw, (x1 + 24, y + (row_height - 10) / 2), value, 21, color, column == 0,
                      max_width=x2 - x1 - 48, anchor="lm")
        y += row_height
    box(draw, (80, 812, 1520, 838), fill=MINT, radius=14)
    draw_text(draw, (800, 825), "總計約 56 分鐘，只看 14 分鐘的生成時間會低估近 4 倍", 21, TEAL, True, anchor="mm")
    footer(draw, 2)
    save(image, "day27-02-cost-breakdown.png")


def strategy_comparison():
    image, draw = canvas()
    header(draw, "同一份測試檔，兩種做法", "策略 A：一次生成　vs　策略 B：拆成小步驟")

    col_w = 660
    xs = [110, 830]
    titles = [("策略 A：一次要求生成完整測試", CORAL), ("策略 B：拆成小步驟", TEAL)]
    rows_a = [
        ("首次產出時間", "4 分鐘產生 9 個測試案例"),
        ("覆核發現的問題", "漏掉 2 個邊界案例，1 項斷言錯誤"),
        ("重跑次數", "2 次：整批重生成＋單獨修正"),
        ("總耗時", "約 31 分鐘"),
        ("最終結果", "9 個測試，2 項需後補"),
    ]
    rows_b = [
        ("首次產出時間", "3 分鐘產生骨架＋3 個基本案例"),
        ("覆核發現的問題", "第二步驟就抓到邊界值遺漏"),
        ("重跑次數", "1 次：只補邊界案例"),
        ("總耗時", "約 19 分鐘"),
        ("最終結果", "8 個測試，一次到位"),
    ]

    for (x, (title, color), rows) in zip(xs, titles, [rows_a, rows_b]):
        box(draw, (x, 280, x + col_w, 330), fill=color, radius=16)
        draw_text(draw, (x + col_w / 2, 305), title, 23, WHITE, True, anchor="mm", max_width=col_w - 40)
        y = 344
        row_h = 90
        for label, value in rows:
            box(draw, (x, y, x + col_w, y + row_h - 12), fill=WHITE, outline="#D4DEE2", width=2, radius=14)
            draw_text(draw, (x + 24, y + 20), label, 19, SLATE, True)
            draw_text(draw, (x + 24, y + 47), value, 20, INK, max_width=col_w - 48, spacing=6)
            y += row_h

    box(draw, (110, 812, 1490, 852), fill=NAVY, radius=18)
    draw_text(draw, (800, 832), "產出快不等於總成本低，覆核與返工要一起算", 22, WHITE, True, anchor="mm")
    footer(draw, 3)
    save(image, "day27-03-strategy-comparison.png")


def scheduling_diagram():
    image, draw = canvas()
    header(draw, "串行或並行，看相依與衝突", "三個任務組合，三種排程判斷")

    combos = [
        ("組合一", "補 OCR 測試 ＋ 複核介面\n否決原因欄位", "無相依、低衝突", "並行", TEAL),
        ("組合二", "先定分級規則 → 再讓 ETL\n產生存取權限", "高相依", "串行", CORAL),
        ("組合三", "OCR 輸出格式調整 ＋\nprompt 調整（共用資料結構）", "中相依、高衝突風險", "先對齊介面\n再並行", GOLD),
    ]
    x_positions = [90, 620, 1150]
    y = 300
    w = 360
    h = 430
    for (label, task, risk, decision, color), x in zip(combos, x_positions):
        box(draw, (x, y, x + w, y + h), fill=WHITE, outline=color, width=4, radius=24)
        box(draw, (x, y, x + w, y + 64), fill=color, radius=24)
        draw_text(draw, (x + w / 2, y + 32), label, 24, WHITE, True, anchor="mm")
        draw_text(draw, (x + 26, y + 96), task, 21, NAVY, True, max_width=w - 52, spacing=10)
        draw.line((x + 26, y + 210, x + w - 26, y + 210), fill="#D9E2E6", width=2)
        draw_text(draw, (x + 26, y + 232), "風險：" + risk, 20, SLATE, max_width=w - 52, spacing=8)
        box(draw, (x + 26, y + h - 96, x + w - 26, y + h - 26), fill="#EDF3F3", radius=16)
        draw_text(draw, (x + w / 2, y + h - 61), "建議：" + decision, 22, color, True, anchor="mm",
                  max_width=w - 70, align="center")
    footer(draw, 4)
    save(image, "day27-04-scheduling.png")


def tradeoff_triangle():
    image, draw = canvas()
    header(draw, "成本最佳化的邊界", "省下來的時間，不能拿安全、測試與可維護性去換")

    cx, cy, r = 800, 560, 280
    import math
    labels = [
        ("成本／時間", TEAL, -90),
        ("安全與權限", CORAL, 150),
        ("測試與可維護性", GOLD, 30),
    ]
    points = []
    for _, _, angle in labels:
        rad = math.radians(angle)
        points.append((cx + r * math.cos(rad), cy + r * math.sin(rad)))
    draw.polygon(points, outline=NAVY, width=6)
    box(draw, (cx - 210, cy - 90, cx + 210, cy + 90), fill=WHITE, outline=NAVY, width=3, radius=20)
    draw_text(draw, (cx, cy - 20), "只縮短上下文、", 24, INK, True, anchor="mm")
    draw_text(draw, (cx, cy + 20), "把任務講清楚、排好順序", 24, INK, True, anchor="mm")

    for (text, color, angle), point in zip(labels, points):
        rad = math.radians(angle)
        lx = cx + (r + 130) * math.cos(rad)
        ly = cy + (r + 60) * math.sin(rad)
        draw.ellipse((point[0] - 14, point[1] - 14, point[0] + 14, point[1] + 14), fill=color)
        draw_text(draw, (lx, ly), text, 26, color, True, anchor="mm", align="center")

    box(draw, (140, 806, 1460, 848), fill=MINT, radius=18)
    draw_text(draw, (800, 827), "浪費的是等待與返工，不是驗收標準與安全把關", 22, TEAL, True, anchor="mm")
    footer(draw, 5)
    save(image, "day27-05-tradeoff.png")


if __name__ == "__main__":
    cover()
    cost_breakdown()
    strategy_comparison()
    scheduling_diagram()
    tradeoff_triangle()
    print("Generated 5 Day 27 images at 1600x900.")
