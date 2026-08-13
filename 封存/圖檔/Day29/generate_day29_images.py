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
    draw_text(draw, (1520, 846), f"DAY 29 · {number:02d}", 20, SLATE, True, anchor="ra")


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
    draw_text(draw, (100, 92), "DAY 29｜團隊、流程與治理", 27, "#77D2C4", True)
    draw_text(draw, (100, 205), "踩雷經驗談", 62, WHITE, True)
    draw_text(draw, (104, 307), "把事故翻譯成護欄，不是翻譯成一句下次小心", 30, "#DCEBE8")

    col_w = 640
    xs = [100, 800]
    titles = [("交辦、執行、驗收都可能出錯", CORAL), ("三次事故＋可重複使用的護欄", TEAL)]
    rows_a = ["上下文不足，AI 自己補假設", "修改範圍比預期廣", "完成摘要被讀者放大解讀"]
    rows_b = ["交辦前補資料分級與允許目錄", "diff 檔案數超出預期就先停", "標題寫清楚完成與待確認項目"]
    y0 = 470
    for x, (title, color), rows in zip(xs, titles, [rows_a, rows_b]):
        box(draw, (x, y0, x + col_w, y0 + 250), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + col_w / 2, y0 + 40), title, 24, WHITE, True, anchor="mm", max_width=col_w - 60)
        yy = y0 + 90
        for row in rows:
            draw_text(draw, (x + 34, yy), "・" + row, 21, "#DCEBE8", max_width=col_w - 68, spacing=8)
            yy += 48
    draw_text(draw, (100, 805), "三次事故都來自 Day 24、26、27 的真實紀錄，不是新編故事", 24, "#AFC5CE")
    save(image, "day29-01-cover.png")


def three_failure_modes():
    image, draw = canvas()
    header(draw, "同一問題的三個階段", "上下文不足 → 修改過廣 → 摘要誤導")

    col_w = 440
    xs = [90, 580, 1070]
    titles = [("階段一：交辦", CORAL), ("階段二：執行", GOLD), ("階段三：驗收", TEAL)]
    rows_list = [
        ["來源：Day 26", "任務沒說資料能不能用", "客戶掃描檔進了測試斷言", "Codex 沒被告知這條線"],
        ["來源：Day 27", "只准改 REJECT 分支", "列舉改名波及 5 個檔案", "diff 數量是最快訊號"],
        ["來源：Day 24", "程式契約已完成", "待確認四項被標題蓋過", "完成要寫清楚範圍"],
    ]
    y0 = 280
    for x, (title, color), rows in zip(xs, titles, rows_list):
        box(draw, (x, y0, x + col_w, y0 + 60), fill=color, radius=18)
        draw_text(draw, (x + col_w / 2, y0 + 30), title, 22, WHITE, True, anchor="mm")
        box(draw, (x, y0 + 76, x + col_w, y0 + 470), fill=WHITE, outline=color, width=3, radius=20)
        yy = y0 + 112
        for row in rows:
            draw_text(draw, (x + 26, yy), "・" + row, 20, INK, max_width=col_w - 52, spacing=8)
            yy += 88
        if x != xs[-1]:
            arrow(draw, (x + col_w + 8, y0 + 270), (x + col_w + 62, y0 + 270), SLATE, 5)

    box(draw, (110, 790, 1490, 840), fill=MINT, radius=16)
    draw_text(draw, (800, 815), "三個階段常常連在一起發生，不是三個孤立事件", 21, TEAL, True, anchor="mm")
    footer(draw, 2)
    save(image, "day29-02-three-failure-modes.png")


def diff_scope():
    image, draw = canvas()
    header(draw, "修改過廣的偵測", "允許改動的檔案清單　vs　實際 diff 變更")

    box(draw, (110, 280, 760, 620), fill=WHITE, outline=TEAL, width=4, radius=24)
    draw_text(draw, (435, 320), "交辦時的允許清單", 24, TEAL, True, anchor="mm")
    allow_rows = ["OcrPreprocessor.java", "OcrPreprocessorTest.java"]
    yy = 400
    for row in allow_rows:
        box(draw, (150, yy, 720, yy + 60), fill=MINT, radius=14)
        draw_text(draw, (435, yy + 30), row, 21, INK, True, anchor="mm")
        yy += 84
    draw_text(draw, (435, 580), "預期變更檔案數：2", 20, SLATE, True, anchor="mm")

    arrow(draw, (780, 450), (860, 450), CORAL, 8)

    box(draw, (860, 280, 1510, 700), fill=WHITE, outline=CORAL, width=4, radius=24)
    draw_text(draw, (1185, 320), "實際 diff 變更了 5 個檔案", 23, CORAL, True, anchor="mm")
    diff_rows = [
        ("OcrPreprocessor.java", True),
        ("OcrPreprocessorTest.java", True),
        ("OcrOutcome.java", False),
        ("BatchRejectReport.java", False),
        ("另一處批次報表引用", False),
    ]
    yy = 390
    for row, allowed in diff_rows:
        color = MINT if allowed else "#FBDCD3"
        border = TEAL if allowed else CORAL
        box(draw, (900, yy, 1470, yy + 50), fill=color, outline=border, width=2, radius=12)
        label = row + ("　（允許）" if allowed else "　（超出範圍）")
        draw_text(draw, (1185, yy + 25), label, 19, INK, True, anchor="mm")
        yy += 62

    box(draw, (110, 740, 1490, 800), fill=NAVY, radius=18)
    draw_text(draw, (800, 770), "檔案數對不上，就先停下來逐行看 diff，再決定要不要合併", 21, WHITE, True, anchor="mm")
    footer(draw, 3)
    save(image, "day29-03-diff-scope.png")


def guardrail_matrix():
    image, draw = canvas()
    header(draw, "從事故回推護欄", "三種失敗模式，各自的預防、偵測、限制影響、復原")

    headers = ["失敗模式", "預防", "偵測", "限制影響", "復原"]
    col_x = [80, 340, 700, 1000, 1280, 1520]
    for i, title in enumerate(headers):
        box(draw, (col_x[i], 260, col_x[i + 1] - 8, 305), fill=NAVY, radius=10)
        draw_text(draw, ((col_x[i] + col_x[i + 1] - 8) / 2, 282), title, 19, WHITE, True, anchor="mm")

    rows = [
        ("上下文不足\n（Day 26）", "交辦前填資料分級\n與允許目錄", "覆核測試斷言\n是否出現真實檔名", "限定可讀寫目錄\n到測試資料夾", "換成合成資料\n重跑測試"),
        ("修改過廣\n（列舉改名）", "交辦寫明允許\n改動的檔案清單", "核對 diff 變更\n檔案數是否超出預期", "只合併允許\n清單內的變更", "退回多餘變更\n拆成獨立任務"),
        ("摘要誤導\n（Day 24）", "標題寫清楚\n完成／待確認項目數", "展示或上線前\n重讀待確認清單", "縮小展示\n或發布範圍", "標成部分完成\n列出負責人"),
    ]
    y = 320
    row_h = 150
    for index, cells in enumerate(rows):
        fill = WHITE if index % 2 == 0 else "#EDF3F3"
        box(draw, (col_x[0], y, col_x[5], y + row_h - 12), fill=fill, outline="#D4DEE2", width=2, radius=14)
        for i, cell in enumerate(cells):
            color = TEAL if i == 0 else INK
            bold = i == 0
            draw_text(draw, (col_x[i] + 18, y + (row_h - 12) / 2), cell, 17, color, bold,
                      max_width=col_x[i + 1] - col_x[i] - 36, anchor="lm", spacing=6)
        y += row_h
    footer(draw, 4)
    save(image, "day29-04-guardrail-matrix.png")


def updated_workflow():
    image, draw = canvas()
    header(draw, "更新後的交辦與驗收流程", "三個新增檢查點，插進既有工作節奏")

    steps = [
        ("交辦", "新增：資料分級與\n允許改動範圍欄位", CORAL),
        ("執行", "Codex 依範圍\n讀寫檔案、修改程式", SLATE),
        ("Diff 檢查", "新增：變更檔案數\n是否超出允許清單", GOLD),
        ("測試驗證", "局部與完整測試\n都要通過", SLATE),
        ("交付摘要", "新增：標題寫清楚\n完成／待確認項目數", TEAL),
    ]
    x = 90
    step_w = 270
    y0 = 380
    for i, (title, desc, color) in enumerate(steps):
        box(draw, (x, y0, x + step_w, y0 + 220), fill=WHITE, outline=color, width=4, radius=20)
        box(draw, (x, y0, x + step_w, y0 + 60), fill=color, radius=20)
        draw_text(draw, (x + step_w / 2, y0 + 30), title, 22, WHITE, True, anchor="mm")
        draw_text(draw, (x + step_w / 2, y0 + 130), desc, 19, INK, anchor="mm",
                  max_width=step_w - 40, align="center", spacing=8)
        if i < len(steps) - 1:
            arrow(draw, (x + step_w + 6, y0 + 110), (x + step_w + 44, y0 + 110), NAVY, 5)
        x += step_w + 50

    box(draw, (110, 660, 1490, 720), fill=MINT, radius=18)
    draw_text(draw, (800, 690), "三個檢查點都來自這次的真實事故，不是憑空增加的流程", 21, TEAL, True, anchor="mm")
    footer(draw, 5)
    save(image, "day29-05-updated-workflow.png")


if __name__ == "__main__":
    cover()
    three_failure_modes()
    diff_scope()
    guardrail_matrix()
    updated_workflow()
    print("Generated 5 Day 29 images at 1600x900.")
