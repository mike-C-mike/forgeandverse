# Forge & Verse v14 Validation

Validated in the build environment on August 4, 2026.

## Repository checks

Passed:

- TOML, YAML, and front matter parsing
- Reserved Hugo field checks
- Required fields for works, free releases, journal entries, discipline pages, and design studies
- Discipline, release-path, related-release, and related-journal relationships
- Static image and download references
- Package-file, companion-preview, adoption-step, and release-history structure
- SHA-256 values referenced by release front matter
- PDF signatures
- DOCX ZIP structure and required content types
- Release ZIP archive integrity
- Hugo template delimiter balance
- CSS brace balance
- JavaScript brace review

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

## Code checks

Passed:

- `node --check assets/js/site.js`
- `tinycss2` stylesheet parse: 849 rules, 0 parse errors
- Python bytecode compilation for validation, document generation, and release packaging scripts

## Intake kit documents

### Requester guide

- DOCX rendered successfully
- Final PDF rendered successfully
- Page count: 1
- Visual review passed with no clipping, overlap, broken glyphs, or missing content
- Accessibility audit: 0 high-severity findings; medium findings relate to layout tables not marked as semantic header tables

### Implementation guide

- DOCX rendered successfully
- Final PDF rendered successfully
- Page count: 4
- Every page visually reviewed
- No clipping, overlap, broken glyphs, or missing content
- Accessibility audit: 0 high-severity findings; medium findings relate to layout tables not marked as semantic header tables

### Release package

- ZIP integrity test passed
- Package contains 9 files inside one versioned folder
- Component SHA-256 manifest included
- Public manifest includes the complete bundle checksum

## Remaining local check

Hugo Extended is not installed in this build environment. Run the complete Hugo v0.164.0 build and rendered-site validator on the Windows development machine:

```powershell
.\scripts\build.ps1
```

Then review these pages in the browser:

- `/downloads/digital-forensics-intake-request/`
- `/journal/the-device-is-not-the-question/`
- `/journal/`
- `/search/?q=objective`
- Homepage Examiner's Bench section
