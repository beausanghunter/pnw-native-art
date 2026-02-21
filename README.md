# PNW Native Art Studio

A Python desktop drawing app for creating artwork in the style of
**Pacific Northwest Coast** Native American artists such as Bill Reid,
Robert Davidson, and Freda Diesing.

Built with **Tkinter** (Python's standard GUI library — no JavaScript required),
**svgwrite** for SVG export, and **reportlab** for PDF export.

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the app
python main.py
```

## How to draw

1. **Click and drag** on the canvas — drag distance sets the radius.
2. Adjust **Fill**, **Stroke**, and **Width** in the toolbar before drawing.
3. Hit **Export SVG** or **Export PDF** to save your work.

## Project layout

```
pnw-native-art/
├── main.py          # App entry point — Tkinter window and canvas
├── shapes.py        # Shape primitives: draw_circle(), (ovoid, u-form coming soon)
├── export.py        # export_svg() and export_pdf()
└── requirements.txt
```

## Planned formline vocabulary

| Shape     | Role in formline art                        | Status      |
|-----------|---------------------------------------------|-------------|
| Circle    | Eyes, joints, decorative dots               | Done        |
| Ovoid     | Master primary form — all major body masses | Coming soon |
| U-form    | Standard secondary element                  | Coming soon |
| Split-U   | Tertiary element with inner void            | Coming soon |
| Eye       | Ovoid + inner circle (iris)                 | Coming soon |

## References

- *Form and Freedom* — Bill Holm (definitive formline analysis)
- [Bill Reid Gallery](https://www.billreidgallery.ca)
- [Robert Davidson](https://www.robertdavidson.ca)
