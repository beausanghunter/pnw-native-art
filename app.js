/**
 * PNW Native Art Studio
 *
 * SVG drawing app inspired by Pacific Northwest Coast art traditions
 * (formline, ovoids, U-forms, split-U forms, etc.)
 *
 * Currently supported shapes:
 *   - Circle (drawCircle)
 *
 * More formline primitives to come.
 */

'use strict';

// ── State ─────────────────────────────────────────────────────────────────────

const state = {
  tool: 'circle',
  fillColor: '#c0392b',
  strokeColor: '#1a1a1a',
  strokeWidth: 3,
  // drag tracking
  dragging: false,
  startX: 0,
  startY: 0,
};

// ── DOM refs ──────────────────────────────────────────────────────────────────

const canvas        = document.getElementById('canvas');
const drawingLayer  = document.getElementById('drawing-layer');
const previewLayer  = document.getElementById('preview-layer');
const statusMsg     = document.getElementById('status-msg');
const coordsDisplay = document.getElementById('coords');

// ── Drawing primitives ────────────────────────────────────────────────────────

/**
 * drawCircle — create an SVG <circle> element.
 *
 * In PNW Coast art, circles appear as eyes, joints, and decorative elements.
 * They are typically rendered with a bold stroke and a contrasting fill.
 *
 * @param {number} cx        - Centre x coordinate (SVG user units)
 * @param {number} cy        - Centre y coordinate (SVG user units)
 * @param {number} r         - Radius (SVG user units); clamped to >= 1
 * @param {object} [opts]    - Optional style overrides
 * @param {string} [opts.fill]        - CSS fill color  (default: state.fillColor)
 * @param {string} [opts.stroke]      - CSS stroke color (default: state.strokeColor)
 * @param {number} [opts.strokeWidth] - Stroke width     (default: state.strokeWidth)
 * @returns {SVGCircleElement}
 */
function drawCircle(cx, cy, r, opts = {}) {
  const fill        = opts.fill        ?? state.fillColor;
  const stroke      = opts.stroke      ?? state.strokeColor;
  const strokeWidth = opts.strokeWidth ?? state.strokeWidth;

  const el = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  el.setAttribute('cx', cx);
  el.setAttribute('cy', cy);
  el.setAttribute('r', Math.max(1, r));
  el.setAttribute('fill', fill);
  el.setAttribute('stroke', stroke);
  el.setAttribute('stroke-width', strokeWidth);
  return el;
}

// ── SVG coordinate helper ─────────────────────────────────────────────────────

function svgPoint(evt) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.viewBox.baseVal.width  / rect.width;
  const scaleY = canvas.viewBox.baseVal.height / rect.height;
  return {
    x: (evt.clientX - rect.left) * scaleX,
    y: (evt.clientY - rect.top)  * scaleY,
  };
}

// ── Canvas interaction ────────────────────────────────────────────────────────

canvas.addEventListener('mousedown', (evt) => {
  if (evt.button !== 0) return;
  const pt = svgPoint(evt);
  state.dragging = true;
  state.startX = pt.x;
  state.startY = pt.y;
  evt.preventDefault();
});

canvas.addEventListener('mousemove', (evt) => {
  const pt = svgPoint(evt);
  coordsDisplay.textContent = `x: ${Math.round(pt.x)}  y: ${Math.round(pt.y)}`;

  if (!state.dragging) return;

  // Show live preview
  previewLayer.innerHTML = '';

  if (state.tool === 'circle') {
    const dx = pt.x - state.startX;
    const dy = pt.y - state.startY;
    const r  = Math.hypot(dx, dy);
    const preview = drawCircle(state.startX, state.startY, r, {
      fill: state.fillColor + '99', // semi-transparent preview
    });
    previewLayer.appendChild(preview);
  }
});

canvas.addEventListener('mouseup', (evt) => {
  if (!state.dragging) return;
  state.dragging = false;
  previewLayer.innerHTML = '';

  const pt = svgPoint(evt);

  if (state.tool === 'circle') {
    const dx = pt.x - state.startX;
    const dy = pt.y - state.startY;
    const r  = Math.hypot(dx, dy);
    if (r < 2) return; // ignore accidental clicks
    const circle = drawCircle(state.startX, state.startY, r);
    drawingLayer.appendChild(circle);
    statusMsg.textContent = `Circle added — centre (${Math.round(state.startX)}, ${Math.round(state.startY)}), radius ${Math.round(r)}px.`;
  }
});

canvas.addEventListener('mouseleave', () => {
  if (state.dragging) {
    state.dragging = false;
    previewLayer.innerHTML = '';
  }
  coordsDisplay.textContent = '';
});

// ── Toolbar controls ──────────────────────────────────────────────────────────

document.getElementById('btn-circle').addEventListener('click', () => {
  state.tool = 'circle';
  statusMsg.textContent = 'Click and drag on the canvas to draw a circle.';
});

document.getElementById('fill-color').addEventListener('input', (e) => {
  state.fillColor = e.target.value;
});

document.getElementById('stroke-color').addEventListener('input', (e) => {
  state.strokeColor = e.target.value;
});

const strokeWidthInput = document.getElementById('stroke-width');
const strokeWidthVal   = document.getElementById('stroke-width-val');
strokeWidthInput.addEventListener('input', (e) => {
  state.strokeWidth = Number(e.target.value);
  strokeWidthVal.textContent = e.target.value;
});

document.getElementById('btn-clear').addEventListener('click', () => {
  drawingLayer.innerHTML  = '';
  previewLayer.innerHTML  = '';
  statusMsg.textContent   = 'Canvas cleared.';
});

// ── Export: SVG ───────────────────────────────────────────────────────────────

document.getElementById('btn-export-svg').addEventListener('click', () => {
  const serializer = new XMLSerializer();
  const svgStr = serializer.serializeToString(canvas);
  const blob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' });
  triggerDownload(blob, 'pnw-art.svg');
  statusMsg.textContent = 'SVG exported.';
});

// ── Export: PDF ───────────────────────────────────────────────────────────────

document.getElementById('btn-export-pdf').addEventListener('click', async () => {
  statusMsg.textContent = 'Generating PDF…';
  try {
    const { jsPDF } = window.jspdf;

    // Canvas dimensions in SVG user units
    const svgWidth  = canvas.viewBox.baseVal.width;
    const svgHeight = canvas.viewBox.baseVal.height;

    // Page size in mm (keep same aspect ratio)
    const mmWidth  = 297;  // A4 landscape width
    const mmHeight = Math.round(svgHeight / svgWidth * mmWidth);

    const pdf = new jsPDF({
      orientation: mmWidth > mmHeight ? 'landscape' : 'portrait',
      unit: 'mm',
      format: [mmWidth, mmHeight],
    });

    await pdf.svg(canvas, { x: 0, y: 0, width: mmWidth, height: mmHeight });
    pdf.save('pnw-art.pdf');
    statusMsg.textContent = 'PDF exported.';
  } catch (err) {
    console.error(err);
    statusMsg.textContent = 'PDF export failed — see console for details.';
  }
});

// ── Utility ───────────────────────────────────────────────────────────────────

function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href     = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
