from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-assets" / "prototypes"
DOWNLOADS = ROOT / "static" / "downloads" / "studio-proofs"
DOWNLOADS.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#1D1F20")
BRASS = colors.HexColor("#9B7438")
MUTED = colors.HexColor("#666C70")
LINE = colors.HexColor("#CBC3B5")
PALE = colors.HexColor("#F4F0E7")
WHITE = colors.white

styles = getSampleStyleSheet()
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.1, leading=12.4, textColor=INK, spaceAfter=5)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.7, leading=10.1, textColor=MUTED)
EYEBROW = ParagraphStyle("Eyebrow", parent=BODY, fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=BRASS, spaceAfter=4)
TITLE = ParagraphStyle("Title", parent=BODY, fontName="Times-Bold", fontSize=24, leading=27, textColor=INK, spaceAfter=6)
LEDE = ParagraphStyle("Lede", parent=BODY, fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=BODY, fontName="Times-Bold", fontSize=14, leading=17, textColor=INK, spaceBefore=8, spaceAfter=5)
CHECK = ParagraphStyle("Check", parent=BODY, leftIndent=14, firstLineIndent=-14, spaceAfter=4)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header_footer(c: canvas.Canvas, doc: BaseDocTemplate, label: str, version: str) -> None:
    width, height = letter
    c.saveState()
    c.setStrokeColor(BRASS); c.setLineWidth(0.8); c.line(0.62 * inch, height - 0.46 * inch, width - 0.62 * inch, height - 0.46 * inch)
    c.setFont("Times-Bold", 7.5); c.setFillColor(INK); c.drawString(0.62 * inch, height - 0.36 * inch, "FORGE & VERSE")
    c.setFont("Helvetica-Bold", 6.4); c.setFillColor(MUTED); c.drawRightString(width - 0.62 * inch, height - 0.36 * inch, label.upper())
    c.setStrokeColor(LINE); c.setLineWidth(0.45); c.line(0.62 * inch, 0.48 * inch, width - 0.62 * inch, 0.48 * inch)
    c.setFont("Helvetica", 6.8); c.setFillColor(MUTED); c.drawString(0.62 * inch, 0.32 * inch, f"Studio proof {version} | Evaluation only")
    c.drawRightString(width - 0.62 * inch, 0.32 * inch, f"Page {doc.page}")
    c.restoreState()


def build_doc(path: Path, story: list, label: str, version: str) -> None:
    doc = BaseDocTemplate(str(path), pagesize=letter, leftMargin=0.64 * inch, rightMargin=0.64 * inch, topMargin=0.67 * inch, bottomMargin=0.66 * inch, title=label, author="Forge & Verse")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="proof", frames=[frame], onPage=lambda c, d: header_footer(c, d, label, version))])
    def deterministic_canvas(filename: str, pagesize=None, **kwargs):
        kwargs.pop("invariant", None); kwargs.pop("pageCompression", None)
        return canvas.Canvas(filename, pagesize=pagesize, invariant=1, pageCompression=1, **kwargs)
    doc.build(story, canvasmaker=deterministic_canvas)


def callout(label: str, text: str) -> Table:
    content = [Paragraph(label.upper(), EYEBROW), Paragraph(text, ParagraphStyle("CalloutBody", parent=BODY, textColor=WHITE, fontSize=10, leading=13))]
    table = Table([[content]], colWidths=[7.18 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INK), ("BOX", (0, 0), (-1, -1), 0.5, LINE), ("LINEABOVE", (0, 0), (-1, 0), 1.2, BRASS),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def checklist(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"[ ] {item}", CHECK) for item in items]


def rating_table(rows: list[tuple[str, str]]) -> Table:
    data = [[Paragraph("TEST", EYEBROW), Paragraph("NOTES", EYEBROW), Paragraph("1-5", EYEBROW)]]
    for title, prompt in rows:
        data.append([Paragraph(f'<b>{title}</b><br/><font size="7.5" color="#666C70">{prompt}</font>', BODY), Paragraph("_______________________________________________________________<br/>_______________________________________________________________", SMALL), Paragraph("____", BODY)])
    table = Table(data, colWidths=[1.95 * inch, 4.55 * inch, 0.68 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("GRID", (0, 0), (-1, -1), 0.45, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 1), (-1, -1), 8), ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]))
    return table


def bench_story() -> list:
    return [
        Paragraph("THE EXAMINER'S BENCH", EYEBROW), Paragraph("Bench Status Pad Field Test 0.3", TITLE),
        Paragraph("A refined 4 x 6 continuity proof built to survive ordinary handwriting, active-process risk, and the last five minutes of a shift.", LEDE),
        callout("What changed", "Version 0.3 removes the ambiguous Safe to resume marker, adds an actionable Do not interrupt marker, replaces Do not forget with Critical context, and redistributes writing room after three representative desk simulations. This is not practitioner field validation yet."), Spacer(1, 8),
        Paragraph("Run the interruption test", H2), *checklist([
            "Print the exact 4 x 6 proof at 100 percent / Actual Size.", "Use fictitious or sanitized information unless your agency has approved a test.",
            "Complete the card during the final five minutes of a realistic work session.", "Leave the card out of sight for at least two hours; overnight or a weekend is better.",
            "Start a timer before reading it. Stop when you can state the current process, last completed action, next action, and open loop.", "Target: accurate re-entry in under thirty seconds without reopening full notes first.",
        ]),
        Paragraph("Stress the two risky moments", H2),
        Paragraph("<b>Process still running:</b> mark Process running and, only when true, Do not interrupt. A checkbox that does not change behavior does not deserve to stay.", BODY),
        Paragraph("<b>Blocked work:</b> mark Blocked and use Open loop / blocker for the dependency. Critical context is for the fragile detail that does not naturally belong in another field.", BODY),
        PageBreak(), Paragraph("Evaluation sheet", TITLE), Paragraph("A small card earns its place only if it saves more reconstruction time than it costs to complete.", LEDE),
        rating_table([("Return speed", "Measured seconds until the examination state is clear."), ("Writing room", "Normal handwriting fits without shrinking into note-card script."),
                      ("State markers", "Running / Do not interrupt / Blocked alter behavior rather than decorate the page."), ("Next action", "The first move on return is obvious."),
                      ("Open loop", "A dependency or unresolved question remains intelligible later."), ("Critical context", "The final field captures something useful that no other field owns.")]),
        Spacer(1, 8), Paragraph("Verdict", H2), Paragraph("Measured return time: __________________ seconds", BODY), Paragraph("Field that felt cramped: _________________________________________________", BODY),
        Paragraph("Field that could disappear: ______________________________________________", BODY), Paragraph("Overall: [ ] another test  [ ] revise before testing again  [ ] wrong format", BODY),
    ]


def notebook_story() -> list:
    return [
        Paragraph("THE EXAMINER'S BENCH", EYEBROW), Paragraph("Examination Notebook Field Test 0.3", TITLE),
        Paragraph("A 32-page, 5.5 x 8.5 production-oriented dummy that keeps guided structure near 16 percent of the interior and gives the rest back to handwriting.", LEDE),
        callout("What changed", "Version 0.3 compresses seven structured pages into five, introduces mirrored gutter margins for a bound object, expands the dummy from 12 to 32 pages, and separates four working-page treatments into deliberate test runs. It is still a field proof, not an approved case notebook."), Spacer(1, 8),
        Paragraph("What to test", H2), *checklist([
            "Print double-sided at 100 percent, or inspect at exact trim size if your printer cannot duplex half-letter stock.", "Use at least three ordinary pens. Record bleed-through, feathering, drag, and dry time.",
            "Use the case-orientation, source-index, working-index, and pause pages only when they help; skipped structure is useful evidence.", "Spend at least twenty minutes each on ruled, ruled-with-margin, dot-grid, and open pages.",
            "Hold or clip the stack as if it were bound. Judge whether the mirrored gutter leaves enough hand room.", "Confirm how handwritten notes are treated under your agency and court/discovery practice before any real-case pilot.",
        ]),
        Paragraph("The design target", H2), Paragraph("The front matter should orient the work without becoming paper software. Across the 31-page interior after the cover, 26 pages are open working pages (83.9 percent).", BODY),
        PageBreak(), Paragraph("Evaluation sheet", TITLE), Paragraph("This proof is trying to answer physical questions now: trim, gutter, ruling, page mix, paper behavior, and whether the compressed indexes are enough.", LEDE),
        rating_table([("Trim", "Does 5.5 x 8.5 feel portable without making diagrams cramped?"), ("Gutter", "Can the inner edge be used comfortably when the pages are bound?"),
                      ("Front matter", "Do five structured pages orient the case without duplicating software?"), ("Ruling", "Which page treatment disappears best while you work?"),
                      ("Page mix", "Would you carry a mixed interior or prefer a single ruling style?"), ("Pen / paper", "Which pens expose bleed, feathering, show-through, or drag?")]),
        Spacer(1, 8), Paragraph("Working-page preference", H2), Paragraph("[ ] Light ruled   [ ] Ruled + margin   [ ] Dot grid   [ ] Open   [ ] Mixed", BODY),
        Paragraph("Page that should be removed: _____________________________________________", BODY), Paragraph("Page that needs more room: ______________________________________________", BODY),
        Paragraph("Overall: [ ] physical sample next  [ ] revise dummy  [ ] rethink trim", BODY),
    ]


def write_readme(folder: Path, title: str, version: str, files: list[tuple[str, str]], purpose: str) -> None:
    lines = [title, "=" * len(title), "", f"Version: {version}", "Publisher: Forge & Verse", "", "Purpose", "-------", purpose, "", "Included files", "--------------"]
    for name, description in files: lines.append(f"- {name}: {description}")
    lines += ["", "Testing and records caution", "---------------------------", "Use fictitious or sanitized information unless your agency has approved the proof for a controlled test. These materials are not approved case records, chain-of-custody documents, or substitutes for agency policy.", "", "Permission", "----------", "You may print and internally evaluate these studio proofs. You may not sell, rebrand, redistribute, or represent them as a finished Forge & Verse release.", "", "Verification", "------------", "SHA-256 values are listed in SHA256SUMS.txt.", ""]
    (folder / "README.txt").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def deterministic_package(folder: Path, bundle_path: Path, names: list[str]) -> str:
    checksums = [(sha256(folder / name), name) for name in names]
    (folder / "SHA256SUMS.txt").write_text("\n".join(f"{digest}  {name}" for digest, name in checksums) + "\n", encoding="utf-8", newline="\n")
    all_names = names + ["SHA256SUMS.txt"]
    if bundle_path.exists(): bundle_path.unlink()
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        root = bundle_path.stem
        for name in all_names:
            info = zipfile.ZipInfo(f"{root}/{name}", date_time=(2026, 8, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = (0o644 & 0xFFFF) << 16
            archive.writestr(info, (folder / name).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(bundle_path) as archive:
        bad = archive.testzip()
        if bad: raise RuntimeError(f"ZIP integrity failed at {bad}")
    return sha256(bundle_path)


def main() -> None:
    for obsolete in [DOWNLOADS / "bench-status-pad-field-test-v0.2", DOWNLOADS / "examination-notebook-field-test-v0.2"]:
        if obsolete.exists(): shutil.rmtree(obsolete)
    for obsolete in [DOWNLOADS / "forge-and-verse-bench-status-pad-field-test-v0.2.zip", DOWNLOADS / "forge-and-verse-examination-notebook-field-test-v0.2.zip"]:
        if obsolete.exists(): obsolete.unlink()

    bench_dir = DOWNLOADS / "bench-status-pad-field-test-v0.3"; notebook_dir = DOWNLOADS / "examination-notebook-field-test-v0.3"
    for directory in [bench_dir, notebook_dir]:
        if directory.exists(): shutil.rmtree(directory)
        directory.mkdir(parents=True)

    build_doc(bench_dir / "bench-status-pad-field-test-guide.pdf", bench_story(), "Bench Status Pad Field Test", "0.3")
    shutil.copy2(SOURCE / "bench-status-pad-prototype-4x6.pdf", bench_dir / "bench-status-pad-prototype-4x6.pdf")
    shutil.copy2(SOURCE / "bench-status-pad-prototype-letter-2up.pdf", bench_dir / "bench-status-pad-prototype-letter-2up.pdf")
    bench_files = [("bench-status-pad-field-test-guide.pdf", "Two-page interruption test and evaluation sheet."), ("bench-status-pad-prototype-4x6.pdf", "Exact-size refined portrait proof."), ("bench-status-pad-prototype-letter-2up.pdf", "Two-up letter-size office-printer test.")]
    write_readme(bench_dir, "Bench Status Pad Field Test", "0.3", bench_files, "A controlled print-and-use test for the refined 4 x 6 continuity-pad concept.")
    bench_names = [name for name, _ in bench_files] + ["README.txt"]
    bench_hash = deterministic_package(bench_dir, DOWNLOADS / "forge-and-verse-bench-status-pad-field-test-v0.3.zip", bench_names)

    build_doc(notebook_dir / "examination-notebook-field-test-guide.pdf", notebook_story(), "Examination Notebook Field Test", "0.3")
    shutil.copy2(SOURCE / "examination-notebook-interior-prototype.pdf", notebook_dir / "examination-notebook-interior-prototype.pdf")
    notebook_files = [("examination-notebook-field-test-guide.pdf", "Two-page physical test protocol and evaluation sheet."), ("examination-notebook-interior-prototype.pdf", "Thirty-two-page 5.5 x 8.5 interior dummy.")]
    write_readme(notebook_dir, "Examination Notebook Field Test", "0.3", notebook_files, "A controlled print-and-use test for the production-oriented Examination Notebook dummy.")
    notebook_names = [name for name, _ in notebook_files] + ["README.txt"]
    notebook_hash = deterministic_package(notebook_dir, DOWNLOADS / "forge-and-verse-examination-notebook-field-test-v0.3.zip", notebook_names)

    print(f"BENCH_BUNDLE_SHA256={bench_hash}")
    print(f"NOTEBOOK_BUNDLE_SHA256={notebook_hash}")


if __name__ == "__main__":
    main()
