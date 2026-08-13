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
    draw_text(draw, (80, 116), title, 46, NAVY, True)
    if subtitle:
        draw_text(draw, (82, 190), subtitle, 26, SLATE)
    draw.line((80, 238, 1520, 238), fill="#C9D5DB", width=2)


def footer(draw, number):
    draw_text(draw, (80, 846), "2026 iThome 鐵人賽｜ChatGPT & Codex", 20, SLATE)
    draw_text(draw, (1520, 846), f"DAY 30 · {number:02d}", 20, SLATE, True, anchor="ra")


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
    draw_text(draw, (100, 92), "DAY 30｜結語：AI 與人類是否能夠共存", 27, "#77D2C4", True)
    draw_text(draw, (100, 195), "What's next?", 60, WHITE, True)
    draw_text(draw, (104, 296), "沒有找到替我負責的工具,找到了一套能重跑的方法", 28, "#DCEBE8")

    col_w = 640
    xs = [100, 800]
    titles = [("Day 01 出發時的期待", CORAL), ("Day 30 收斂後的答案", TEAL)]
    rows_a = ["能不能縮短 Java 開發工作", "任務難度自選、樣本數是 1", "效率提升只是主觀印象"]
    rows_b = ["加速釐清、定位與執行,不接手判斷", "六欄提示詞、允許清單、品質護欄", "配對前後測,誠實標出樣本限制"]
    y0 = 470
    for x, (title, color), rows in zip(xs, titles, [rows_a, rows_b]):
        box(draw, (x, y0, x + col_w, y0 + 250), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + col_w / 2, y0 + 40), title, 24, WHITE, True, anchor="mm", max_width=col_w - 60)
        yy = y0 + 90
        for row in rows:
            draw_text(draw, (x + 34, yy), "・" + row, 21, "#DCEBE8", max_width=col_w - 68, spacing=8)
            yy += 48
    draw_text(draw, (100, 805), "封面兩欄取材自 Day 01 基準線卡片與本篇各節的真實引用", 24, "#AFC5CE")
    save(image, "day30-01-cover.png")


def five_stage_overview():
    image, draw = canvas()
    header(draw, "30 天五個階段", "各階段留下的關鍵收穫,不是各自獨立的短文")

    stages = [
        ("第 0 週", "心智模型", "Day 01-03", "先分清楚兩者的\n能力邊界", CORAL),
        ("第 1 週", "需求與設計", "Day 04-09", "提示詞六欄,把\n未知決策攤開", GOLD),
        ("第 2 週", "Codex 基礎", "Day 10-16", "讀→改→測→報,\n證據留在 diff 裡", TEAL),
        ("第 3 週", "整合工作流", "Day 17-24", "重構、除錯、文件\n都靠拆小任務", SLATE),
        ("第 4 週", "團隊與治理", "Day 25-29", "個人技巧變成\n可稽核的流程", NAVY),
    ]
    col_w = 250
    gap = 45
    x = 90
    y0 = 300
    for i, (week, title, days, note, color) in enumerate(stages):
        box(draw, (x, y0, x + col_w, y0 + 60), fill=color, radius=18)
        draw_text(draw, (x + col_w / 2, y0 + 30), week, 22, WHITE, True, anchor="mm")
        box(draw, (x, y0 + 76, x + col_w, y0 + 430), fill=WHITE, outline=color, width=3, radius=20)
        draw_text(draw, (x + col_w / 2, y0 + 116), title, 23, INK, True, anchor="mm", max_width=col_w - 30)
        draw_text(draw, (x + col_w / 2, y0 + 160), days, 19, SLATE, anchor="mm")
        draw_text(draw, (x + col_w / 2, y0 + 230), note, 19, INK, anchor="mm", max_width=col_w - 40,
                  align="center", spacing=8)
        if i < len(stages) - 1:
            arrow(draw, (x + col_w + 4, y0 + 250), (x + col_w + gap - 4, y0 + 250), SLATE, 5)
        x += col_w + gap

    box(draw, (110, 770, 1490, 820), fill=MINT, radius=16)
    draw_text(draw, (800, 795), "五週彼此呼應,才是評審重點裡的「結構」,不是三十篇各自的短文", 21, TEAL, True, anchor="mm")
    footer(draw, 2)
    save(image, "day30-02-five-stage-overview.png")


def tool_vs_human():
    image, draw = canvas()
    header(draw, "代理可以執行,責任不能外包", "工具加速的工作,和必須留給人判斷的工作")

    box(draw, (110, 280, 760, 700), fill=WHITE, outline=TEAL, width=4, radius=24)
    draw_text(draw, (435, 322), "可以交給工具加速", 24, TEAL, True, anchor="mm")
    left_rows = ["定位問題根因、產生候選修改", "執行指定測試與完整測試指令", "整理 diff、草擬 commit／PR 說明"]
    yy = 400
    for row in left_rows:
        box(draw, (150, yy, 720, yy + 80), fill=MINT, radius=14)
        draw_text(draw, (435, yy + 40), row, 19, INK, True, anchor="mm", max_width=540)
        yy += 100

    arrow(draw, (780, 490), (860, 490), CORAL, 8)

    box(draw, (860, 280, 1510, 700), fill=WHITE, outline=CORAL, width=4, radius=24)
    draw_text(draw, (1185, 322), "必須由人負責", 24, CORAL, True, anchor="mm")
    right_rows = ["判斷業務規則是否正確", "核准資料存取與可改動範圍", "決定是否合併、是否上線"]
    yy = 400
    for row in right_rows:
        box(draw, (900, yy, 1470, yy + 80), fill="#FBDCD3", radius=14)
        draw_text(draw, (1185, yy + 40), row, 19, INK, True, anchor="mm", max_width=540)
        yy += 100

    box(draw, (110, 740, 1490, 800), fill=NAVY, radius=18)
    draw_text(draw, (800, 770), "Day 13-16、Day 27 的證據都落在這條線的兩側,線本身要交辦時先畫好", 20, WHITE, True, anchor="mm")
    footer(draw, 3)
    save(image, "day30-03-tool-vs-human.png")


def day01_day29_data():
    image, draw = canvas()
    header(draw, "Day 01 卡片　vs　Day 29 配對前後測", "範圍與樣本數不同,不能直接比;能比的是同條件跑出的數字")

    box(draw, (110, 280, 720, 500), fill="#EDF3F3", outline="#B9C7CC", width=3, radius=22)
    draw_text(draw, (415, 320), "Day 01 基準線卡片", 23, SLATE, True, anchor="mm")
    for i, row in enumerate(["任務難度：自選", "樣本數：1", "只能記錄主觀對照"]):
        draw_text(draw, (150, 368 + i * 38), "・" + row, 19, INK, max_width=540)
    draw_text(draw, (415, 478), "不適合拿來算百分比", 18, CORAL, True, anchor="mm")

    headers = ["指標", "基準線（人工）", "AI 協作", "差異"]
    col_x = [790, 990, 1180, 1370, 1520]
    for i, title in enumerate(headers):
        box(draw, (col_x[i], 280, col_x[i + 1] - 6, 322), fill=NAVY, radius=10)
        draw_text(draw, ((col_x[i] + col_x[i + 1] - 6) / 2, 301), title, 16, WHITE, True, anchor="mm")

    rows = [
        ("生成到定稿時間", "104.0 分鐘", "62.0 分鐘", "-40%"),
        ("平均複核時間", "21.1 分鐘", "28.5 分鐘", "+7.4 分鐘"),
        ("修改或否決比例", "25.0%", "37.5%", "+12.5pp"),
        ("平均引用錯誤數", "0.25", "1.00", "約 4 倍"),
    ]
    y = 330
    row_h = 38
    for index, cells in enumerate(rows):
        fill = WHITE if index % 2 == 0 else "#EDF3F3"
        box(draw, (col_x[0], y, col_x[4], y + row_h - 6), fill=fill, outline="#D4DEE2", width=2, radius=10)
        for i, cell in enumerate(cells):
            color = CORAL if i == 3 else INK
            bold = i == 0 or i == 3
            draw_text(draw, (col_x[i] + 14, y + (row_h - 6) / 2), cell, 15, color, bold,
                      anchor="lm", max_width=col_x[i + 1] - col_x[i] - 28)
        y += row_h

    box(draw, (110, 560, 1510, 700), fill=MINT, radius=20)
    draw_text(draw, (140, 590), "速度快 40%,複核負擔、修改否決比例、引用錯誤數同時變差", 22, TEAL, True, max_width=1350)
    draw_text(draw, (140, 634), "落在「只提升速度」象限:先補強複核驗收,不是急著擴大試用", 22, TEAL, True, max_width=1350)

    box(draw, (110, 730, 1510, 800), fill=NAVY, radius=18)
    draw_text(draw, (800, 765), "兩批各 8 筆屬示範規模,結論只支持這個案例,不能推論整個團隊", 21, WHITE, True, anchor="mm")
    footer(draw, 4)
    save(image, "day30-04-day01-day29-data.png")


def action_roadmap():
    image, draw = canvas()
    header(draw, "給讀者的下一步", "個人今天、專案本週、團隊本月,三個可以馬上開始的範圍")

    steps = [
        ("個人｜今天", "挑一個能重現的小型\nJava 缺陷,先補一項\n會失敗的測試", CORAL),
        ("專案｜本週", "補一份最小 AGENTS.md,\n交辦模板加一欄\n允許改動的檔案清單", GOLD),
        ("團隊｜本月", "選一項低風險用途,\n比照 SOP 與盤點表\n跑一輪有負責人的試辦", TEAL),
    ]
    col_w = 420
    x = 120
    y0 = 320
    for i, (title, desc, color) in enumerate(steps):
        box(draw, (x, y0, x + col_w, y0 + 340), fill=WHITE, outline=color, width=4, radius=24)
        box(draw, (x, y0, x + col_w, y0 + 74), fill=color, radius=24)
        draw_text(draw, (x + col_w / 2, y0 + 37), title, 26, WHITE, True, anchor="mm")
        draw_text(draw, (x + col_w / 2, y0 + 190), desc, 21, INK, anchor="mm",
                  max_width=col_w - 60, align="center", spacing=10)
        if i < len(steps) - 1:
            arrow(draw, (x + col_w + 8, y0 + 170), (x + col_w + 62, y0 + 170), SLATE, 6)
        x += col_w + 60

    box(draw, (120, 720, 1480, 780), fill=MINT, radius=18)
    draw_text(draw, (800, 750), "範圍一層比一層大,但都從同一套「先寫清楚、再要證據」的方法出發", 21, TEAL, True, anchor="mm")
    footer(draw, 5)
    save(image, "day30-05-action-roadmap.png")


def boundary_and_next():
    image, draw = canvas()
    header(draw, "邊界會一直移動", "AI 擅長的部分持續擴張,人要顧好的判斷責任沒有變")

    box(draw, (110, 280, 760, 700), fill=WHITE, outline=TEAL, width=4, radius=24)
    draw_text(draw, (435, 322), "context／skill／Agent", 24, TEAL, True, anchor="mm")
    left_rows = [
        "context：先把上下文交代清楚,\n工具才少猜錯",
        "skill：把重複驗證過的做法\n收進可重跑的技能",
        "Agent：授權範圍變大,\n核對證據的責任也變大",
    ]
    yy = 400
    for row in left_rows:
        box(draw, (150, yy, 720, yy + 90), fill=MINT, radius=14)
        draw_text(draw, (435, yy + 45), row, 19, INK, True, anchor="mm", max_width=540, align="center")
        yy += 110

    arrow(draw, (780, 490), (860, 490), CORAL, 8)

    box(draw, (860, 280, 1510, 700), fill=WHITE, outline=CORAL, width=4, radius=24)
    draw_text(draw, (1185, 322), "不會跟著移動的界線", 24, CORAL, True, anchor="mm")
    right_rows = ["目標與限制由人設定", "驗收條件由人拍板", "上線與否由人承擔後果"]
    yy = 400
    for row in right_rows:
        box(draw, (900, yy, 1470, yy + 80), fill="#FBDCD3", radius=14)
        draw_text(draw, (1185, yy + 40), row, 19, INK, True, anchor="mm", max_width=540)
        yy += 100

    box(draw, (110, 740, 1490, 800), fill=NAVY, radius=18)
    draw_text(draw, (800, 770), "工具能做的事會一直變多,但誰承擔判斷責任,三十天下來沒有變過", 20, WHITE, True, anchor="mm")
    footer(draw, 6)
    save(image, "day30-06-boundary-and-next.png")


if __name__ == "__main__":
    cover()
    five_stage_overview()
    tool_vs_human()
    day01_day29_data()
    action_roadmap()
    boundary_and_next()
    print("Generated 6 Day 30 images at 1600x900.")
