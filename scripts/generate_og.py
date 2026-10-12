from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og-preview.png"

WIDTH, HEIGHT = 1200, 630
PAPER = "#f2efe6"
INK = "#13201d"
MUTED = "#63706b"
BLUE = "#3157ff"
LIME = "#c8ff52"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


regular = ROOT / "assets" / "fonts" / "lato-regular.ttf"
bold = ROOT / "assets" / "fonts" / "lato-bold.ttf"
serif_candidates = [
    Path("/System/Library/Fonts/Supplemental/Georgia.ttf"),
    Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
]
serif = next((path for path in serif_candidates if path.exists()), regular)

canvas = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
draw = ImageDraw.Draw(canvas)

# Quiet scientific-paper grid.
for x in range(0, WIDTH, 40):
    draw.line((x, 0, x, HEIGHT), fill="#e1ded4", width=1)
for y in range(0, HEIGHT, 40):
    draw.line((0, y, WIDTH, y), fill="#e1ded4", width=1)

# Thin spectral/orbital lines behind the portrait.
draw.ellipse((710, -140, 1260, 520), outline="#d8d3ff", width=2)
draw.ellipse((820, 330, 1270, 780), outline="#d9f5a1", width=3)

draw.text((64, 54), "CHENGCHUN LIU", font=font(bold, 22), fill=INK)
draw.ellipse((278, 61, 290, 73), fill=BLUE)
draw.ellipse((296, 61, 308, 73), fill=LIME)

headline_font = font(serif, 92)
italic_font_path = Path("/System/Library/Fonts/Supplemental/Georgia Italic.ttf")
italic_font = font(italic_font_path if italic_font_path.exists() else serif, 82)
draw.text((64, 130), "AI for chemistry.", font=headline_font, fill=INK)
draw.text((116, 229), "Built to reason.", font=italic_font, fill=BLUE)

body = "Molecular spectra · geometric learning · scientific agents"
draw.text((68, 365), body, font=font(regular, 27), fill=MUTED)

draw.rounded_rectangle((64, 440, 386, 510), radius=35, fill=INK)
draw.text((95, 462), "Research portfolio", font=font(bold, 21), fill=PAPER)
draw.text((339, 459), "↗", font=font(bold, 25), fill=LIME)

draw.text((66, 555), "Peking University  ·  AI for Chemistry", font=font(bold, 18), fill=INK)

# Portrait card.
photo = Image.open(ROOT / "assets" / "chengchun-liu.jpg").convert("RGB")
target_w, target_h = 312, 416
scale = max(target_w / photo.width, target_h / photo.height)
resized = photo.resize((round(photo.width * scale), round(photo.height * scale)), Image.Resampling.LANCZOS)
left = (resized.width - target_w) // 2
top = max(0, (resized.height - target_h) // 4)
portrait = resized.crop((left, top, left + target_w, top + target_h))

card = Image.new("RGBA", (352, 516), (255, 255, 255, 175))
card_draw = ImageDraw.Draw(card)
card_draw.rounded_rectangle((0, 0, 351, 515), radius=24, fill=(255, 255, 255, 190), outline=(19, 32, 29, 45), width=2)
mask = Image.new("L", (target_w, target_h), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle((0, 0, target_w, target_h), radius=15, fill=255)
card.paste(portrait, (20, 20), mask)
card_draw.text((22, 458), "Ph.D. researcher · Peking University", font=font(bold, 16), fill=INK)
card_draw.text((22, 485), "Beijing · UTC+8", font=font(regular, 15), fill=MUTED)

canvas.paste(card, (790, 58), card)

draw.ellipse((1070, 422, 1124, 476), fill=LIME, outline=INK, width=2)
draw.text((1081, 431), "C", font=font(serif, 31), fill=INK)

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, format="PNG", optimize=True)
print(OUT)

