from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1600, 900
ROOT = Path(__file__).parent
FONT_REGULAR = Path(r"C:\Windows\Fonts\msjh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msjhbd.ttc")

NAVY = "#0F172A"
WHITE = "#FFFFFF"
TEAL = "#14B8A6"
CYAN = "#22D3EE"
BLUE = "#3B82F6"
PURPLE = "#8B5CF6"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded(draw, box, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )


def label(draw, xy, value, size, fill, bold=False, anchor=None):
    draw.text(
        xy,
        value,
        font=font(size, bold),
        fill=fill,
        anchor=anchor,
    )


def arrow(draw, start, end, color=CYAN, width=8):
    draw.line([start, end], fill=color, width=width)
    end_x, end_y = end
    draw.polygon(
        [
            (end_x, end_y),
            (end_x - 22, end_y - 15),
            (end_x - 22, end_y + 15),
        ],
        fill=color,
    )


def cover():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.ellipse((1240, -190, 1770, 340), fill="#134E4A")
    draw.ellipse((-240, 640, 200, 1080), fill="#1E3A8A")

    label(draw, (115, 105), "DAY 12 · CODEX 基礎入門", 38, "#5EEAD4", True)
    label(draw, (115, 235), "讓 Codex 讀懂你的專案", 78, WHITE, True)
    label(
        draw,
        (115, 330),
        "把隱性默契寫成可執行、可驗證的規則",
        42,
        "#CBD5E1",
    )

    cards = [
        (115, "程式碼", "pom.xml · src/", BLUE),
        (610, "專案規則", "AGENTS.md", TEAL),
        (1105, "交付證據", "diff · test · risk", PURPLE),
    ]
    for x, title, note, color in cards:
        rounded(draw, (x, 540, x + 380, 710), "#1E293B", 24, color, 4)
        label(draw, (x + 190, 600), title, 34, color, True, "mm")
        label(draw, (x + 190, 662), note, 25, WHITE, False, "mm")

    arrow(draw, (520, 625), (595, 625))
    arrow(draw, (1015, 625), (1090, 625))
    image.save(ROOT / "day12-01-cover.png", format="PNG", optimize=True)


if __name__ == "__main__":
    cover()
