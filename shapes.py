"""
shapes.py — Drawing primitives for PNW Native Art Studio.

Each function accepts an svgwrite.Drawing and returns an SVG element
that can be added to the drawing for export.

In Pacific Northwest Coast art, these geometric forms are the vocabulary
of formline design (per Bill Holm's analysis in Form and Freedom):
  - Circle  : eyes, joints, decorative dots
  - Ovoid   : (coming soon) the master shape of formline
  - U-form  : (coming soon) standard secondary element
  - Split-U : (coming soon) tertiary element with inner void
"""

import svgwrite


def draw_circle(
    drawing: svgwrite.Drawing,
    cx: float,
    cy: float,
    r: float,
    fill: str = "#c0392b",
    stroke: str = "#1a1a1a",
    stroke_width: float = 3,
) -> svgwrite.shapes.Circle:
    """Create an SVG <circle> element and return it.

    In PNW Coast art, circles appear as eye pupils, joint indicators,
    and repeating decorative motifs. They are typically rendered with
    a bold, dark outline and a saturated fill.

    Args:
        drawing:      An svgwrite.Drawing instance (used as an element factory).
        cx:           Centre x coordinate in SVG user units.
        cy:           Centre y coordinate in SVG user units.
        r:            Radius in SVG user units; clamped to a minimum of 1.
        fill:         CSS fill color string (hex, named, or rgb()).
        stroke:       CSS stroke color string.
        stroke_width: Stroke width in SVG user units.

    Returns:
        An svgwrite Circle element. Call ``drawing.add(el)`` to place it.

    Example:
        dwg = svgwrite.Drawing("out.svg", size=(800, 600))
        el  = draw_circle(dwg, cx=200, cy=300, r=50)
        dwg.add(el)
        dwg.save()
    """
    return drawing.circle(
        center=(cx, cy),
        r=max(1.0, r),
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )
