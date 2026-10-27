#!/usr/bin/env python3
"""Build the README demo GIF without external image assets."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 800
HEIGHT = 450
SCALE = 1
FRAMES = 54

INK = "#111827"
PAPER = "#F8FAFC"
PANEL = "#1F2937"
MUTED = "#94A3B8"
BLUE = "#2563EB"
GREEN = "#16A34A"
ORANGE = "#EA580C"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font(36, bold=True)
FONT_SUBTITLE = load_font(18)
FONT_LABEL = load_font(16, bold=True)
FONT_BODY = load_font(16)
FONT_SMALL = load_font(13)


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str,
    radius: int = 12,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_request(draw: ImageDraw.ImageDraw, progress: float) -> None:
    rounded_rect(draw, (52, 156, 344, 370), PAPER)
    draw.text((76, 178), "REQUEST", font=FONT_LABEL, fill=INK)
    lines = [
        "Add validated CSV import",
        "before any customer row",
        "is written to storage.",
        "",
        "Unknown: rejection behavior",
    ]
    visible_chars = int(sum(len(line) + 1 for line in lines) * progress)
    consumed = 0
    for index, line in enumerate(lines):
        remaining = max(0, visible_chars - consumed)
        shown = line[:remaining]
        consumed += len(line) + 1
        color = ORANGE if line.startswith("Unknown:") else INK
        draw.text((76, 218 + index * 26), shown, font=FONT_BODY, fill=color)


def draw_question(draw: ImageDraw.ImageDraw, opacity: float) -> None:
    value = int(255 * opacity)
    color = f"#{value:02x}{value:02x}{value:02x}"
    rounded_rect(draw, (372, 156, 748, 370), PANEL)
    draw.text((396, 178), "SCOPE QUESTION", font=FONT_LABEL, fill=color)
    draw.text((396, 218), "Should a malformed file", font=FONT_BODY, fill=color)
    draw.text((396, 244), "reject every row?", font=FONT_BODY, fill=color)
    draw.text((396, 290), "A  Reject all rows", font=FONT_BODY, fill=color)
    draw.text((396, 318), "B  Keep valid rows", font=FONT_BODY, fill=color)
    draw.text((396, 346), "Recommended: A", font=FONT_SMALL, fill=color)


def draw_scope(draw: ImageDraw.ImageDraw, revealed: int) -> None:
    rounded_rect(draw, (52, 142, 748, 386), "#FFFFFF")
    draw.text((76, 166), "SCOPE.md", font=FONT_LABEL, fill=INK)
    draw.text((612, 166), "V1.0", font=FONT_SMALL, fill=MUTED)
    fields = ["Goal", "Inputs / Outputs", "Must do", "Won't do", "Acceptance"]
    colors = [BLUE, ORANGE, GREEN, "#7C3AED", "#0891B2"]
    for index, (field, color) in enumerate(zip(fields, colors)):
        y = 208 + index * 32
        active = index < revealed
        bubble = color if active else "#E2E8F0"
        draw.ellipse((78, y + 2, 96, y + 20), fill=bubble)
        draw.text((110, y), field, font=FONT_BODY, fill=INK if active else MUTED)
        if active:
            draw.line((82, y + 12, 87, y + 17, 93, y + 7), fill="#FFFFFF", width=2)


def scale_font(font: ImageFont.FreeTypeFont) -> ImageFont.FreeTypeFont:
    path = getattr(font, "path", None)
    size = getattr(font, "size", 16)
    if path:
        return ImageFont.truetype(path, size=size * SCALE)
    return ImageFont.load_default()


def make_frame(index: int) -> Image.Image:
    canvas = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), "#E2E8F0")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH * SCALE, 118 * SCALE), fill=INK)
    draw.rectangle((0, 400 * SCALE, WIDTH * SCALE, HEIGHT * SCALE), fill=INK)
    draw.text(
        (52 * SCALE, 28 * SCALE),
        "SCOPE GATE",
        font=scale_font(FONT_TITLE),
        fill="#FFFFFF",
    )
    draw.text(
        (52 * SCALE, 77 * SCALE),
        "Close the scope before the code.",
        font=scale_font(FONT_SUBTITLE),
        fill="#CBD5E1",
    )

    if index < 14:
        draw_request(draw, min(1.0, index / 10))
    elif index < 25:
        draw_request(draw, 1.0)
        draw_question(draw, min(1.0, (index - 13) / 6))
    else:
        revealed = max(0, min(5, (index - 27) // 3))
        draw_scope(draw, revealed)
        if index >= 43:
            draw.text(
                (52 * SCALE, 414 * SCALE),
                "Scope closed. Design starts here.",
                font=scale_font(FONT_SUBTITLE),
                fill="#E2E8F0",
            )

    draw.text(
        (748 * SCALE, 420 * SCALE),
        "05 FIELDS",
        font=scale_font(FONT_SMALL),
        fill=MUTED,
        anchor="ra",
    )
    return canvas.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def build(output: Path) -> None:
    frames = [make_frame(index).quantize(colors=128) for index in range(FRAMES)]
    output.parent.mkdir(parents=True, exist_ok=True)
    durations = [90] * FRAMES
    durations[-1] = 1100
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("demo.gif"),
    )
    args = parser.parse_args()
    build(args.output.resolve())
    print(f"Wrote {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
