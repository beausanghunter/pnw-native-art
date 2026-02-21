# PNW Native Art Studio

An SVG-based drawing app for creating artwork in the style of **Pacific Northwest Coast** Native American artists such as Bill Reid, Robert Davidson, and Freda Diesing.

## Features

- **Circle tool** — click and drag to place circles (used as eyes, joints, and decorative elements in formline art)
- **Fill & stroke color pickers** — choose your palette
- **Stroke width control** — bold outlines are central to the formline tradition
- **Export to SVG** — save your vector artwork
- **Export to PDF** — A4-proportioned PDF via jsPDF + svg2pdf.js

## Running

Open `index.html` in any modern browser — no build step required.

```bash
open index.html   # macOS
xdg-open index.html  # Linux
```

Or serve locally:

```bash
npx serve .
# or
python3 -m http.server 8080
```

## Planned Shapes (formline vocabulary)

- **Ovoid** — the fundamental building block of formline design
- **U-form** — standard U-shaped element
- **Split-U** — U-form with inner void
- **Eye** — ovoid + inner circle (iris)
- **Claw / talon**
- **Feather groupings**

## References

- *Form and Freedom* — Bill Holm (definitive formline analysis)
- [Bill Reid Gallery](https://www.billreidgallery.ca)
- [Robert Davidson](https://www.robertdavidson.ca)
