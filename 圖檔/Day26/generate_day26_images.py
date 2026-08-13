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
    draw_text(draw, (100, 92), "DAY 26｜從 0 到 1 的 AI 可驗證工作流試煉", 27, "#77D2C4", True)
    draw_text(draw, (100, 205), "團隊 Prompt 庫與 SOP", 70, WHITE, True)
    draw_text(draw, (104, 307), "能測試、能否決、能維護，才是團隊資產", 32, "#DCEBE8")

    stages = [
        ("聊天紀錄", "個人經驗", CORAL),
        ("版本化 Prompt", "輸入與停止條件", TEAL),
        ("基準案例", "預期與失效", GOLD),
        ("複核 SOP", "角色與升級", TEAL),
    ]
    x_positions = [105, 465, 825, 1185]
    y = 500
    for index, ((title, detail, color), x) in enumerate(zip(stages, x_positions)):
        box(draw, (x, y, x + 270, y + 170), fill="#173D57", outline=color, width=4, radius=24)
        draw_text(draw, (x + 135, y + 58), title, 28, WHITE, True, anchor="mm")
        draw_text(draw, (x + 135, y + 116), detail, 22, "#C8D8DF", anchor="mm")
        if index < len(stages) - 1:
            arrow(draw, (x + 280, y + 85), (x + 345, y + 85), "#91A8B6", 5)
    draw_text(draw, (100, 805), "把一次成功，變成下一位能重跑的流程", 25, "#AFC5CE")
    save(image, "day26-01-cover.png")


def chat_to_asset():
    image, draw = canvas()
    header(draw, "從個人技巧到團隊資產", "提示詞離開聊天紀錄，才開始累積")
    box(draw, (80, 300, 650, 730), fill="#FBE8E4", outline="#F2B7AA", width=3)
    draw_text(draw, (120, 340), "個人聊天紀錄", 32, CORAL, True)
    chat_items = ["不知道是哪一版", "來源與限制散落", "沒有驗收基準", "換人就重新試"]
    y = 425
    for item in chat_items:
        draw.ellipse((125, y + 5, 147, y + 27), fill=CORAL)
        draw_text(draw, (170, y), item, 27, INK)
        y += 70

    arrow(draw, (700, 515), (865, 515), TEAL, 8)
    draw_text(draw, (782, 465), "補齊契約", 23, TEAL, True, anchor="mm")

    box(draw, (915, 300, 1520, 730), fill=WHITE, outline="#B6DAD3", width=3)
    draw_text(draw, (955, 340), "團隊提示詞資產", 32, TEAL, True)
    asset_items = ["版本與負責人", "必要輸入與禁止事項", "固定輸出與停止條件", "測試、失效與變更紀錄"]
    y = 425
    for item in asset_items:
        draw.ellipse((960, y + 5, 982, y + 27), fill=TEAL)
        draw_text(draw, (1005, y), item, 27, INK)
        y += 70
    footer(draw, 2)
    save(image, "day26-02-chat-to-asset.png")


def prompt_contract():
    image, draw = canvas()
    header(draw, "Prompt 契約", "不是一段神奇句子，而是一份可驗收工作說明")
    box(draw, (80, 290, 1520, 755), fill=WHITE, outline="#CAD7DD", width=3)
    draw_text(draw, (125, 330), "draft-from-sources · v0.1.0", 30, NAVY, True)
    cards = [
        ("必要輸入", "目的｜允許等級\n來源｜分級表｜沿用規則", TEAL),
        ("停止條件", "規則待確認\n來源超出權限", CORAL),
        ("固定輸出", "草稿標示｜來源對照\n沿用檢查｜待確認", GOLD),
        ("驗收責任", "人工核對來源\n另用一致算法重算", NAVY),
    ]
    x_positions = [120, 480, 840, 1200]
    for (title, detail, color), x in zip(cards, x_positions):
        box(draw, (x, 410, x + 280, 650), fill="#F7FAFA", outline=color, width=4, radius=24)
        draw_text(draw, (x + 140, 470), title, 28, color, True, anchor="mm")
        draw.line((x + 38, 515, x + 242, 515), fill="#D6E0E4", width=2)
        draw_text(draw, (x + 140, 570), detail, 22, INK, anchor="mm", align="center", spacing=18)
    box(draw, (210, 690, 1390, 735), fill=MINT, radius=18)
    draw_text(draw, (800, 713), "沒有核定規則時，正確輸出是停止，不是猜一個答案", 24, TEAL, True, anchor="mm")
    footer(draw, 3)
    save(image, "day26-03-prompt-contract.png")


def test_matrix():
    image, draw = canvas()
    header(draw, "合成案例人工走查", "沒有呼叫正式模型，只檢查判斷分支與預期結果")
    labels = [(80, 300, 220, "案例"), (240, 300, 790, "檢查重點"),
              (810, 300, 1270, "預期行為"), (1290, 300, 1520, "人工走查")]
    for x1, y1, x2, title in labels:
        box(draw, (x1, y1 - 45, x2, y1), fill=NAVY, radius=12)
        draw_text(draw, ((x1 + x2) / 2, y1 - 22), title, 22, WHITE, True, anchor="mm")
    rows = [
        ("P-01", "兩項主張、兩份來源", "各自連回來源", "符合預期"),
        ("P-02", "本案例的通用術語", "不列為逐字引用", "符合預期"),
        ("P-03", "沿用規則待確認", "停止生成正文", "符合預期"),
        ("P-04", "示範分級表＋來源", "依示範規則停止", "符合預期"),
    ]
    y = 322
    row_height = 112
    coords = [(80, 220), (240, 790), (810, 1270), (1290, 1520)]
    for index, row in enumerate(rows):
        fill = WHITE if index % 2 == 0 else "#EDF3F3"
        for column, ((x1, x2), value) in enumerate(zip(coords, row)):
            box(draw, (x1, y, x2, y + row_height - 12), fill=fill, outline="#D4DEE2", width=2, radius=12)
            color = TEAL if column in (0, 3) else INK
            draw_text(draw, ((x1 + x2) / 2, y + 49), value, 22, color, column in (0, 3),
                      max_width=x2 - x1 - 28, anchor="mm", align="center")
        y += row_height
    box(draw, (80, 786, 1520, 824), fill="#FBE8E4", radius=16)
    draw_text(draw, (800, 805), "走查結果不是模型測試；正式分級規則仍待組織核定", 22, CORAL, True, anchor="mm")
    footer(draw, 4)
    save(image, "day26-04-test-matrix.png")


def sop_flow():
    image, draw = canvas()
    header(draw, "Prompt 接入複核 SOP", "每個角色知道何時接手，也知道何時必須停止")
    stages = [
        ("1", "申請人", "核准來源\n與任務條件", TEAL),
        ("2", "執行人", "鎖定版本\n檢查輸入", GOLD),
        ("3", "AI 生成", "草稿＋\n來源對照", CORAL),
        ("4", "複核人", "來源／沿用／\n敏感資料", TEAL),
        ("5", "維護人", "失敗分類\n新版重測", NAVY),
    ]
    x_positions = [70, 375, 680, 985, 1290]
    y = 345
    for index, ((number, role, output, color), x) in enumerate(zip(stages, x_positions)):
        if index:
            arrow(draw, (x - 78, y + 118), (x - 18, y + 118), "#91A7B2", 5)
        box(draw, (x, y, x + 240, y + 238), fill=WHITE, outline=color, width=4, radius=24)
        draw.ellipse((x + 18, y + 18, x + 68, y + 68), fill=color)
        draw_text(draw, (x + 43, y + 43), number, 23, WHITE, True, anchor="mm")
        draw_text(draw, (x + 120, y + 96), role, 27, NAVY, True, anchor="mm")
        draw.line((x + 35, y + 132, x + 205, y + 132), fill="#D5DFE3", width=2)
        draw_text(draw, (x + 120, y + 181), output, 22, SLATE, anchor="mm", align="center", spacing=15)
    box(draw, (180, 680, 1420, 770), fill=NAVY, radius=24)
    draw_text(draw, (800, 711), "失敗不刪紀錄：保留原因、輸入識別碼與 Prompt 版本", 27, WHITE, True, anchor="mm")
    draw_text(draw, (800, 751), "跨客戶資料、敏感資訊或規則未核定 → 停止並升級", 22, "#C7D8DF", anchor="mm")
    footer(draw, 5)
    save(image, "day26-05-sop-flow.png")


if __name__ == "__main__":
    cover()
    chat_to_asset()
    prompt_contract()
    test_matrix()
    sop_flow()
    print("Generated 5 Day 26 images at 1600x900.")
