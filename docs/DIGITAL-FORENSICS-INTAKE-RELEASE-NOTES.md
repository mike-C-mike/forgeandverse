# Digital Forensics Intake Kit Release Notes

## Version 1.2 - August 5, 2026

The kit now supports paper-first, local digital, and agency-customized workflows without forcing one interaction model.

### Added

- Local-only fillable PDF with 105 named fields
- 61 text fields and 44 checkboxes
- Machine-readable JSON field map
- Machine-readable public release manifest with sizes, media types, and SHA-256 values
- Public working-style choices for fillable PDF, print PDF, and editable DOCX
- Fillable-PDF build and audit scripts
- Viewer, save, print, routing, and records testing guidance in the implementation guide

### Security and privacy boundary

The fillable PDF contains no JavaScript, automatic submission action, telemetry, or connection to Forge & Verse. The adopting organization remains responsible for storage, routing, access, retention, and protection of completed files.

## Version 1.1 - August 4, 2026

The original two-page intake form is now one part of a broader handoff kit.

### Added

- One-page requester guide for officers and investigators
- Four-page implementation guide for forensic units and administrators
- Editable DOCX versions of both guides
- Versioned ZIP bundle
- README and use terms
- Internal component checksum manifest
- Public checksum manifest that includes the complete bundle
- Public release history and adoption path
- Related practice note: `The Device Is Not the Question`

### Unchanged

The original intake request PDF and DOCX remain byte-for-byte unchanged from version 1.0. Their SHA-256 values remain the same.

## Version 1.0 - August 4, 2026

Initial release of the two-page Digital Forensics Intake Request as print-ready PDF and editable DOCX.
