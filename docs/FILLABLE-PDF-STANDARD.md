# Fillable PDF Standard

A fillable Forge & Verse release should add a digital path without pretending every workflow belongs in a browser.

## Core requirements

- The form must remain usable as a normal printed PDF.
- Fields should sit over the approved visual form rather than creating a second, visually divergent layout.
- Every field needs a stable, descriptive, unique name and an accessible alternate label.
- Multiline areas must allow actual narrative responses without clipping.
- The file must not contain JavaScript, automatic submission actions, telemetry, external links used for data transfer, or a connection back to Forge & Verse.
- The page must plainly state that credentials belong only in an organization-approved channel.
- Agencies must test save, reopen, print, accessibility, signature, routing, and records behavior in the PDF viewer they actually approve.

## Release checks

1. Render the blank fillable PDF and compare it with the print edition.
2. Fill a representative set of text fields and checkboxes.
3. Save, reopen, render, and inspect both pages.
4. Extract the AcroForm field list and confirm names, labels, types, and counts.
5. Confirm that no JavaScript or SubmitForm action is present.
6. Recalculate package and public checksums after any change.

## Current intake implementation

The Digital Forensics Intake Kit v1.2 contains:

- 105 total fields
- 61 text fields
- 44 checkboxes
- no JavaScript
- no automatic form submission
- a machine-readable JSON field map

Build and audit commands:

```powershell
python -m pip install -r .\scripts\requirements-forms.txt
python .\scripts\build_fillable_intake_form.py
python .\scripts\audit_fillable_intake_form.py
```
