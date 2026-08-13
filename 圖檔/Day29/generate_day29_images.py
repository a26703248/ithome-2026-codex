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
    draw_text(draw, (100, 92), "DAY 29｜從 0 到 1 的 AI 可驗證工作流試煉", 27, "#77D2C4", True)
    draw_text(draw, (100, 205), "用數據說話", 62, WHITE, True)
    draw_text(draw, (104, 307), "「感覺變快了」不是可採用的導入結論", 32, "#DCEBE8")

    col_w = 640
    xs = [100, 800]
    titles = [("只看生成時間、任務難度不同", CORAL), ("固定規格＋前後測＋品質護欄", TEAL)]
    rows_a = ["只記錄 AI 生成那幾分鐘", "前後任務範圍、難度不一致", "沒有品質護欄、只看速度"]
    rows_b = ["生成到定稿、複核全程都算", "同一規格，雙軌各做一次", "同時追蹤修改與否決比例"]
    y0 = 470
    for x, (title, color), rows in zip(xs, titles, [rows_a, rows_b]):
        box(draw, (x, y0, x + col_w, y0 + 250), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + col_w / 2, y0 + 40), title, 24, WHITE, True, anchor="mm", max_width=col_w - 60)
        yy = y0 + 90
        for row in rows:
            draw_text(draw, (x + 34, yy), "・" + row, 21, "#DCEBE8", max_width=col_w - 68, spacing=8)
            yy += 48
    draw_text(draw, (100, 805), "比較的單位是「可追溯的一批資料」，不是一次主觀印象", 24, "#AFC5CE")
    save(image, "day29-01-cover.png")


def metrics_guardrail():
    image, draw = canvas()
    header(draw, "效率指標要搭配品質護欄", "五項指標：定義、資料來源、對應護欄")

    headers = ["指標", "定義", "護欄行動"]
    col_x = [80, 430, 1120, 1520]
    for i, title in enumerate(headers):
        box(draw, (col_x[i], 260, col_x[i + 1] - 10, 305), fill=NAVY, radius=12)
        draw_text(draw, ((col_x[i] + col_x[i + 1] - 10) / 2, 282), title, 21, WHITE, True, anchor="mm")

    rows = [
        ("生成到定稿時間", "系統產出草稿到複核人員定稿的時間", "同時看修改或否決比例是否上升"),
        ("複核審查時間", "複核人員檢視、修改、標註的時間", "同時看引用錯誤數是否增加"),
        ("大幅修改或否決比例", "MAJOR_REVISION 與 REJECTED 合計佔比", "比例上升就先別擴大試用範圍"),
        ("任務完成率", "未被否決、有進入定稿流程的比例", "與否決原因交叉比對，不能只看數字"),
        ("平均引用錯誤數", "複核時發現引用既有內容出錯的次數", "錯誤數上升需加強複核強度"),
    ]
    y = 320
    row_h = 92
    for index, (metric, definition, guardrail) in enumerate(rows):
        fill = WHITE if index % 2 == 0 else "#EDF3F3"
        box(draw, (col_x[0], y, col_x[3], y + row_h - 10), fill=fill, outline="#D4DEE2", width=2, radius=14)
        draw_text(draw, (col_x[0] + 22, y + (row_h - 10) / 2), metric, 20, TEAL, True,
                  max_width=col_x[1] - col_x[0] - 44, anchor="lm", spacing=6)
        draw_text(draw, (col_x[1] + 22, y + (row_h - 10) / 2), definition, 19, INK,
                  max_width=col_x[2] - col_x[1] - 44, anchor="lm", spacing=6)
        draw_text(draw, (col_x[2] + 22, y + (row_h - 10) / 2), guardrail, 19, SLATE,
                  max_width=col_x[3] - col_x[2] - 44, anchor="lm", spacing=6)
        y += row_h
    box(draw, (80, 812, 1520, 848), fill=MINT, radius=16)
    draw_text(draw, (800, 830), "速度變快、品質同時退步，不能只摘速度那一半", 21, TEAL, True, anchor="mm")
    footer(draw, 2)
    save(image, "day29-02-metrics-guardrail.png")


def pre_post_design():
    image, draw = canvas()
    header(draw, "配對前後測，才可比較", "同一份規格，分別以人工與 Codex 各實作一次")

    box(draw, (560, 270, 1040, 340), fill=NAVY, radius=18)
    draw_text(draw, (800, 305), "固定規格＋固定驗收條件", 24, WHITE, True, anchor="mm")
    arrow(draw, (800, 345), (800, 390), TEAL, 6)

    col_w = 640
    xs = [100, 800]
    titles = [("基準線：人工撰寫", CORAL), ("AI 協作：Codex", TEAL)]
    rows_a = [
        ("設計＋撰寫", "6 分鐘設計＋24 分鐘產出"),
        ("覆核與測試", "12 分鐘"),
        ("返工", "1 次，6 分鐘：漏防呆空清單"),
        ("總耗時", "48 分鐘"),
    ]
    rows_b = [
        ("設計＋撰寫", "5 分鐘寫規格＋4 分鐘產出"),
        ("覆核與測試", "9 分鐘覆核 diff＋補測試"),
        ("返工", "1 次，8 分鐘：完成率定義理解落差"),
        ("總耗時", "26 分鐘"),
    ]
    y0 = 410
    for x, (title, color), rows in zip(xs, titles, [rows_a, rows_b]):
        box(draw, (x, y0, x + col_w, y0 + 50), fill=color, radius=16)
        draw_text(draw, (x + col_w / 2, y0 + 25), title, 22, WHITE, True, anchor="mm")
        yy = y0 + 64
        row_h = 78
        for label, value in rows:
            box(draw, (x, yy, x + col_w, yy + row_h - 12), fill=WHITE, outline="#D4DEE2", width=2, radius=14)
            draw_text(draw, (x + 24, yy + 18), label, 18, SLATE, True)
            draw_text(draw, (x + 24, yy + 44), value, 19, INK, max_width=col_w - 48, spacing=6)
            yy += row_h

    box(draw, (110, 812, 1490, 852), fill=NAVY, radius=18)
    draw_text(draw, (800, 832), "兩邊最後收斂到同 8 項測試，差異只在耗時與返工原因", 21, WHITE, True, anchor="mm")
    footer(draw, 3)
    save(image, "day29-03-pre-post-design.png")


def day01_vs_day28():
    image, draw = canvas()
    header(draw, "從主觀記錄到可追溯資料", "Day 01 基準線卡片　vs　Day 29 配對資料集")

    col_w = 640
    xs = [100, 800]
    titles = [("Day 01：基準線卡片", GOLD), ("Day 29：配對資料集", TEAL)]
    rows_a = [
        "任務範圍自選，難度不固定",
        "只記錄「原本完成時間」的粗略描述",
        "沒有固定驗收條件",
        "無法直接併入本篇統計數字",
    ]
    rows_b = [
        "同一規格雙軌各實作一次",
        "生成、複核、返工分項計時",
        "固定驗收條件：8 項測試＋例外處理",
        "16 筆樣本，基準線／AI 協作各 8 筆",
    ]
    y0 = 300
    for x, (title, color), rows in zip(xs, titles, [rows_a, rows_b]):
        box(draw, (x, y0, x + col_w, y0 + 400), fill=WHITE, outline=color, width=4, radius=24)
        box(draw, (x, y0, x + col_w, y0 + 60), fill=color, radius=24)
        draw_text(draw, (x + col_w / 2, y0 + 30), title, 23, WHITE, True, anchor="mm")
        yy = y0 + 96
        for row in rows:
            draw_text(draw, (x + 30, yy), "・" + row, 21, INK, max_width=col_w - 60, spacing=8)
            yy += 76

    box(draw, (110, 730, 1490, 800), fill=MINT, radius=18)
    draw_text(draw, (800, 750), "不是否定 Day 01，而是承認它的限制：", 21, TEAL, True, anchor="mm")
    draw_text(draw, (800, 778), "沒有固定驗收條件的紀錄，不能拿來做速度比較", 21, TEAL, True, anchor="mm")
    footer(draw, 4)
    save(image, "day29-04-day01-vs-day29.png")


def decision_matrix():
    image, draw = canvas()
    header(draw, "結果對應決策", "速度與品質，四種組合對應四種行動")

    cx0, cy0 = 480, 300
    size = 460
    mid_x = cx0 + size / 2
    mid_y = cy0 + size / 2
    box(draw, (cx0, cy0, cx0 + size, cy0 + size), fill=WHITE, outline=NAVY, width=4, radius=8)
    draw.line((mid_x, cy0, mid_x, cy0 + size), fill="#C9D5DB", width=3)
    draw.line((cx0, mid_y, cx0 + size, mid_y), fill="#C9D5DB", width=3)

    quadrants = [
        (cx0, cy0, "速度、品質\n都改善", "擴大試用", TEAL),
        (mid_x, cy0, "只提升品質", "評估額外\n時間是否值得", GOLD),
        (cx0, mid_y, "只提升速度", "補強複核驗收\n（本次落點）", CORAL),
        (mid_x, mid_y, "速度、品質\n都退步", "停止或\n重新設計流程", SLATE),
    ]
    half = size / 2
    for x, y, label, action, color in quadrants:
        draw_text(draw, (x + half / 2, y + 46), label, 19, NAVY, True, anchor="mm", max_width=half - 30, align="center")
        box(draw, (x + 20, y + 80, x + half - 20, y + half - 20), fill=color, radius=14)
        draw_text(draw, (x + half / 2, y + (80 + half - 20) / 2), action, 18, WHITE, True,
                  anchor="mm", max_width=half - 60, align="center")

    draw_text(draw, (cx0 + size / 2, cy0 - 34), "品質改善 →", 20, SLATE, True, anchor="mm")
    draw_text(draw, (cx0 - 40, mid_y), "速度改善 ↑", 20, SLATE, True, anchor="mm")

    box(draw, (1040, 320, 1520, 700), fill="#EDF3F3", outline=CORAL, width=3, radius=20)
    draw_text(draw, (1080, 356), "本次結果", 24, CORAL, True)
    draw_text(draw, (1080, 404), "生成到定稿：-42 分鐘", 20, INK, spacing=8)
    draw_text(draw, (1080, 440), "複核時間：+7.4 分鐘", 20, INK, spacing=8)
    draw_text(draw, (1080, 476), "大幅修改或否決：+12.5 個百分點", 20, INK, max_width=400, spacing=8)
    draw_text(draw, (1080, 540), "平均引用錯誤：+0.75（約 4 倍）", 20, INK, max_width=400, spacing=8)
    draw_text(draw, (1080, 600), "落在「只提升速度」象限：", 19, CORAL, True, max_width=400, spacing=8)
    draw_text(draw, (1080, 630), "先補強複核，不宜貿然擴大範圍", 19, CORAL, True, max_width=400, spacing=8)

    footer(draw, 5)
    save(image, "day29-05-decision-matrix.png")


if __name__ == "__main__":
    cover()
    metrics_guardrail()
    pre_post_design()
    day01_vs_day28()
    decision_matrix()
    print("Generated 5 Day 29 images at 1600x900.")
