from __future__ import annotations

"""Build the local-only fillable PDF edition of the Digital Forensics Intake Request.

The visual source remains the approved print-ready PDF. Transparent AcroForm widgets are
placed over the existing writing areas so the fillable and print editions remain visually
identical. The file does not submit data or contain JavaScript.
"""

from dataclasses import dataclass
from pathlib import Path
import json
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "static" / "downloads" / "intake-kit"
SOURCE = KIT / "digital-forensics-intake-request.pdf"
OUTPUT = KIT / "digital-forensics-intake-request-fillable.pdf"
FIELD_MAP = KIT / "digital-forensics-intake-request-field-map.json"
PX_TO_PT = 72 / 120  # Coordinates were measured from the 120 dpi review render.


@dataclass(frozen=True)
class Field:
    page: int
    name: str
    label: str
    rect_px: tuple[float, float, float, float]
    kind: str = "text"
    multiline: bool = False
    maxlen: int | None = None


def rpx(values: tuple[float, float, float, float]) -> fitz.Rect:
    x0, y0, x1, y1 = values
    return fitz.Rect(x0 * PX_TO_PT, y0 * PX_TO_PT, x1 * PX_TO_PT, y1 * PX_TO_PT)


def text(page: int, name: str, label: str, rect: tuple[float, float, float, float], *, multiline: bool = False, maxlen: int | None = None) -> Field:
    return Field(page, name, label, rect, "text", multiline, maxlen)


def check(page: int, name: str, label: str, x: float, y: float, size: float = 13) -> Field:
    return Field(page, name, label, (x, y, x + size, y + size), "checkbox")


FIELDS: list[Field] = [
    # Page 1: request and case information
    text(0, "requesting_agency_unit", "Requesting agency or unit", (58, 220, 350, 250)),
    text(0, "date_submitted", "Date submitted", (365, 220, 650, 250), maxlen=30),
    text(0, "requested_completion_date", "Requested completion date", (666, 220, 962, 250), maxlen=40),
    text(0, "requestor_name_title", "Requestor name and title", (58, 284, 350, 316)),
    text(0, "badge_employee_id", "Badge or employee ID", (365, 284, 650, 316), maxlen=45),
    text(0, "phone", "Phone", (666, 284, 962, 316), maxlen=45),
    text(0, "email", "Email", (58, 349, 350, 384)),
    text(0, "case_incident_number", "Case or incident number", (365, 349, 650, 384), maxlen=55),
    text(0, "evidence_system_number", "Evidence system number", (666, 349, 962, 384), maxlen=55),
    text(0, "incident_offense_type", "Incident or offense type", (58, 414, 350, 450)),
    text(0, "lead_investigator", "Lead investigator", (365, 414, 650, 450)),
    text(0, "prosecutor_legal_contact", "Prosecutor or legal contact", (666, 414, 962, 450)),
    check(0, "priority_routine", "Routine priority", 60, 469),
    check(0, "priority_expedited", "Expedited priority", 143, 469),
    check(0, "priority_emergency", "Emergency priority", 242, 469),
    text(0, "priority_justification", "Priority justification", (350, 464, 775, 491)),

    # Page 1: authority and scope
    check(0, "authority_search_warrant", "Search warrant authority", 127, 536),
    check(0, "authority_consent", "Consent authority", 250, 536),
    check(0, "authority_exigent", "Exigent circumstances authority", 350, 536),
    check(0, "authority_agency_owned", "Agency-owned system or device authority", 495, 536),
    check(0, "authority_other_selected", "Other authority selected", 728, 536),
    text(0, "authority_other", "Other authority", (786, 526, 930, 551)),
    check(0, "authority_documentation_attached", "Authority documentation attached", 127, 558),
    check(0, "authority_documentation_case_file", "Authority documentation available in case file", 223, 558),
    check(0, "authority_documentation_not_applicable", "Authority documentation not applicable", 384, 558),
    text(0, "authority_date_expiration", "Authority date or expiration", (585, 551, 855, 575)),
    text(0, "scope_of_examination", "Scope of examination", (58, 599, 962, 660), multiline=True),
    text(0, "investigative_question", "Question the examination should help answer", (58, 704, 962, 775), multiline=True),
    text(0, "known_facts_time_sensitive", "Known facts and time-sensitive concerns", (58, 814, 962, 874), multiline=True),

    # Page 1: submitted devices and media, four rows by six columns
    *[
        text(0, f"device_{row}_{field}", label, rect)
        for row, y0, y1 in ((1, 963, 1013), (2, 1014, 1064), (3, 1065, 1115), (4, 1116, 1166))
        for field, label, x0, x1 in (
            ("evidence_id", f"Device {row} item or evidence ID", 58, 208),
            ("description", f"Device {row} device or media", 208, 359),
            ("make_model", f"Device {row} make or model", 359, 510),
            ("serial_id", f"Device {row} serial, IMEI, or service ID", 510, 661),
            ("power_condition", f"Device {row} power or condition", 661, 812),
            ("owner_user", f"Device {row} owner or primary user", 812, 962),
        )
        for rect in ((x0 + 3, y0 + 3, x1 - 3, y1 - 3),)
    ],
    check(0, "packaging_intact", "Packaging intact", 237, 1171),
    check(0, "packaging_opened", "Packaging opened for safety or preservation", 297, 1171),
    check(0, "packaging_unsealed", "Packaging unsealed", 538, 1171),
    check(0, "packaging_other_selected", "Other packaging condition selected", 620, 1171),
    text(0, "packaging_other", "Other packaging or seal condition", (681, 1166, 878, 1192)),

    # Page 2: requested services
    check(1, "service_preservation_isolation", "Preservation or isolation requested", 59, 208),
    check(1, "service_mobile_acquisition", "Mobile acquisition requested", 239, 208),
    check(1, "service_computer_image", "Computer or drive image requested", 389, 208),
    check(1, "service_removable_media", "Removable media acquisition requested", 582, 208),
    check(1, "service_targeted_extraction", "Targeted extraction requested", 59, 230),
    check(1, "service_file_system_full", "File-system or full extraction requested", 218, 230),
    check(1, "service_cloud_account", "Cloud or account collection requested", 435, 230),
    check(1, "service_password_recovery", "Password recovery attempt requested", 635, 230),
    check(1, "service_malware_triage", "Malware or incident triage requested", 59, 251),
    check(1, "service_review_analysis", "Data review or analysis requested", 250, 251),
    check(1, "service_technical_report", "Technical report requested", 425, 251),
    check(1, "service_other_selected", "Other service selected", 560, 251),
    text(1, "service_other", "Other requested service", (620, 245, 800, 271)),
    text(1, "requested_date_range", "Requested date range", (58, 282, 500, 314)),
    text(1, "known_accounts_usernames_phones", "Known accounts, usernames, or phone numbers", (516, 282, 962, 314)),
    text(1, "known_contacts_identifiers", "Known contacts or identifiers", (58, 346, 500, 379)),
    text(1, "known_keywords_filenames_apps", "Known keywords, filenames, or applications", (516, 346, 962, 379)),
    text(1, "specific_data_requested", "Specific data requested", (58, 420, 962, 489), multiline=True),
    text(1, "relevant_context", "Relevant context for the examiner", (58, 530, 962, 595), multiline=True),

    # Page 2: access, handling, and submission notes
    check(1, "passcode_yes", "Known passcode provided through approved method", 251, 662),
    check(1, "passcode_no", "No known passcode", 539, 662),
    check(1, "passcode_unknown", "Passcode status unknown", 584, 662),
    check(1, "device_state_on", "Device state on", 250, 703),
    check(1, "device_state_off", "Device state off", 309, 703),
    check(1, "device_state_unknown", "Device state unknown", 354, 703),
    check(1, "network_isolated", "Network isolated", 541, 703),
    check(1, "network_connected", "Network connected", 638, 703),
    check(1, "network_unknown", "Network state unknown", 728, 703),
    check(1, "accessory_charger", "Charger submitted", 217, 724),
    check(1, "accessory_cable", "Cable submitted", 295, 724),
    check(1, "accessory_sim", "SIM submitted", 350, 724),
    check(1, "accessory_memory_card", "Memory card submitted", 399, 724),
    check(1, "accessory_external_storage", "External storage submitted", 521, 724),
    check(1, "accessory_other_selected", "Other accessory selected", 642, 724),
    text(1, "accessory_other", "Other accessory", (691, 718, 855, 742)),
    text(1, "handling_history", "Handling history, preservation steps, and unusual conditions", (58, 777, 962, 828), multiline=True),
    text(1, "additional_instructions", "Additional instructions or limitations", (58, 868, 962, 922), multiline=True),

    # Page 2: submission and forensic unit acceptance
    text(1, "requestor_signature", "Requestor signature or typed name", (58, 1000, 500, 1032)),
    text(1, "requestor_signature_datetime", "Requestor date and time", (515, 1000, 962, 1032)),
    text(1, "received_by", "Received by", (58, 1066, 500, 1099)),
    text(1, "date_time_received", "Date and time received", (515, 1066, 962, 1099)),
    text(1, "evidence_location_transfer", "Evidence location or transfer record", (58, 1132, 500, 1164)),
    text(1, "forensic_request_queue_number", "Forensic request or queue number", (515, 1132, 962, 1164)),
    check(1, "scope_confirmed_yes", "Initial scope confirmed with requestor: yes", 308, 1183),
    check(1, "scope_confirmed_no", "Initial scope confirmed with requestor: no", 368, 1183),
    text(1, "clarification_needed", "Clarification needed", (410, 1178, 840, 1202)),
    text(1, "forensic_unit_intake_notes", "Forensic unit intake notes", (228, 1203, 805, 1232)),
]


def add_text_widget(page: fitz.Page, field: Field) -> None:
    widget = fitz.Widget()
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.field_name = field.name
    widget.field_label = field.label
    widget.rect = rpx(field.rect_px)
    widget.field_value = ""
    widget.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE if field.multiline else 0
    widget.text_font = "Helv"
    widget.text_fontsize = 8.5 if not field.multiline else 8.2
    widget.text_color = (0.08, 0.08, 0.08)
    widget.fill_color = None
    widget.border_color = None
    widget.border_width = 0
    if field.maxlen:
        widget.text_maxlen = field.maxlen
    page.add_widget(widget)


def add_checkbox_widget(page: fitz.Page, field: Field) -> None:
    widget = fitz.Widget()
    widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = field.name
    widget.field_label = field.label
    widget.rect = rpx(field.rect_px)
    widget.field_value = False
    widget.fill_color = None
    widget.border_color = None
    widget.border_width = 0
    page.add_widget(widget)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source PDF: {SOURCE}")

    doc = fitz.open(SOURCE)
    for field in FIELDS:
        page = doc[field.page]
        if field.kind == "checkbox":
            add_checkbox_widget(page, field)
        else:
            add_text_widget(page, field)

    metadata = doc.metadata or {}
    metadata.update(
        {
            "title": "Digital Forensics Intake Request - Fillable Edition",
            "author": "Forge & Verse",
            "subject": "Local-only fillable digital forensic services request template",
            "keywords": "digital forensics, intake, request, fillable PDF, evidence, template",
            "creator": "Forge & Verse / PyMuPDF",
        }
    )
    doc.set_metadata(metadata)
    doc.save(OUTPUT, garbage=4, deflate=True, clean=True)
    doc.close()

    verification = fitz.open(OUTPUT)
    names: list[str] = []
    for page in verification:
        widget = page.first_widget
        while widget:
            names.append(widget.field_name)
            widget = widget.next
    verification.close()

    if len(names) != len(FIELDS):
        raise SystemExit(f"Expected {len(FIELDS)} fields, found {len(names)}")
    if len(names) != len(set(names)):
        raise SystemExit("Duplicate field names detected")

    field_map = {
        "release": "Digital Forensics Intake Kit",
        "version": "1.2",
        "form": OUTPUT.name,
        "field_count": len(FIELDS),
        "fields": [
            {
                "name": field.name,
                "label": field.label,
                "page": field.page + 1,
                "type": field.kind,
                "multiline": field.multiline,
            }
            for field in FIELDS
        ],
    }
    FIELD_MAP.write_text(json.dumps(field_map, indent=2) + "\n", encoding="utf-8")

    print(f"Created {OUTPUT}")
    print(f"Created {FIELD_MAP}")
    print(f"Fields: {len(names)} ({sum(f.kind == 'checkbox' for f in FIELDS)} checkboxes, {sum(f.kind == 'text' for f in FIELDS)} text fields)")


if __name__ == "__main__":
    main()
