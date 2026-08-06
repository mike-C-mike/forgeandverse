from __future__ import annotations

import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "static" / "downloads" / "intake-kit"
FORM = KIT / "digital-forensics-intake-request-fillable.pdf"
FIELD_MAP = KIT / "digital-forensics-intake-request-field-map.json"
EXPECTED_FIELDS = 105
EXPECTED_TEXT = 61
EXPECTED_CHECKBOX = 44


def main() -> int:
    if not FORM.exists() or not FIELD_MAP.exists():
        raise SystemExit("Fillable PDF or field map is missing")

    raw = FORM.read_bytes()
    forbidden = (b"/JavaScript", b"/SubmitForm", b"/Launch")
    found_forbidden = [token.decode("ascii") for token in forbidden if token in raw]
    if found_forbidden:
        raise SystemExit(f"Forbidden active PDF actions found: {', '.join(found_forbidden)}")

    doc = fitz.open(FORM)
    fields: list[tuple[str, int]] = []
    for page in doc:
        widget = page.first_widget
        while widget:
            fields.append((widget.field_name, widget.field_type))
            widget = widget.next
    page_count = doc.page_count
    doc.close()

    names = [name for name, _ in fields]
    text_count = sum(kind == fitz.PDF_WIDGET_TYPE_TEXT for _, kind in fields)
    checkbox_count = sum(kind == fitz.PDF_WIDGET_TYPE_CHECKBOX for _, kind in fields)

    mapping = json.loads(FIELD_MAP.read_text(encoding="utf-8"))
    mapped_names = [entry["name"] for entry in mapping.get("fields", [])]

    errors: list[str] = []
    if page_count != 2: errors.append(f"Expected 2 pages, found {page_count}")
    if len(fields) != EXPECTED_FIELDS: errors.append(f"Expected {EXPECTED_FIELDS} fields, found {len(fields)}")
    if text_count != EXPECTED_TEXT: errors.append(f"Expected {EXPECTED_TEXT} text fields, found {text_count}")
    if checkbox_count != EXPECTED_CHECKBOX: errors.append(f"Expected {EXPECTED_CHECKBOX} checkboxes, found {checkbox_count}")
    if len(names) != len(set(names)): errors.append("Duplicate field names found")
    if names != mapped_names: errors.append("PDF field order or names do not match the field map")
    if int(mapping.get("field_count", -1)) != EXPECTED_FIELDS: errors.append("Field map count is incorrect")

    if errors:
        raise SystemExit("Fillable intake audit failed:\n- " + "\n- ".join(errors))

    print("Fillable intake audit passed.")
    print(f"  Pages: {page_count}")
    print(f"  Fields: {len(fields)}")
    print(f"  Text fields: {text_count}")
    print(f"  Checkboxes: {checkbox_count}")
    print("  Active submission or JavaScript actions: none detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
