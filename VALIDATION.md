# Forge & Verse v18.19 Validation

Validated in the build environment on August 6, 2026.

## Repository checks

Passed:

- TOML, YAML, JSON, and front matter parsing
- Reserved Hugo field checks
- Required fields for works, free releases, journal entries, discipline pages, and design studies
- Discipline, release-path, related-release, related-journal, related-study, and related-work relationships
- Journal-kind validation
- Five-state physical-edition data and ordering validation
- Nested edition metadata, format specifications, and study-route checks
- Production-partner and fulfillment requirements for any edition marked Available
- Static image, download, proof-file, and proof-bundle references
- Field-proof metadata and SHA-256 values
- Release-manifest file sizes, routes, media records, and hashes
- Intake field-map count and release-page metadata
- 27 image files opened and verified
- 15 PDF signatures verified
- 4 DOCX archives verified, including `word/document.xml`
- 4 ZIP archives tested with no corrupt members
- Hugo template delimiter balance across 42 template files
- CSS parsing: 1,040 qualified rules, 46 at-rules, zero parse errors
- JavaScript syntax validation
- Python compilation for repository scripts

Command:

```text
python scripts/validate.py
```

Result:

```text
Forge & Verse validation passed.
  Disciplines: 4
  Study stages: 5
  Edition states: 5
  Works: 1
  Free works: 1
  Journal pieces: 5
  Design studies: 4
  Content files: 28
```

## What this round specifically validates

- `/editions/` content and layout are present.
- Physical editions use only these public states: `in-studio`, `proof-in-hand`, `edition-approved`, `available`, and `resting`.
- An edition cannot be marked `available` without an external URL, production-partner name, fulfillment note, and purchase-button label.
- A digital room mockup does not silently promote a work to `proof-in-hand`.
- The Believe in the Badge edition remains `in-studio` and has no ordering link.
- Search metadata and Work structured data can include edition state and material direction.
- Work archetypes include the edition model without enabling it by default.

## Remaining local check

A Hugo executable is not available in this build container, so the final generated-site and browser review must run on the Windows development machine:

```powershell
.\scripts\build.ps1
```

The build script will run repository validation, Hugo, and rendered-site validation in sequence.

Then start the local server and open the priority page set:

```powershell
.\scripts\dev.ps1
.\scripts\open-review-pages.ps1
```

Priority review:

- `/`
- `/works/`
- `/works/believe-in-the-badge/`
- `/editions/`
- `/materials/`
- `/journal/`
- `/roadmap/`
- `/roadmap/believe-in-the-badge-edition/`
- `/downloads/digital-forensics-intake-request/`

Review desktop, tablet, and narrow mobile widths, with particular attention to heading balance, natural card height, edition-format cards, and long-page spacing.
