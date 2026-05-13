from PIL import Image, ImageDraw, ImageFont

SIZE = 400
img = Image.new("RGBA", (SIZE, SIZE))
draw = ImageDraw.Draw(img)

for y in range(SIZE):
    t = y / SIZE
    r = int(26 + (22 - 26) * t)
    g = int(10 + (33 - 10) * t)
    b = int(46 + (62 - 46) * t)
    draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

cx, cy = 200, 150
dw, dh = 130, 160
draw.rounded_rectangle(
    [cx - dw//2, cy - dh//2, cx + dw//2, cy + dh//2],
    radius=12, fill=(124, 58, 237, 242)
)

lines = [(90, -45), (70, -28), (80, -11), (55, 6), (65, 23), (40, 40)]
for w, yo in lines:
    x0 = cx - w // 2
    y0 = cy + yo
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + 6], radius=3, fill=(255, 255, 255, 128))

fcx, fcy = cx + 80, cy - 60
draw.ellipse([fcx - 20, fcy - 20, fcx + 20, fcy + 20], fill=(251, 191, 36))
pts = [(fcx - 5, fcy - 8), (fcx - 8, fcy + 1), (fcx - 2, fcy + 1), (fcx - 6, fcy + 11)]
draw.line(pts, fill=(26, 10, 46), width=3)

try:
    font = ImageFont.truetype("segoeui.ttf", 36)
except:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), "Prompt Templates", font=font)
tx = (SIZE - (bbox[2] - bbox[0])) // 2
draw.text((tx, 290), "Prompt Templates", fill=(226, 232, 240), font=font)

img.save("logo.png")
print("logo.png created")
