#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-assets" / "product-proofs"
OUT.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#121313")
COAL = colors.HexColor("#1B1D1E")
STEEL = colors.HexColor("#747A7D")
PAPER = colors.HexColor("#F1EDE3")
IVORY = colors.HexColor("#FBF8F0")
BRASS = colors.HexColor("#9A7947")
BRASS_LIGHT = colors.HexColor("#C1A26F")
OXBLOOD = colors.HexColor("#5C2528")
LINE = colors.HexColor("#D2CCBF")

SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SANS = "Helvetica"
SANS_M = "Helvetica-Bold"
SANS_B = "Helvetica-Bold"


def pdf(path: Path, pagesize: tuple[float, float]) -> canvas.Canvas:
    return canvas.Canvas(str(path), pagesize=pagesize, invariant=1, pageCompression=1)


def fit(text: str, font: str, max_size: float, min_size: float, width: float) -> float:
    size = max_size
    while size > min_size and pdfmetrics.stringWidth(text, font, size) > width:
        size -= 0.5
    return size


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        proposed = (current + " " + word).strip()
        if not current or pdfmetrics.stringWidth(proposed, font, size) <= width:
            current = proposed
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float,
                 font: str = SANS, size: float = 9, leading: float | None = None,
                 color=INK) -> float:
    leading = leading or size * 1.3
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def brand(c: canvas.Canvas, w: float, h: float, dark: bool = False) -> None:
    c.setFillColor(PAPER if dark else INK)
    c.setFont(SERIF_B, 8)
    c.drawString(0.33 * inch, h - 0.28 * inch, "FORGE & VERSE")
    c.setStrokeColor(BRASS)
    c.setLineWidth(1)
    c.line(0.33 * inch, h - 0.34 * inch, w - 0.33 * inch, h - 0.34 * inch)


def field(c: canvas.Canvas, x: float, y: float, w: float, h: float,
          label: str, lines: int = 2, accent: bool = False) -> None:
    c.setStrokeColor(BRASS if accent else LINE)
    c.setLineWidth(0.7)
    c.rect(x, y - h, w, h, stroke=1, fill=0)
    c.setFont(SANS_B, 6.2)
    c.setFillColor(BRASS if accent else STEEL)
    c.drawString(x + 5, y - 11, label.upper())
    if lines:
        c.setStrokeColor(colors.HexColor("#DAD4C9"))
        c.setLineWidth(0.35)
        top = y - 20
        gap = max(8, (h - 24) / lines)
        for i in range(lines):
            c.line(x + 5, top - i * gap, x + w - 5, top - i * gap)


def build_pad(filename: str, title: str, room: str, fields: list[dict],
              trim: tuple[float, float], state_markers: list[str]) -> None:
    bleed = 0.125
    W = (trim[0] + 2 * bleed) * inch
    H = (trim[1] + 2 * bleed) * inch
    c = pdf(OUT / filename, (W, H))
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    x0 = bleed * inch
    y0 = bleed * inch
    tw = trim[0] * inch

    brand(c, W, H)
    c.setFillColor(BRASS)
    c.setFont(SANS_B, 6.4)
    c.drawString(x0 + 10, H - 0.57 * inch, room.upper())
    size = fit(title, SERIF_B, 20, 14, tw - 20)
    c.setFont(SERIF_B, size)
    c.setFillColor(INK)
    c.drawString(x0 + 10, H - 0.88 * inch, title)

    y = H - 1.10 * inch
    c.setFont(SANS_B, 6.0)
    c.setFillColor(STEEL)
    c.drawString(x0 + 10, y, "STATE")
    x = x0 + 48
    for marker in state_markers:
        c.setStrokeColor(LINE)
        c.rect(x, y - 5, 9, 9, fill=0, stroke=1)
        c.setFont(SANS_M, 6.0)
        c.setFillColor(INK)
        c.drawString(x + 13, y - 3, marker)
        x += 16 + pdfmetrics.stringWidth(marker, SANS_M, 6.0)
    y -= 20

    gap = 6
    total_h = y - (y0 + 24)
    weights = [item.get("weight", 1) for item in fields]
    unit = (total_h - gap * (len(fields) - 1)) / sum(weights)
    for item in fields:
        fh = unit * item.get("weight", 1)
        field(c, x0 + 10, y, tw - 20, fh, item["label"],
              item.get("lines", 2), item.get("accent", False))
        y -= fh + gap

    c.setFont(SANS, 5.6)
    c.setFillColor(STEEL)
    c.drawString(
        x0 + 10, y0 + 7,
        "Working aid - not the official record. Follow local policy for retention, security, and disposal."
    )
    c.save()


def notebook_header(c: canvas.Canvas, w: float, h: float, room: str,
                    title: str, page_no: int) -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.45)
    c.line(0.55 * inch, h - 0.45 * inch, w - 0.45 * inch, h - 0.45 * inch)
    c.setFont(SANS_B, 6.0)
    c.setFillColor(STEEL)
    c.drawString(0.55 * inch, h - 0.34 * inch, room.upper())
    c.drawRightString(w - 0.45 * inch, h - 0.34 * inch, title.upper())
    c.line(0.55 * inch, 0.38 * inch, w - 0.45 * inch, 0.38 * inch)
    c.setFont(SANS, 5.8)
    c.drawRightString(w - 0.45 * inch, 0.24 * inch, str(page_no))


def cover(c: canvas.Canvas, w: float, h: float, room: str, title: str,
          kicker: str, subtitle: str, back: bool = False) -> None:
    c.setFillColor(INK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#343738"))
    c.setLineWidth(0.7)
    for i in range(6):
        x = w * (0.55 + i * 0.08)
        c.line(x, 0, x, h)
    c.setFillColor(OXBLOOD)
    c.rect(0.47 * inch, 0.6 * inch, 0.05 * inch, h - 1.2 * inch, fill=1, stroke=0)
    brand(c, w, h, dark=True)

    if back:
        c.setFillColor(BRASS_LIGHT)
        c.setFont(SANS_B, 7)
        c.drawString(0.72 * inch, 1.2 * inch, "FORGE & VERSE")
        c.setFillColor(colors.HexColor("#B8B4AC"))
        c.setFont(SANS, 7)
        c.drawString(0.72 * inch, 0.95 * inch, "Made for people whose work carries weight.")
        return

    c.setFillColor(BRASS_LIGHT)
    c.setFont(SANS_B, 7)
    c.drawString(0.72 * inch, h - 1.35 * inch, room.upper())
    c.setFillColor(PAPER)
    c.setFont(SERIF_B, 29)
    y = h - 2.0 * inch
    for line in wrap(title, SERIF_B, 29, w - 1.4 * inch):
        c.drawString(0.72 * inch, y, line)
        y -= 31
    y -= 10
    c.setFillColor(colors.HexColor("#D2CDC3"))
    c.setFont(SANS, 8.4)
    for line in wrap(subtitle, SANS, 8.4, w - 1.45 * inch):
        c.drawString(0.72 * inch, y, line)
        y -= 12
    c.setFillColor(BRASS)
    c.setFont(SANS_B, 6.4)
    c.drawString(0.72 * inch, 0.92 * inch, kicker.upper())


def structured_page(c: canvas.Canvas, w: float, h: float, room: str,
                    title: str, page_no: int, headline: str, fields: list[dict]) -> None:
    notebook_header(c, w, h, room, title, page_no)
    c.setFont(SERIF_B, 20)
    c.setFillColor(INK)
    c.drawString(0.65 * inch, h - 0.92 * inch, headline)
    y = h - 1.15 * inch
    for item in fields:
        fh = item.get("h", 0.68) * inch
        field(c, 0.65 * inch, y, w - 1.1 * inch, fh, item["label"],
              item.get("lines", 2), item.get("accent", False))
        y -= fh + 7


def writing_page(c: canvas.Canvas, w: float, h: float, room: str,
                 title: str, page_no: int, kind: str) -> None:
    notebook_header(c, w, h, room, title, page_no)
    x0 = 0.65 * inch
    x1 = w - 0.45 * inch
    ytop = h - 0.75 * inch
    ybot = 0.62 * inch

    if kind == "dot":
        c.setFillColor(colors.HexColor("#D6D1C7"))
        yy = ybot
        while yy < ytop:
            xx = x0
            while xx < x1:
                c.circle(xx, yy, 0.5, fill=1, stroke=0)
                xx += 18
            yy += 18
    elif kind == "open":
        c.setStrokeColor(colors.HexColor("#E0DAD0"))
        c.line(x0, ytop, x1, ytop)
    else:
        c.setStrokeColor(colors.HexColor("#DAD4C9"))
        c.setLineWidth(0.35)
        yy = ytop
        while yy > ybot:
            c.line(x0, yy, x1, yy)
            yy -= 22
        if kind == "margin":
            c.setStrokeColor(BRASS)
            c.line(x0 + 0.48 * inch, ytop, x0 + 0.48 * inch, ybot)


def build_notebook(filename: str, room: str, title: str, kicker: str,
                   subtitle: str, structure: list[dict], pages: int = 36) -> None:
    W = 5.5 * inch
    H = 8.5 * inch
    c = pdf(OUT / filename, (W, H))

    cover(c, W, H, room, title, kicker, subtitle)
    c.showPage()

    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    brand(c, W, H)
    c.setFont(SERIF_B, 13)
    c.setFillColor(INK)
    c.drawString(0.65 * inch, H - 1.05 * inch, "This notebook belongs to")
    c.setStrokeColor(LINE)
    c.line(0.65 * inch, H - 1.45 * inch, W - 0.6 * inch, H - 1.45 * inch)
    c.setFont(SANS, 7)
    c.setFillColor(STEEL)
    c.drawString(
        0.65 * inch, 0.65 * inch,
        "Working notes may be subject to local retention, discovery, security, and evidence-handling requirements."
    )
    c.showPage()

    page_no = 1
    for item in structure:
        structured_page(c, W, H, room, title, page_no, item["headline"], item["fields"])
        c.showPage()
        page_no += 1

    kinds = ["ruled", "margin", "dot", "open"]
    target_interiors = pages - 4
    for i in range(target_interiors - len(structure)):
        writing_page(c, W, H, room, title, page_no, kinds[(i // 6) % len(kinds)])
        c.showPage()
        page_no += 1

    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    brand(c, W, H)
    c.setFont(SERIF_B, 15)
    c.setFillColor(INK)
    c.drawString(0.65 * inch, H - 1.05 * inch, "Before this book closes")
    draw_wrapped(
        c,
        "Move anything that belongs in an official system, report, case file, ticket, incident record, or evidence record to the place your policy requires. Then retain or dispose of these working notes according to local rules.",
        0.65 * inch, H - 1.4 * inch, W - 1.25 * inch, SANS, 8.5, 11, STEEL
    )
    c.showPage()

    cover(c, W, H, room, title, kicker, subtitle, back=True)
    c.save()


def wall(filename: str, title: str, room: str, quote: str, body: str,
         orientation: str, motif: str) -> None:
    if orientation == "landscape":
        W, H = 12 * inch, 8 * inch
    else:
        W, H = 8 * inch, 12 * inch

    c = pdf(OUT / filename, (W, H))
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    if motif == "hash":
        c.setStrokeColor(colors.HexColor("#2D3031"))
        c.setLineWidth(1)
        for i in range(9):
            x = 0.5 * inch + i * (W - inch) / 8
            c.line(x, 0.55 * inch, x, H - 0.55 * inch)
        c.setFillColor(OXBLOOD)
        c.rect(W * 0.68, 0, W * 0.05, H, fill=1, stroke=0)
        c.setFont(SANS, 6)
        c.setFillColor(colors.HexColor("#61686B"))
        digest = "9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08"
        y = 0.75 * inch
        for chunk in [digest[i:i + 16] for i in range(0, len(digest), 16)]:
            c.drawString(W * 0.72, y, chunk)
            y += 12

    elif motif == "shelf":
        c.setStrokeColor(colors.HexColor("#474542"))
        c.setLineWidth(2)
        base = 0.75 * inch
        for r in range(4):
            y = base + r * 1.45 * inch
            c.line(W * 0.48, y, W - 0.55 * inch, y)
            for j in range(5):
                x = W * 0.5 + j * 0.85 * inch
                c.setFillColor(colors.HexColor("#27292A"))
                c.rect(x, y + 0.06 * inch, 0.68 * inch, 0.92 * inch, fill=1, stroke=0)
                c.setFillColor(BRASS if (r == 1 and j == 3) else colors.HexColor("#6C6A65"))
                c.rect(x + 0.07 * inch, y + 0.65 * inch, 0.34 * inch, 0.07 * inch, fill=1, stroke=0)

    elif motif == "watch":
        c.setStrokeColor(colors.HexColor("#343738"))
        c.setLineWidth(1)
        cx, cy, rr = W * 0.76, H * 0.5, min(W, H) * 0.25
        p = c.beginPath()
        p.moveTo(cx, cy + rr)
        p.lineTo(cx + rr * 0.62, cy + rr * 0.58)
        p.lineTo(cx + rr * 0.5, cy - rr * 0.45)
        p.lineTo(cx, cy - rr)
        p.lineTo(cx - rr * 0.5, cy - rr * 0.45)
        p.lineTo(cx - rr * 0.62, cy + rr * 0.58)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(OXBLOOD)
        c.rect(W * 0.67, 0, 0.07 * inch, H, fill=1, stroke=0)

    elif motif == "signal":
        nodes: list[tuple[float, float]] = []
        c.setStrokeColor(colors.HexColor("#323637"))
        c.setLineWidth(0.8)
        for row in range(5):
            for col in range(6):
                nodes.append((W * 0.55 + col * 0.65 * inch, 1.0 * inch + row * 1.15 * inch))
        for i, (x, y) in enumerate(nodes):
            if i + 1 < len(nodes) and (i + 1) % 6:
                c.line(x, y, nodes[i + 1][0], nodes[i + 1][1])
            if i + 6 < len(nodes):
                c.line(x, y, nodes[i + 6][0], nodes[i + 6][1])
        c.setFillColor(BRASS)
        for i, (x, y) in enumerate(nodes):
            c.circle(x, y, 3.2 if i in (4, 9, 16, 21) else 1.2, fill=1, stroke=0)

    brand(c, W, H, dark=True)
    left = 0.7 * inch
    maxw = W * 0.47 if orientation == "landscape" else W - 1.4 * inch

    c.setFillColor(BRASS_LIGHT)
    c.setFont(SANS_B, 7)
    c.drawString(left, H - 0.9 * inch, room.upper())

    size = fit(title, SERIF_B, 32, 20, maxw)
    c.setFillColor(PAPER)
    c.setFont(SERIF_B, size)
    y = H - 1.35 * inch
    for line in wrap(title, SERIF_B, size, maxw):
        c.drawString(left, y, line)
        y -= size * 1.02

    y -= 12
    qsize = 16 if len(quote) < 80 else 13
    c.setFillColor(BRASS_LIGHT)
    c.setFont(SERIF, qsize)
    for line in wrap(quote, SERIF, qsize, maxw):
        c.drawString(left, y, line)
        y -= qsize * 1.2

    y -= 8
    draw_wrapped(c, body, left, y, maxw, SANS, 7.9, 10.5, colors.HexColor("#B9B6AE"))
    c.setFillColor(colors.HexColor("#787B7C"))
    c.setFont(SANS_B, 5.8)
    c.drawString(left, 0.45 * inch, "STUDIO MATERIAL PROOF - NOT YET AN APPROVED EDITION")
    c.save()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    for child in OUT.iterdir():
        if child.is_file() and child.suffix.lower() in {".pdf", ".json"}:
            child.unlink()

    build_pad(
        "examiner-bench-status-pad-v0.4-4x6-bleed.pdf",
        "Bench Status", "The Examiner's Bench",
        [
            {"label": "Case / reference", "lines": 1, "weight": 0.65},
            {"label": "Current process / tool state", "lines": 2, "weight": 1.15},
            {"label": "Last completed action", "lines": 2},
            {"label": "Next intended action", "lines": 2},
            {"label": "Open loop / blocker", "lines": 2},
            {"label": "Critical context", "lines": 2, "weight": 1.05, "accent": True},
        ],
        (4, 6), ["Running", "Do not interrupt", "Blocked"]
    )

    build_pad(
        "evidence-custody-status-pad-v0.1-5x7-bleed.pdf",
        "Custody Status", "The Evidence Room",
        [
            {"label": "Case / project reference", "lines": 1, "weight": 0.7},
            {"label": "Current operational state", "lines": 2},
            {"label": "Action pending", "lines": 2},
            {"label": "Waiting on", "lines": 2},
            {"label": "Next check / follow-up", "lines": 1, "weight": 0.7},
            {"label": "Do not release or move until", "lines": 2},
            {"label": "Critical context / discrepancy", "lines": 2, "weight": 1.1, "accent": True},
        ],
        (5, 7), ["Pending", "Blocked", "Ready"]
    )

    build_pad(
        "watch-notes-pad-v0.1-5x7-bleed.pdf",
        "Watch Notes", "The Watch",
        [
            {"label": "Now", "lines": 3, "weight": 1.25, "accent": True},
            {"label": "Next", "lines": 2},
            {"label": "Waiting on", "lines": 2},
            {"label": "Need to tell someone", "lines": 2},
            {"label": "Before I leave", "lines": 3, "weight": 1.35},
        ],
        (5, 7), ["Active", "Waiting", "Handoff"]
    )

    build_pad(
        "signal-incident-status-pad-v0.1-5x7-bleed.pdf",
        "Incident Status", "The Signal",
        [
            {"label": "Incident / ticket", "lines": 1, "weight": 0.65},
            {"label": "Current condition", "lines": 2},
            {"label": "Containment / change in effect", "lines": 2},
            {"label": "Owner / decision maker", "lines": 1, "weight": 0.65},
            {"label": "Next action", "lines": 2},
            {"label": "Next checkpoint", "lines": 1, "weight": 0.65},
            {"label": "Do not change / fragile context", "lines": 2, "weight": 1.1, "accent": True},
        ],
        (5, 7), ["Investigating", "Contained", "Recovering"]
    )

    build_notebook(
        "examiner-examination-notebook-v0.4-5.5x8.5.pdf",
        "The Examiner's Bench", "Examination Notebook",
        "Case thinking / working notes", "Structure when needed. Space when it matters.",
        [
            {"headline": "Case orientation", "fields": [
                {"label": "Case / reference", "lines": 1},
                {"label": "Question being answered", "lines": 3, "h": 1.0},
                {"label": "Evidence sources in scope", "lines": 3, "h": 1.0},
                {"label": "Constraints / authority / time", "lines": 2, "h": 0.85},
            ]},
            {"headline": "Working index", "fields": [
                {"label": "Source / device / image", "lines": 2},
                {"label": "Tool / version / method", "lines": 2},
                {"label": "Open questions", "lines": 3, "h": 1.05},
                {"label": "Finding references", "lines": 3, "h": 1.05},
            ]},
            {"headline": "Pause / resume", "fields": [
                {"label": "Last completed", "lines": 2},
                {"label": "Current process", "lines": 2},
                {"label": "Next action", "lines": 2},
                {"label": "Critical context", "lines": 3, "h": 1.05, "accent": True},
            ]},
        ]
    )

    build_notebook(
        "evidence-working-ledger-v0.1-5.5x8.5.pdf",
        "The Evidence Room", "Working Ledger",
        "Room projects / operational notes", "For the work around the evidence system, not in place of it.",
        [
            {"headline": "Project orientation", "fields": [
                {"label": "Project / issue", "lines": 2},
                {"label": "Owner / partners", "lines": 2},
                {"label": "Current state", "lines": 2},
                {"label": "Next checkpoint", "lines": 2},
            ]},
            {"headline": "Decision log", "fields": [
                {"label": "Date / time", "lines": 1},
                {"label": "Decision / change", "lines": 3, "h": 1.05},
                {"label": "Why / authority / source", "lines": 3, "h": 1.05},
                {"label": "Follow-up", "lines": 2},
            ]},
            {"headline": "Open issues", "fields": [
                {"label": "Discrepancy / question", "lines": 3, "h": 1.05},
                {"label": "Waiting on", "lines": 2},
                {"label": "Next action", "lines": 2},
                {"label": "Due / checkpoint", "lines": 1},
            ]},
        ]
    )

    build_notebook(
        "watch-field-notebook-v0.1-5.5x8.5.pdf",
        "The Watch", "Field Notebook",
        "Operational notes / handoffs", "A place for the working thought before it moves to the official place.",
        [
            {"headline": "Shift orientation", "fields": [
                {"label": "Date / shift / assignment", "lines": 1},
                {"label": "Priorities", "lines": 3, "h": 1.05},
                {"label": "People / numbers", "lines": 3, "h": 1.05},
                {"label": "Pending handoff", "lines": 2},
            ]},
            {"headline": "Timeline", "fields": [
                {"label": "Start / end", "lines": 1},
                {"label": "Events / actions / decisions", "lines": 7, "h": 2.1},
                {"label": "Follow-up", "lines": 2},
            ]},
            {"headline": "Handoff", "fields": [
                {"label": "What is unfinished", "lines": 3, "h": 1.05},
                {"label": "Waiting on", "lines": 2},
                {"label": "Who needs to know", "lines": 2},
                {"label": "Before next shift", "lines": 2, "accent": True},
            ]},
        ]
    )

    build_notebook(
        "signal-incident-recovery-notebook-v0.1-5.5x8.5.pdf",
        "The Signal", "Incident & Recovery Notebook",
        "Technical incident working notes",
        "Keep the timeline, decisions, and fragile context visible when the screens are already full.",
        [
            {"headline": "Incident orientation", "fields": [
                {"label": "Incident / ticket", "lines": 1},
                {"label": "Observed condition", "lines": 3, "h": 1.05},
                {"label": "Affected systems / scope", "lines": 3, "h": 1.05},
                {"label": "Incident lead / comms path", "lines": 2},
            ]},
            {"headline": "Decision log", "fields": [
                {"label": "Time", "lines": 1},
                {"label": "Decision / change", "lines": 3, "h": 1.05},
                {"label": "Reason / evidence", "lines": 3, "h": 1.05},
                {"label": "Owner / follow-up", "lines": 2},
            ]},
            {"headline": "Recovery checkpoint", "fields": [
                {"label": "Current condition", "lines": 2},
                {"label": "Containment / safeguards", "lines": 2},
                {"label": "Next action", "lines": 2},
                {"label": "Do not change / preserve", "lines": 3, "h": 1.05, "accent": True},
            ]},
        ]
    )

    wall(
        "examiner-a-hash-is-a-promise-proof-8x12.pdf",
        "A Hash Is a Promise", "The Examiner's Bench",
        "Integrity is a claim supported by method.",
        "The value is not that the number looks scientific. The value is that another person can check the path from acquisition to examination and ask whether the evidence remained what we said it was.",
        "portrait", "hash"
    )
    wall(
        "evidence-preserved-until-it-matters-proof-12x8.pdf",
        "Preserved Until It Matters", "The Evidence Room",
        "Preservation gives truth time to catch up.",
        "An ordinary item can sit quietly for years before a new question gives it consequence. The work is making sure that future question is still possible.",
        "landscape", "shelf"
    )
    wall(
        "watch-believe-in-the-badge-proof-12x8.pdf",
        "Believe in the Badge", "The Watch",
        "Stand tall. Lead with heart. Keep showing up.",
        "The badge is not only authority. It is steadiness in a shaky moment, compassion when it would be easier to harden, and the decision to keep showing up when the work is difficult and unseen. Kindness is still legal in all 50 states.",
        "landscape", "watch"
    )
    wall(
        "signal-the-quiet-day-proof-12x8.pdf",
        "The Quiet Day", "The Signal",
        "Nothing happened today. That was the work.",
        "Quiet systems are rarely accidents. They are patches applied before the incident, backups tested before the failure, logs kept long enough to matter, and people making careful decisions while nothing dramatic is happening.",
        "landscape", "signal"
    )

    records = []
    for path in sorted(OUT.glob("*.pdf")):
        records.append({
            "file": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    (OUT / "manifest.json").write_text(
        json.dumps({"generated": "2026-11-15", "items": records}, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated {len(records)} product proof PDFs.")


if __name__ == "__main__":
    main()
