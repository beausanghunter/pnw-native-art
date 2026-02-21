"""
main.py — PNW Native Art Studio

A Tkinter desktop drawing app for creating artwork in the style of
Pacific Northwest Coast Native American artists (Bill Reid, Robert Davidson, etc.)

Run:
    python main.py
"""

import math
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.colorchooser import askcolor

from export import export_pdf, export_svg

# ── Canvas dimensions (SVG user units = screen pixels at 1:1) ─────────────────

CANVAS_W = 800
CANVAS_H = 600
BG_COLOR = "#fdf6e3"  # warm off-white (birch bark)


# ── Application ───────────────────────────────────────────────────────────────

class PNWArtStudio:
    """Main application window."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PNW Native Art Studio")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")

        # Current style
        self.fill_color   = "#c0392b"  # cedar red
        self.stroke_color = "#1a1a1a"  # charcoal
        self.stroke_width = 3

        # All committed shapes (used for SVG/PDF export)
        self.shapes: list[dict] = []

        # Drag state
        self._drag_start: tuple[int, int] | None = None
        self._preview_id: int | None = None

        self._build_ui()
        self.root.mainloop()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── Toolbar ────────────────────────────────────────────────────────────
        toolbar = tk.Frame(self.root, bg="#2a2420", pady=8)
        toolbar.pack(fill="x", padx=8, pady=(8, 0))

        # Fill color
        tk.Label(toolbar, text="Fill:", bg="#2a2420", fg="#c8b89a",
                 font=("Georgia", 10)).pack(side="left", padx=(8, 2))
        self.fill_btn = tk.Button(
            toolbar, bg=self.fill_color, width=3,
            command=self._pick_fill, relief="solid", bd=1,
        )
        self.fill_btn.pack(side="left", padx=(0, 12))

        # Stroke color
        tk.Label(toolbar, text="Stroke:", bg="#2a2420", fg="#c8b89a",
                 font=("Georgia", 10)).pack(side="left", padx=(0, 2))
        self.stroke_btn = tk.Button(
            toolbar, bg=self.stroke_color, width=3,
            command=self._pick_stroke, relief="solid", bd=1,
        )
        self.stroke_btn.pack(side="left", padx=(0, 12))

        # Stroke width
        tk.Label(toolbar, text="Width:", bg="#2a2420", fg="#c8b89a",
                 font=("Georgia", 10)).pack(side="left", padx=(0, 2))
        self._width_var = tk.IntVar(value=self.stroke_width)
        tk.Scale(
            toolbar, from_=1, to=20, orient="horizontal",
            variable=self._width_var, length=90,
            bg="#2a2420", fg="#c8b89a", highlightthickness=0, showvalue=True,
            command=lambda v: setattr(self, "stroke_width", int(v)),
        ).pack(side="left", padx=(0, 16))

        # Action buttons
        for label, cmd, bg, fg in [
            ("Clear",      self._clear,      "#3d3028", "#e0d6c8"),
            ("Export SVG", self._export_svg, "#3d3028", "#e0d6c8"),
            ("Export PDF", self._export_pdf, "#7a4020", "#ffe0c8"),
        ]:
            tk.Button(
                toolbar, text=label, command=cmd,
                bg=bg, fg=fg, relief="flat", padx=10,
                font=("Georgia", 10),
            ).pack(side="left", padx=2)

        # ── Drawing canvas ─────────────────────────────────────────────────────
        canvas_frame = tk.Frame(self.root, bg="#1a1a1a")
        canvas_frame.pack(padx=8, pady=8)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=CANVAS_W, height=CANVAS_H,
            bg=BG_COLOR, cursor="crosshair",
            highlightthickness=1, highlightbackground="#3d3028",
        )
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<B1-Motion>",        self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        # ── Status bar ─────────────────────────────────────────────────────────
        status_frame = tk.Frame(self.root, bg="#1a1a1a")
        status_frame.pack(fill="x", padx=8, pady=(0, 8))

        self._status = tk.StringVar(value="Click and drag to draw a circle.")
        tk.Label(
            status_frame, textvariable=self._status,
            bg="#1a1a1a", fg="#6a5a4a", font=("Georgia", 10),
        ).pack(side="left")

    # ── Color pickers ──────────────────────────────────────────────────────────

    def _pick_fill(self) -> None:
        color = askcolor(color=self.fill_color, title="Fill Color")[1]
        if color:
            self.fill_color = color
            self.fill_btn.configure(bg=color)

    def _pick_stroke(self) -> None:
        color = askcolor(color=self.stroke_color, title="Stroke Color")[1]
        if color:
            self.stroke_color = color
            self.stroke_btn.configure(bg=color)

    # ── Mouse interaction ──────────────────────────────────────────────────────

    def _on_press(self, evt: tk.Event) -> None:
        self._drag_start = (evt.x, evt.y)

    def _on_drag(self, evt: tk.Event) -> None:
        if self._drag_start is None:
            return
        x0, y0 = self._drag_start
        r = math.hypot(evt.x - x0, evt.y - y0)

        if self._preview_id is not None:
            self.canvas.delete(self._preview_id)

        # Dashed preview ring
        self._preview_id = self.canvas.create_oval(
            x0 - r, y0 - r, x0 + r, y0 + r,
            outline=self.stroke_color, fill="", width=1, dash=(4, 4),
        )

    def _on_release(self, evt: tk.Event) -> None:
        if self._drag_start is None:
            return

        if self._preview_id is not None:
            self.canvas.delete(self._preview_id)
            self._preview_id = None

        x0, y0 = self._drag_start
        r = math.hypot(evt.x - x0, evt.y - y0)
        self._drag_start = None

        if r < 2:
            return  # ignore accidental clicks

        # Commit shape to the Tkinter canvas
        self.canvas.create_oval(
            x0 - r, y0 - r, x0 + r, y0 + r,
            outline=self.stroke_color,
            fill=self.fill_color,
            width=self.stroke_width,
        )

        # Record for SVG/PDF export
        self.shapes.append({
            "type":         "circle",
            "cx":           x0,
            "cy":           y0,
            "r":            r,
            "fill":         self.fill_color,
            "stroke":       self.stroke_color,
            "stroke_width": self.stroke_width,
        })

        self._status.set(
            f"Circle — centre ({int(x0)}, {int(y0)}), "
            f"radius {int(r)}px  |  {len(self.shapes)} shape(s)"
        )

    # ── Actions ────────────────────────────────────────────────────────────────

    def _clear(self) -> None:
        self.canvas.delete("all")
        self.shapes.clear()
        self._status.set("Canvas cleared.")

    def _export_svg(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg")],
            initialfile="pnw-art.svg",
        )
        if path:
            export_svg(self.shapes, CANVAS_W, CANVAS_H, path)
            self._status.set(f"SVG saved → {path}")

    def _export_pdf(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="pnw-art.pdf",
        )
        if path:
            try:
                export_pdf(self.shapes, CANVAS_W, CANVAS_H, path)
                self._status.set(f"PDF saved → {path}")
            except Exception as exc:
                messagebox.showerror("Export Error", str(exc))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    PNWArtStudio()
