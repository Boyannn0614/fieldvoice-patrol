"""Create a deterministic four-zone field board with blue flood markers."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "simulated_field.png"

image = Image.new("RGB", (960, 640), (170, 213, 184))
draw = ImageDraw.Draw(image)
draw.line((480, 0, 480, 640), fill="white", width=16)
draw.line((0, 320, 960, 320), fill="white", width=16)

# Controlled blue markers: each zone has a different simulated water area.
draw.rectangle((80, 80, 190, 150), fill=(30, 120, 210))
draw.rectangle((600, 70, 890, 235), fill=(25, 115, 215))
draw.ellipse((135, 405, 285, 555), fill=(25, 125, 220))

labels = (("A", 24, 42), ("B", 504, 42), ("C", 24, 362), ("D", 504, 362))
for label, x, y in labels:
    draw.text((x, y), label, fill=(45, 65, 45), font=ImageFont.load_default())

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
image.save(OUTPUT)
print(OUTPUT)
