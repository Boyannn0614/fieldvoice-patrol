"""Detect blue color blocks used to simulate flooded areas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


REGIONS = ("top_left", "top_right", "bottom_left", "bottom_right")


def severity(ratio: float) -> str:
    if ratio >= 0.20:
        return "warning"
    if ratio >= 0.05:
        return "watch"
    return "normal"


def analyze(image: Image.Image) -> tuple[dict, Image.Image]:
    rgb = np.asarray(image.convert("RGB"))
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mask = (blue > 110) & (blue > red * 1.25) & (blue > green * 1.12)

    height, width = mask.shape
    boxes = (
        (0, 0, width // 2, height // 2),
        (width // 2, 0, width, height // 2),
        (0, height // 2, width // 2, height),
        (width // 2, height // 2, width, height),
    )
    annotated = image.copy()
    regions = []
    for name, (x1, y1, x2, y2) in zip(REGIONS, boxes):
        region_mask = mask[y1:y2, x1:x2]
        ratio = float(np.count_nonzero(region_mask)) / float(region_mask.size)
        level = severity(ratio)
        regions.append({"region": name, "blue_ratio": round(ratio, 4), "level": level})
        color = {"normal": (50, 160, 70), "watch": (230, 150, 10), "warning": (215, 35, 35)}[level]
        draw = ImageDraw.Draw(annotated)
        draw.rectangle((x1, y1, x2 - 1, y2 - 1), outline=color, width=4)
        draw.text((x1 + 12, y1 + 12), f"{name}: {ratio:.1%} {level}", fill=color, font=ImageFont.load_default())

    worst = max(regions, key=lambda item: item["blue_ratio"])
    result = {
        "method": "RGB blue-block simulation",
        "disclaimer": "Color blocks simulate standing water; this is not real-field water recognition.",
        "image_size": {"width": width, "height": height},
        "regions": regions,
        "highest_risk_region": worst["region"],
        "highest_blue_ratio": worst["blue_ratio"],
        "overall_level": worst["level"],
    }
    return result, annotated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output-image", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    try:
        image = Image.open(args.image).convert("RGB")
    except OSError as exc:
        raise SystemExit(f"Cannot read image: {args.image}") from exc
    result, annotated = analyze(image)

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.output_image:
        args.output_image.parent.mkdir(parents=True, exist_ok=True)
        annotated.save(args.output_image)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
