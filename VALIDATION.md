# Forge & Verse v16 Validation

Validated in the build environment on August 5, 2026.

## Repository checks

Passed:

- TOML, YAML, JSON, and front matter parsing
- Reserved Hugo field checks
- Required fields for works, free releases, journal entries, discipline pages, and design studies
- Discipline, release-path, related-release, and related-journal relationships
- Static image, download, proof-file, and proof-bundle references
- Field-proof version, date, package metadata, and SHA-256 values
- Release-manifest file sizes, media records, routes, and SHA-256 values
- Intake field-map count and release-page metadata
- PDF signatures, DOCX archive structure, and ZIP integrity
- Hugo template delimiter balance
- CSS brace balance

Command:

```text
python scripts/validate.py
```

Result:

```text
Forge & Verse validation passed.
Disciplines: 4
Study stages: 5
Works: 1
Free works: 1
Journal pieces: 4
Design studies: 4
Content files: 26
```

## Fillable intake form

Passed:

- Two-page PDF
- 105 unique AcroForm fields
- 61 text fields
- 44 checkboxes
- Field names and order match the machine-readable field map
- No JavaScript, SubmitForm, or Launch action detected
- Blank fillable render remains visually equivalent to the print edition
- Representative text and checkbox values were filled, saved, reopened, and rendered
- No clipping found in the filled review sample

Command:

```text
python scripts/audit_fillable_intake_form.py
```

## Intake companion documents

Visually reviewed after regeneration:

- Requester guide: one page
- Implementation guide: four pages
- No clipping, overlaps, broken glyphs, or missing content found
- Both footers identify Intake Kit v1.2
- Implementation guide includes fillable-viewer, local-storage, save, print, routing, and records testing guidance

## Intake package

Passed:

- Versioned v1.2 ZIP integrity
- Component checksum manifest
- Public SHA-256 manifest
- Machine-readable JSON release manifest
- Fillable PDF, print PDF, editable sources, field map, guides, README, release notes, and use terms present

## Remaining local check

Hugo Extended is not installed in this build environment. Run the complete Hugo v0.164.0 build and rendered-site validator on the Windows development machine:

```powershell
.\scripts\build.ps1
```

Priority browser review:

- `/downloads/digital-forensics-intake-request/`
- Homepage studio introduction
- Mobile layout of the three working-style cards
- Release manifest and checksum links
