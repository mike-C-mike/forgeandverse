from __future__ import annotations

import hashlib
import shutil
import textwrap
import zipfile
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    PageBreak,
    Spacer,
    Table,
    TableStyle,
)

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

FONT_DIRS = [
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/opentype/inter"),
    Path("/usr/share/fonts/truetype/inter"),
]


def find_font(names: list[str]) -> Path:
    for directory in FONT_DIRS:
        for name in names:
            candidate = directory / name
            if candidate.exists():
                return candidate
    raise FileNotFoundError(f"Could not locate any of: {', '.join(names)}")


pdfmetrics.registerFont(TTFont("FV-Sans", str(find_font(["Inter-Regular.otf", "DejaVuSans.ttf"]))))
pdfmetrics.registerFont(TTFont("FV-Sans-Bold", str(find_font(["Inter-Bold.otf", "DejaVuSans-Bold.ttf"]))))
pdfmetrics.registerFont(TTFont("FV-Serif", str(find_font(["DejaVuSerif.ttf"]))))
pdfmetrics.registerFont(TTFont("FV-Serif-Bold", str(find_font(["DejaVuSerif-Bold.ttf"]))))

styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="FV-Sans",
    fontSize=9.1,
    leading=12.4,
    textColor=INK,
    spaceAfter=5,
)
SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=7.7,
    leading=10.1,
    textColor=MUTED,
)
EYEBROW = ParagraphStyle(
    "Eyebrow",
    parent=BODY,
    fontName="FV-Sans-Bold",
    fontSize=7.5,
    leading=9,
    textColor=BRASS,
    spaceAfter=4,
)
TITLE = ParagraphStyle(
    "Title",
    parent=BODY,
    fontName="FV-Serif-Bold",
    fontSize=24,
    leading=27,
    textColor=INK,
    spaceAfter=6,
)
LEDE = ParagraphStyle(
    "Lede",
    parent=BODY,
    fontSize=10.5,
    leading=14,
    textColor=MUTED,
    spaceAfter=10,
)
H2 = ParagraphStyle(
    "H2",
    parent=BODY,
    fontName="FV-Serif-Bold",
    fontSize=14,
    leading=17,
    textColor=INK,
    spaceBefore=8,
    spaceAfter=5,
)
H3 = ParagraphStyle(
    "H3",
    parent=BODY,
    fontName="FV-Sans-Bold",
    fontSize=9.2,
    leading=11,
    textColor=INK,
    spaceAfter=2,
)
CHECK = ParagraphStyle(
    "Check",
    parent=BODY,
    leftIndent=14,
    firstLineIndent=-14,
    spaceAfter=4,
)


def header_footer(canvas, doc, label: str, version: str) -> None:
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(BRASS)
    canvas.setLineWidth(0.8)
    canvas.line(0.62 * inch, height - 0.46 * inch, width - 0.62 * inch, height - 0.46 * inch)
    canvas.setFont("FV-Sans-Bold", 7.5)
    canvas.setFillColor(INK)
    canvas.drawString(0.62 * inch, height - 0.36 * inch, "FORGE & VERSE")
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 0.62 * inch, height - 0.36 * inch, label.upper())
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(0.62 * inch, 0.48 * inch, width - 0.62 * inch, 0.48 * inch)
    canvas.setFont("FV-Sans", 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.62 * inch, 0.32 * inch, f"Studio proof {version} | For evaluation only | Do not use as an official case record")
    canvas.drawRightString(width - 0.62 * inch, 0.32 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_doc(path: Path, story: list, label: str, version: str) -> None:
    doc = BaseDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.64 * inch,
        rightMargin=0.64 * inch,
        topMargin=0.67 * inch,
        bottomMargin=0.66 * inch,
        title=label,
        author="Forge & Verse",
        subject=f"{label} field testing guide",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    template = PageTemplate(
        id="proof",
        frames=[frame],
        onPage=lambda canvas, current_doc: header_footer(canvas, current_doc, label, version),
    )
    doc.addPageTemplates([template])
    doc.build(story)


def callout(label: str, text: str, dark: bool = False) -> Table:
    bg = INK if dark else PALE
    body_color = WHITE if dark else INK
    content = [
        Paragraph(label.upper(), ParagraphStyle("CalloutLabel", parent=EYEBROW, textColor=BRASS, spaceAfter=3)),
        Paragraph(text, ParagraphStyle("CalloutBody", parent=BODY, textColor=body_color, fontSize=10 if dark else 9.2, leading=13)),
    ]
    table = Table([[content]], colWidths=[7.18 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, BRASS),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def checklist(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"[ ] {item}", CHECK) for item in items]


def rating_table(rows: list[tuple[str, str]]) -> Table:
    data = [[Paragraph("TEST", EYEBROW), Paragraph("NOTES", EYEBROW), Paragraph("1-5", EYEBROW)]]
    for title, prompt in rows:
        data.append([
            Paragraph(f'<b>{title}</b><br/><font size="7.5" color="#666C70">{prompt}</font>', BODY),
            Paragraph("_________________________________________________________________<br/>_________________________________________________________________", SMALL),
            Paragraph("____", BODY),
        ])
    table = Table(data, colWidths=[1.95 * inch, 4.55 * inch, 0.68 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]))
    return table


def bench_story(version: str) -> list:
    story: list = [
        Paragraph("THE EXAMINER'S BENCH", EYEBROW),
        Paragraph("Bench Status Pad Field Test", TITLE),
        Paragraph("Test whether a 4 x 6 sheet can preserve the active state of an examination without becoming another record to maintain.", LEDE),
        callout("The test", "Complete the sheet at the end of a realistic work session. Put it out of sight. Return later and measure whether the next action becomes clear in under thirty seconds.", dark=True),
        Spacer(1, 8),
        Paragraph("Before you print", H2),
        *checklist([
            "Use the exact-size 4 x 6 PDF for a real scale test.",
            "Use the letter two-up PDF when your printer cannot feed 4 x 6 stock.",
            "Print at 100 percent or Actual Size. Disable Fit, Shrink, or Scale to Page.",
            "Use fictitious or sanitized case information for testing.",
            "Do not treat the proof as an approved agency form or official examination note.",
        ]),
        Paragraph("A useful scenario", H2),
        Paragraph("Pause during an acquisition, review, or verification step that has a clear current state, a recent completed action, and one unresolved question. Fill the sheet with normal handwriting while you are genuinely ready to leave the bench.", BODY),
        Paragraph("Run the return test", H2),
        *checklist([
            "Wait at least two hours. Overnight or a weekend is better.",
            "Start a timer before reading the sheet.",
            "Stop when you can state the current process, last completed action, next action, and blocker.",
            "Record the time. Under thirty seconds is the design target.",
            "Mark any field you skipped, misunderstood, or wished had more room.",
        ]),
        PageBreak(),
        Paragraph("Evaluation sheet", TITLE),
        Paragraph("Score the proof after a real interruption. A neat page is not the goal. Fast, accurate re-entry is.", LEDE),
        rating_table([
            ("Speed", "How quickly did the case state return? Record the measured time."),
            ("Clarity", "Did the fields capture the information you actually needed?"),
            ("Writing room", "Was 4 x 6 large enough with normal handwriting?"),
            ("Friction", "Could the sheet be completed while you were ready to leave?"),
            ("State markers", "Did Running, Safe to resume, and Blocked help or distract?"),
            ("Disposal cue", "Was the temporary-record reminder clear without dominating the page?"),
        ]),
        Spacer(1, 8),
        Paragraph("What should change?", H2),
        Paragraph("Remove or rename: ________________________________________________________________", BODY),
        Paragraph("Add or enlarge: __________________________________________________________________", BODY),
        Paragraph("The one field that earned its space: _________________________________________________", BODY),
        Paragraph("Measured return time: ______________________ seconds", BODY),
        Paragraph("Overall verdict:  [ ] Ready for another test   [ ] Revise first   [ ] Wrong format", BODY),
    ]
    return story


def notebook_story(version: str) -> list:
    story: list = [
        Paragraph("THE EXAMINER'S BENCH", EYEBROW),
        Paragraph("Examination Notebook Field Test", TITLE),
        Paragraph("Test whether light structure can support forensic thinking without crowding the page or pretending to replace the official record.", LEDE),
        callout("The test", "Use the sample through a real reasoning task. The structured pages should orient the work, then disappear. The open pages should feel generous enough that the notebook stops announcing its own design.", dark=True),
        Spacer(1, 8),
        Paragraph("Before you print", H2),
        *checklist([
            "Print double-sided at 100 percent on paper close to the stock you would actually carry.",
            "Use fictitious or sanitized information unless your agency has approved the test.",
            "Try the pens you normally reach for, including gel, rollerball, and ballpoint.",
            "Judge the interior as a working object, not as a presentation PDF.",
            "Do not treat the prototype as an approved case notebook or records process.",
        ]),
        Paragraph("Use the structured pages", H2),
        Paragraph("Complete the case-orientation page, add several evidence sources, record two tool/version references, write open questions, and index at least one finding. Skip anything that does not help. A field that is repeatedly skipped may not deserve to exist.", BODY),
        Paragraph("Use the open pages", H2),
        Paragraph("Spend at least twenty minutes mapping a real technical problem, outlining an examination path, or writing through an uncertainty. Try the ruled, margin, dot-grid, and nearly blank treatments. Notice which structure supports thought and which one keeps asking to be noticed.", BODY),
        Paragraph("Test re-entry", H2),
        Paragraph("Leave the notebook closed for several hours. Return and use only the orientation, indexes, and your handwritten pages to reconstruct where the work stood and what question remained open.", BODY),
        PageBreak(),
        Paragraph("Evaluation sheet", TITLE),
        Paragraph("The notebook succeeds when it adds orientation at a few critical moments and gives the rest of the space back to the examiner.", LEDE),
        rating_table([
            ("Orientation", "Did the front matter help you enter or re-enter the work?"),
            ("Structure", "Which fields earned their space, and which felt supervisory?"),
            ("Writing room", "Did the page feel open enough for diagrams, questions, and long notes?"),
            ("Ruling", "Which treatment best supported your normal thinking style?"),
            ("Pen response", "Note bleed-through, feathering, drag, and drying behavior."),
            ("Record awareness", "Was the policy reminder useful, proportionate, and clear?"),
        ]),
        Spacer(1, 8),
        Paragraph("Working-page preference", H2),
        Paragraph("[ ] Light ruled   [ ] Ruled with margin   [ ] Dot grid   [ ] Nearly blank   [ ] Mixed interior", BODY),
        Paragraph("Remove or rename: ________________________________________________________________", BODY),
        Paragraph("Add or enlarge: __________________________________________________________________", BODY),
        Paragraph("The page that felt most natural: ____________________________________________________", BODY),
        Paragraph("Overall verdict:  [ ] Continue this direction   [ ] Reduce structure   [ ] Rethink the format", BODY),
    ]
    return story


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_readme(folder: Path, title: str, version: str, files: list[tuple[str, str]], notice: str) -> None:
    lines = [
        title,
        "=" * len(title),
        "",
        f"Version: {version}",
        "Publisher: Forge & Verse",
        "",
        "Purpose",
        "-------",
        notice,
        "",
        "Included files",
        "--------------",
    ]
    for name, description in files:
        lines.append(f"- {name}: {description}")
    lines += [
        "",
        "Testing and records caution",
        "---------------------------",
        "Use fictitious or sanitized information unless your agency has approved the proof for a controlled test. These materials are not approved case records, chain-of-custody documents, or substitutes for agency policy.",
        "",
        "Permission",
        "----------",
        "You may print and internally evaluate these studio proofs. You may not sell, rebrand, redistribute, or represent them as an approved Forge & Verse release.",
        "",
        "Verification",
        "------------",
        "SHA-256 values are listed in SHA256SUMS.txt.",
        "",
    ]
    (folder / "README.txt").write_text("\n".join(lines), encoding="utf-8")


def package(folder: Path, bundle_path: Path, files: list[str]) -> tuple[str, list[dict[str, str]]]:
    checksum_rows = []
    for name in files:
        target = folder / name
        checksum_rows.append({"label": name, "file": name, "algorithm": "SHA-256", "value": sha256(target)})
    manifest = folder / "SHA256SUMS.txt"
    manifest.write_text("\n".join(f"{row['value']}  {row['file']}" for row in checksum_rows) + "\n", encoding="utf-8")
    bundle_files = files + ["SHA256SUMS.txt"]
    if bundle_path.exists():
        bundle_path.unlink()
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        root_name = bundle_path.stem
        for name in bundle_files:
            archive.write(folder / name, arcname=f"{root_name}/{name}")
    with zipfile.ZipFile(bundle_path) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"ZIP integrity failed at {bad}")
    return sha256(bundle_path), checksum_rows


def main() -> None:
    bench_version = "0.2"
    notebook_version = "0.2"

    bench_dir = DOWNLOADS / "bench-status-pad-field-test-v0.2"
    notebook_dir = DOWNLOADS / "examination-notebook-field-test-v0.2"
    for directory in (bench_dir, notebook_dir):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True)

    build_doc(bench_dir / "bench-status-pad-field-test-guide.pdf", bench_story(bench_version), "Bench Status Pad Field Test", bench_version)
    shutil.copy2(SOURCE / "bench-status-pad-prototype-4x6.pdf", bench_dir / "bench-status-pad-prototype-4x6.pdf")
    shutil.copy2(SOURCE / "bench-status-pad-prototype-letter-2up.pdf", bench_dir / "bench-status-pad-prototype-letter-2up.pdf")
    bench_files = [
        ("bench-status-pad-field-test-guide.pdf", "Two-page test protocol and evaluation sheet."),
        ("bench-status-pad-prototype-4x6.pdf", "Exact-size portrait proof."),
        ("bench-status-pad-prototype-letter-2up.pdf", "Two-up letter-size print test."),
    ]
    write_readme(bench_dir, "Bench Status Pad Field Test", bench_version, bench_files, "A controlled print-and-use test for the 4 x 6 continuity-pad concept.")
    bench_names = [name for name, _ in bench_files] + ["README.txt"]
    bench_bundle = DOWNLOADS / "forge-and-verse-bench-status-pad-field-test-v0.2.zip"
    bench_bundle_hash, bench_rows = package(bench_dir, bench_bundle, bench_names)

    build_doc(notebook_dir / "examination-notebook-field-test-guide.pdf", notebook_story(notebook_version), "Examination Notebook Field Test", notebook_version)
    shutil.copy2(SOURCE / "examination-notebook-interior-prototype.pdf", notebook_dir / "examination-notebook-interior-prototype.pdf")
    notebook_files = [
        ("examination-notebook-field-test-guide.pdf", "Two-page test protocol and evaluation sheet."),
        ("examination-notebook-interior-prototype.pdf", "Twelve-page interior proof with structured and open working pages."),
    ]
    write_readme(notebook_dir, "Examination Notebook Field Test", notebook_version, notebook_files, "A controlled print-and-use test for the tactile Examination Notebook interior.")
    notebook_names = [name for name, _ in notebook_files] + ["README.txt"]
    notebook_bundle = DOWNLOADS / "forge-and-verse-examination-notebook-field-test-v0.2.zip"
    notebook_bundle_hash, notebook_rows = package(notebook_dir, notebook_bundle, notebook_names)

    print(f"BENCH_BUNDLE_SHA256={bench_bundle_hash}")
    for row in bench_rows:
        print(f"BENCH_FILE={row['file']}|{row['value']}")
    print(f"NOTEBOOK_BUNDLE_SHA256={notebook_bundle_hash}")
    for row in notebook_rows:
        print(f"NOTEBOOK_FILE={row['file']}|{row['value']}")


if __name__ == "__main__":
    main()
