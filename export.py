"""
export.py — SVG and PDF export for PNW Native Art Studio.

export_svg  : writes shapes to a .svg file via svgwrite.
export_pdf  : renders shapes directly to a .pdf file via reportlab.
              (No intermediate SVG-to-PDF conversion — reportlab draws natively.)
"""

from __future__ import annotations
from typing import List

import svgwrite

from shapes import draw_circle

# Canvas background color (warm off-white, like birch bark)
BG_COLOR = "#fdf6e3"

# PDF page size — letter landscape (points: 1 pt = 1/72 in)
PDF_PAGE_W = 792  # 11 in
PDF_PAGE_H = 612  #  8.5 in


# ── Helpers ────────────────────────────────────────────────────────────────────

def _hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    """Convert '#rrggbb' to (r, g, b) floats in [0.0, 1.0]."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


# ── SVG export ─────────────────────────────────────────────────────────────────

def export_svg(
    shapes: List[dict],
    canvas_w: int,
    canvas_h: int,
    path: str,
) -> None:
    """Write all recorded shapes to an SVG file.

    Args:
        shapes:   List of shape dicts produced by the studio canvas.
        canvas_w: Canvas width in pixels.
        canvas_h: Canvas height in pixels.
        path:     Destination file path (e.g. "my-art.svg").
    """
    dwg = svgwrite.Drawing(path, size=(canvas_w, canvas_h))
    dwg.add(dwg.rect(insert=(0, 0), size=(canvas_w, canvas_h), fill=BG_COLOR))

    for s in shapes:
        if s["type"] == "circle":
            el = draw_circle(
                dwg,
                cx=s["cx"],
                cy=s["cy"],
                r=s["r"],
                fill=s["fill"],
                stroke=s["stroke"],
                stroke_width=s["stroke_width"],
            )
            dwg.add(el)

    dwg.save()


# ── PDF export ─────────────────────────────────────────────────────────────────

def export_pdf(
    shapes: List[dict],
    canvas_w: int,
    canvas_h: int,
    path: str,
) -> None:
    """Render all shapes to a PDF file using reportlab.

    The canvas is scaled to fit within a letter-landscape page while
    preserving aspect ratio.

    Args:
        shapes:   List of shape dicts produced by the studio canvas.
        canvas_w: Original canvas width in pixels.
        canvas_h: Original canvas height in pixels.
        path:     Destination file path (e.g. "my-art.pdf").
    """
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import Color

    scale = min(PDF_PAGE_W / canvas_w, PDF_PAGE_H / canvas_h)

    c = rl_canvas.Canvas(path, pagesize=(PDF_PAGE_W, PDF_PAGE_H))

    # Background
    bg = _hex_to_rgb01(BG_COLOR)
    c.setFillColorRGB(*bg)
    c.rect(0, 0, PDF_PAGE_W, PDF_PAGE_H, fill=1, stroke=0)

    for s in shapes:
        if s["type"] == "circle":
            fill_rgb   = _hex_to_rgb01(s["fill"])
            stroke_rgb = _hex_to_rgb01(s["stroke"])

            # Scale coordinates; flip y (reportlab origin = bottom-left)
            cx = s["cx"] * scale
            cy = PDF_PAGE_H - s["cy"] * scale
            r  = s["r"] * scale
            sw = max(0.5, s["stroke_width"] * scale)

            c.setFillColorRGB(*fill_rgb)
            c.setStrokeColorRGB(*stroke_rgb)
            c.setLineWidth(sw)
            c.circle(cx, cy, r, fill=1, stroke=1)

    c.save()
