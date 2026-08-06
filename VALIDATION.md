# Forge & Verse v18 Validation

Validated in the build environment on August 6, 2026.

## Repository checks

Passed:

- TOML, YAML, JSON, and front matter parsing
- Reserved Hugo field checks
- Required fields for works, free releases, journal entries, discipline pages, and design studies
- Discipline, release-path, related-release, related-journal, related-study, and related-work relationships
- Journal-kind validation
- Static image, download, proof-file, and proof-bundle references
- Field-proof metadata, bundles, and SHA-256 values
- Release-manifest file sizes, routes, media records, and hashes
- Intake field-map count and release-page metadata
- Release Desk content and layout presence
- Machine-readable release-ledger schema, entry count, routes, byte sizes, media types, and per-file SHA-256 values
- Plain-text release-ledger checksum manifest
- PDF signatures, DOCX archive structure, and ZIP integrity
- Hugo template delimiter balance
- CSS parsing: 1,056 rules, zero parse errors
- JavaScript syntax validation, including the local browser hash verifier
- Python compilation for repository scripts

Commands:

```text
python scripts/build_release_ledger.py
python scripts/validate.py
node --check assets/js/site.js
```

Result:

```text
Forge & Verse validation passed.
Disciplines: 4
Study stages: 5
Works: 1
Free works: 1
Journal pieces: 5
Design studies: 4
Content files: 28
```

The generated release desk currently tracks:

- 1 open release
- 2 field-proof packages
- 18 downloadable package files and supporting manifests
- 1 machine-readable release ledger

## Remaining local check

Run the complete Hugo v0.164.0 build and rendered-site validator on the Windows development machine:

```powershell
.\scripts\build.ps1
```

Then start the local server and open the priority page set:

```powershell
.\scripts\dev.ps1
.\scripts\open-review-pages.ps1
```

Priority review:

- `/`
- `/works/`
- `/releases/`
- `/downloads/`
- `/downloads/digital-forensics-intake-request/`
- `/roadmap/bench-status-pad/`
- `/roadmap/examination-notebook/`

The Release Desk browser verifier should be tested in the local HTTPS or localhost context with one known matching bundle and one deliberately different file.
